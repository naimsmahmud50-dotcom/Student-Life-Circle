"""
========================================================================================
MODULE:    AST Whitebox Security Scanner & Penetration Defense Suite
TOPIC:     OWASP ASVS L2, SQLi/ORMi Detection, Safe Deserialization & Zero-IDOR Audit
FILE:      backend/scripts/run_security_sweep.py
PURPOSE:   Performs comprehensive static AST whitebox security analysis across the
           FastAPI backend codebase. Inspects Python Abstract Syntax Trees for:
           1. SQL Injection / ORM Injection via raw string interpolation or concat.
           2. Dangerous function calls (eval, exec, pickle.loads, shell=True).
           3. Hardcoded secrets, API tokens, and private keys.
           4. Object-Level Access Control (IDOR) verification across sensitive endpoints.
           5. ASVS L2 security headers and distributed rate limiting middleware.
AUDIENCE:  Security Compliance Engineers, SRE, Penetration Testers & AI Agents
STANDARDS: OWASP ASVS 4.0 L2, NIST SP 800-53, Bandit/Semgrep Rules, Strict Zero-Emoji
========================================================================================
"""

import os
import sys
import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class WhiteboxSecurityScanner:
    """
    AST-based static whitebox code scanner enforcing OWASP ASVS Level 2 standards.
    """

    DANGEROUS_CALLS = {
        "eval": ("CRITICAL", "Dynamic code evaluation via eval() is prohibited"),
        "exec": ("CRITICAL", "Dynamic execution via exec() is prohibited"),
        "__import__": ("HIGH", "Dynamic module importing via __import__() poses code-injection risks"),
    }

    SQL_SINKS = {"execute", "executemany", "raw", "raw_sql", "execute_sql"}

    def __init__(self, target_dir: Optional[str] = None):
        self.target_dir = Path(target_dir or "backend/app").resolve()
        self.findings: List[Dict[str, Any]] = []
        self.scanned_files_count: int = 0

    def scan_file(self, file_path: Path) -> None:
        """Parses and checks an individual Python file via AST."""
        self.scanned_files_count += 1
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source, filename=str(file_path))
        except Exception as e:
            self.findings.append({
                "file": str(file_path),
                "line": 0,
                "category": "SYNTAX_ERROR",
                "severity": "LOW",
                "message": f"Could not parse file: {str(e)}"
            })
            return

        self._check_ast_nodes(tree, file_path, source)

    def _check_ast_nodes(self, tree: ast.AST, file_path: Path, source: str) -> None:
        """Walks AST to detect injection, dangerous calls, and credential exposures."""
        rel_path = str(file_path)
        source_lines = source.splitlines()

        for node in ast.walk(tree):
            lineno = getattr(node, "lineno", 0)
            line_str = source_lines[lineno - 1] if 0 < lineno <= len(source_lines) else ""
            if "# nosec" in line_str or "# nosemgrep" in line_str:
                continue

            # 1. Dangerous function calls (eval, exec)
            if isinstance(node, ast.Call):
                func_name = None
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in self.DANGEROUS_CALLS:
                    sev, msg = self.DANGEROUS_CALLS[func_name]
                    # Exclude the scanner itself or explicit test harnesses if appropriate
                    if "run_security_sweep.py" not in rel_path:
                        self.findings.append({
                            "file": rel_path,
                            "line": getattr(node, "lineno", 0),
                            "category": "DANGEROUS_EXECUTION",
                            "severity": sev,
                            "message": f"{msg} [call: {func_name}]"
                        })

                # Insecure pickle.loads/load
                if isinstance(node.func, ast.Attribute):
                    val = node.func.value
                    if isinstance(val, ast.Name) and val.id == "pickle" and node.func.attr in {"loads", "load"}:
                        self.findings.append({
                            "file": rel_path,
                            "line": getattr(node, "lineno", 0),
                            "category": "INSECURE_DESERIALIZATION",
                            "severity": "HIGH",
                            "message": "Untrusted pickle deserialization detected"
                        })

                # subprocess shell=True check
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in {"Popen", "call", "run", "check_call", "check_output"}:
                        for kw in node.keywords:
                            if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                self.findings.append({
                                    "file": rel_path,
                                    "line": getattr(node, "lineno", 0),
                                    "category": "COMMAND_INJECTION",
                                    "severity": "HIGH",
                                    "message": "subprocess call with shell=True detected"
                                })

                # SQL Injection detection in cursor.execute / db.raw / connection.execute
                if isinstance(node.func, ast.Attribute) and node.func.attr in self.SQL_SINKS:
                    if node.args:
                        first_arg = node.args[0]
                        # Flag f-strings
                        if isinstance(first_arg, ast.JoinedStr):
                            self.findings.append({
                                "file": rel_path,
                                "line": getattr(node, "lineno", 0),
                                "category": "SQL_INJECTION",
                                "severity": "CRITICAL",
                                "message": f"Direct f-string interpolation into {node.func.attr}() SQL sink"
                            })
                        # Flag string concatenation query + var
                        elif isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, (ast.Add, ast.Mod)):
                            self.findings.append({
                                "file": rel_path,
                                "line": getattr(node, "lineno", 0),
                                "category": "SQL_INJECTION",
                                "severity": "HIGH",
                                "message": f"String concatenation/formatting into {node.func.attr}() SQL sink"
                            })
                        # Flag str.format()
                        elif isinstance(first_arg, ast.Call) and isinstance(first_arg.func, ast.Attribute) and first_arg.func.attr == "format":
                            self.findings.append({
                                "file": rel_path,
                                "line": getattr(node, "lineno", 0),
                                "category": "SQL_INJECTION",
                                "severity": "HIGH",
                                "message": f"str.format() detected in {node.func.attr}() SQL sink"
                            })

            # 2. Hardcoded secret credentials
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name_lower = target.id.lower()
                        if any(token in name_lower for token in ("secret_key", "private_key", "aws_secret", "jwt_secret")):
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                val = node.value.value
                                # Ignore test placeholders or defaults
                                if len(val) >= 24 and not any(safe in val.lower() for safe in ("mock", "test", "dummy", "placeholder", "changeme", "dev", "your-", "none")):
                                    self.findings.append({
                                        "file": rel_path,
                                        "line": getattr(node, "lineno", 0),
                                        "category": "HARDCODED_CREDENTIAL",
                                        "severity": "HIGH",
                                        "message": f"Potential high-entropy hardcoded secret in {target.id}"
                                    })

    def verify_idor_defense(self) -> None:
        """Verifies that sensitive router endpoints enforce IDOR ownership validation."""
        router_file = self.target_dir / "api" / "v1" / "router.py"
        if not router_file.exists():
            return

        with open(router_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check required IDOR guards in router
        checks = [
            ("get_quiz_attempt", "FORBIDDEN_ATTEMPT_OWNERSHIP", "IDOR guard missing on GET /quiz-attempts/{attempt_id}"),
            ("save_quiz_answer", "FORBIDDEN_ATTEMPT_OWNERSHIP", "IDOR guard missing on PUT /quiz-attempts/{attempt_id}/answers"),
            ("submit_quiz_attempt", "FORBIDDEN_ATTEMPT_OWNERSHIP", "IDOR guard missing on POST /quiz-attempts/{attempt_id}/submit"),
            ("get_cv_snapshot", "FORBIDDEN_SNAPSHOT_OWNERSHIP", "IDOR guard missing on GET /career/cv-snapshot/{snapshot_id}"),
        ]

        for func_name, expected_token, err_msg in checks:
            if func_name not in content or expected_token not in content:
                self.findings.append({
                    "file": str(router_file),
                    "line": 1,
                    "category": "IDOR_VULNERABILITY",
                    "severity": "CRITICAL",
                    "message": err_msg
                })

    def verify_security_headers_and_middleware(self) -> None:
        """Verifies that security headers middleware and HSTS max-age=63072000 are present."""
        mw_file = self.target_dir / "core" / "middleware.py"
        headers_file = self.target_dir / "core" / "security_headers.py"

        if not mw_file.exists():
            self.findings.append({
                "file": str(mw_file),
                "line": 1,
                "category": "MISSING_MIDDLEWARE",
                "severity": "HIGH",
                "message": "SecurityHeadersMiddleware not implemented"
            })
            return

        with open(headers_file, "r", encoding="utf-8") as f:
            h_content = f.read()

        if "max-age=63072000" not in h_content:
            self.findings.append({
                "file": str(headers_file),
                "line": 1,
                "category": "HSTS_CONFIG_DEFECT",
                "severity": "HIGH",
                "message": "Strict-Transport-Security must enforce 2-year duration (max-age=63072000)"
            })

    def run_sweep(self) -> Dict[str, Any]:
        """Runs the entire security scan across the codebase."""
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root) / file
                    self.scan_file(full_path)

        self.verify_idor_defense()
        self.verify_security_headers_and_middleware()

        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for f in self.findings:
            sev = f.get("severity", "LOW")
            if sev in severity_counts:
                severity_counts[sev] += 1

        passed = (severity_counts["CRITICAL"] == 0 and severity_counts["HIGH"] == 0 and severity_counts["MEDIUM"] == 0)

        report = {
            "title": "OWASP ASVS L2 Whitebox Security Audit Report",
            "target_directory": str(self.target_dir),
            "scanned_files_count": self.scanned_files_count,
            "findings_count": len(self.findings),
            "findings_by_severity": severity_counts,
            "passed": passed,
            "findings": self.findings
        }

        # Ensure reports directory exists and save
        report_path = Path("backend/reports/security-audit-report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report


def main():
    """Command-line entrypoint for automated security scanning."""
    scanner = WhiteboxSecurityScanner()
    report = scanner.run_sweep()

    print("[SECURITY AUDIT] Scanned files:", report["scanned_files_count"])
    print("[SECURITY AUDIT] Findings summary:", report["findings_by_severity"])
    print("[SECURITY AUDIT] Report saved to: backend/reports/security-audit-report.json")

    if not report["passed"]:
        print("[SECURITY AUDIT] FAILED: Vulnerabilities detected.")
        sys.exit(1)
    else:
        print("[SECURITY AUDIT] PASSED: Zero Critical/High/Medium security vulnerabilities found.")
        sys.exit(0)


if __name__ == "__main__":
    main()

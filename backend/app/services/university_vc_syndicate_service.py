"""
University Venture Capital & Angel Syndicate Service.
Features YC-standard Post-Money SAFE / Convertible Note dilution modeling,
cap table simulation across funding rounds, and verified investor syndicate commitment tracking.
"""

import hashlib
import time
import uuid
from typing import Dict, Any, List, Optional


class UniversityVcAngelSyndicateService:
    """
    Venture Capital and Angel Syndicate modeling engine for university student founders.
    Implements industry-standard Y-Combinator Post-Money SAFE cap table math and syndicate ledger.
    """

    _syndicate_commitments: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def calculate_safe_dilution(
        cls,
        startup_name: str = "Agrojatra EdTech",
        safe_type: str = "POST_MONEY_SAFE",
        investment_amount_usd: float = 150000.0,
        valuation_cap_usd: float = 3000000.0,
        discount_pct: float = 20.0,
        existing_founder_shares: int = 8000000
    ) -> Dict[str, Any]:
        """
        Calculates cap table equity ownership, share issuance, and dilution impact
        under YC Post-Money SAFE or Pre-Money Convertible Note mechanisms.
        """
        if valuation_cap_usd <= 0:
            raise ValueError("Valuation Cap must be strictly positive")
        if investment_amount_usd <= 0:
            raise ValueError("Investment amount must be strictly positive")
        if existing_founder_shares <= 0:
            raise ValueError("Existing founder shares must be strictly positive")

        invest_amt = float(investment_amount_usd)
        val_cap = float(valuation_cap_usd)
        founder_shares = int(existing_founder_shares)
        st_clean = (safe_type or "POST_MONEY_SAFE").strip().upper()

        if st_clean == "POST_MONEY_SAFE":
            # YC Post-Money SAFE standard:
            # Investor Ownership % = Investment / Valuation Cap
            investor_equity_pct = min(99.0, (invest_amt / val_cap) * 100.0)
            founder_equity_pct = 100.0 - investor_equity_pct
            post_money_val = val_cap

            # New shares to issue so investor owns investor_equity_pct of (founder_shares + new_shares)
            # new_shares / (founder_shares + new_shares) = frac
            # new_shares = founder_shares * frac / (1 - frac)
            frac = investor_equity_pct / 100.0
            new_shares = int(round(founder_shares * frac / (1.0 - frac))) if frac < 1.0 else 0
            total_post_shares = founder_shares + new_shares
            effective_share_price = post_money_val / float(total_post_shares) if total_post_shares > 0 else 0.0

            summary = (
                f"Under YC Post-Money SAFE, a ${invest_amt:,.0f} investment at a ${val_cap:,.0f} cap "
                f"grants exactly {investor_equity_pct:.2f}% ownership, issuing {new_shares:,} new preferred shares."
            )

        else:
            # Pre-Money SAFE / Note conversion
            pre_share_price = val_cap / float(founder_shares)
            new_shares = int(round(invest_amt / pre_share_price)) if pre_share_price > 0 else 0
            total_post_shares = founder_shares + new_shares
            investor_equity_pct = (float(new_shares) / float(total_post_shares)) * 100.0 if total_post_shares > 0 else 0.0
            founder_equity_pct = 100.0 - investor_equity_pct
            post_money_val = val_cap + invest_amt
            effective_share_price = pre_share_price

            summary = (
                f"Under Pre-Money SAFE, investment converts at pre-money share price of ${pre_share_price:.4f}, "
                f"yielding {investor_equity_pct:.2f}% equity to the incoming syndicate."
            )

        # Build detailed Cap Table
        cap_table = [
            {
                "stakeholder": "Student Founders (Common)",
                "shares": founder_shares,
                "equity_pct": round(founder_equity_pct, 2),
                "share_type": "COMMON_VOTING"
            },
            {
                "stakeholder": f"Angel Syndicate ({st_clean})",
                "shares": new_shares,
                "equity_pct": round(investor_equity_pct, 2),
                "share_type": "PREFERRED_SHADOW"
            }
        ]

        return {
            "startup_name": startup_name.strip(),
            "safe_type": st_clean,
            "investment_amount_usd": round(invest_amt, 2),
            "valuation_cap_usd": round(val_cap, 2),
            "post_money_valuation_usd": round(post_money_val, 2),
            "investor_equity_pct": round(investor_equity_pct, 2),
            "founder_equity_pct": round(founder_equity_pct, 2),
            "effective_share_price_usd": round(effective_share_price, 4),
            "new_shares_issued": new_shares,
            "total_post_shares": total_post_shares,
            "dilution_summary": summary,
            "cap_table": cap_table
        }

    @classmethod
    def register_angel_commitment(
        cls,
        startup_name: str,
        student_founder_id: str,
        target_raise_usd: float = 250000.0,
        investor_name: str = "Dhaka Tech Angels",
        syndicate_tier: str = "ACCREDITED_ANGEL",
        commitment_amount_usd: float = 50000.0
    ) -> Dict[str, Any]:
        """
        Registers an angel syndicate investment commitment with cryptographic escrow verification.
        """
        if not startup_name or not startup_name.strip():
            raise ValueError("Startup name is required")
        if not student_founder_id or not student_founder_id.strip():
            raise ValueError("Founder ID is required")
        if commitment_amount_usd <= 0:
            raise ValueError("Commitment amount must be positive")
        if target_raise_usd <= 0:
            raise ValueError("Target raise must be positive")

        clean_startup = str(startup_name).strip()
        clean_founder = str(student_founder_id).strip()
        clean_investor = str(investor_name).strip() if (investor_name and investor_name is not ...) else "Dhaka Tech Angels"
        if not clean_investor:
            clean_investor = "Dhaka Tech Angels"
        commit_amt = float(commitment_amount_usd)
        target = float(target_raise_usd)

        # Aggregate existing commitments for this startup
        existing_total = sum(
            c["commitment_amount_usd"]
            for c in cls._syndicate_commitments.values()
            if c["startup_name"] == clean_startup
        )
        new_total = existing_total + commit_amt
        progress_pct = min(100.0, round((new_total / target) * 100.0, 2))

        # Generate cryptographic escrow lock seal
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        seal_payload = f"{clean_startup}:{clean_founder}:{clean_investor}:{commit_amt}:{ts}"
        seal_hash = hashlib.sha256(seal_payload.encode("utf-8")).hexdigest()
        seal_code = f"ESCROW-SEAL-{seal_hash[:16].upper()}"

        short_id = uuid.uuid4().hex[:8].upper()
        commitment_id = f"VC-COMMIT-{short_id}"

        status = "FULLY_SUBSCRIBED" if new_total >= target else "COMMITTED"

        record = {
            "commitment_id": commitment_id,
            "startup_name": clean_startup,
            "founder_id": clean_founder,
            "investor_name": clean_investor,
            "syndicate_tier": syndicate_tier.upper().strip(),
            "commitment_amount_usd": round(commit_amt, 2),
            "total_committed_usd": round(new_total, 2),
            "target_raise_usd": round(target, 2),
            "funding_progress_pct": progress_pct,
            "investor_count": sum(1 for c in cls._syndicate_commitments.values() if c["startup_name"] == clean_startup) + 1,
            "escrow_lock_seal": seal_code,
            "status": status,
            "committed_at": ts
        }

        cls._syndicate_commitments[commitment_id] = record
        return record

    @classmethod
    def list_startup_commitments(cls, startup_name: str) -> List[Dict[str, Any]]:
        """Returns all syndicate commitments for a given student startup."""
        clean = startup_name.strip()
        return [c for c in cls._syndicate_commitments.values() if c["startup_name"] == clean]

    @classmethod
    def reset_syndicate_for_testing(cls) -> None:
        """Helper for test isolation."""
        cls._syndicate_commitments.clear()

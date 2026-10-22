"""
High-Performance Computing (HPC) Parallel Job Scheduler Service.
Simulates Slurm-compatible Fair-Share workload management, GPU cluster allocation,
and Amdahl's / Gustafson's parallel scaling speedup dynamics for student AI research.
"""

import time
import uuid
from typing import Dict, Any, List, Optional


class HpcClusterSchedulerService:
    """
    HPC Supercomputer Cluster Scheduler and Parallel Scalability Modeling Engine.
    Simulates NVIDIA H100 / A100 GPU cluster allocations and Amdahl speedup limits.
    """

    # GPU Hardware Profiles (TFLOPS FP16 Tensor Core, VRAM in GB)
    GPU_PROFILES: Dict[str, Dict[str, Any]] = {
        "NVIDIA_H100": {
            "name": "NVIDIA H100 SXM5 80GB",
            "vram_per_gpu_gb": 80.0,
            "tflops_per_gpu": 989.0,
            "max_cluster_gpus": 128,
            "nodes_available": 16
        },
        "NVIDIA_A100": {
            "name": "NVIDIA A100 SXM4 80GB",
            "vram_per_gpu_gb": 80.0,
            "tflops_per_gpu": 312.0,
            "max_cluster_gpus": 128,
            "nodes_available": 32
        },
        "NVIDIA_L40S": {
            "name": "NVIDIA L40S PCIe 48GB",
            "vram_per_gpu_gb": 48.0,
            "tflops_per_gpu": 366.0,
            "max_cluster_gpus": 64,
            "nodes_available": 16
        }
    }

    _active_jobs_queue: List[Dict[str, Any]] = []

    @classmethod
    def calculate_amdahl_speedup(
        cls,
        parallel_fraction: float = 0.95,
        processor_counts: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Calculates theoretical Amdahl's Law (strong scaling) and Gustafson's Law (weak scaling)
        speedup and efficiency curves across processor/GPU counts.
        """
        p = max(0.0, min(0.9999, float(parallel_fraction)))
        serial_fraction = 1.0 - p

        # Theoretical maximum speedup limit as processors -> infinity: 1 / (1 - p)
        theoretical_max = 1.0 / serial_fraction if serial_fraction > 0 else 10000.0

        counts = processor_counts if processor_counts else [1, 2, 4, 8, 16, 32, 64, 128]

        speedup_curve: List[Dict[str, Any]] = []
        gustafson_curve: List[Dict[str, Any]] = []
        efficiency_curve: List[Dict[str, Any]] = []

        for n in counts:
            proc = max(1, int(n))

            # Amdahl's Law: S(n) = 1 / ((1 - p) + (p / n))
            denom = serial_fraction + (p / float(proc))
            amdahl_speedup = 1.0 / denom if denom > 0 else 1.0

            # Gustafson's Law: S_G(n) = n - (1 - p) * (n - 1)
            gustafson_speedup = float(proc) - (serial_fraction * (float(proc) - 1.0))

            # Parallel Efficiency: S(n) / n * 100%
            efficiency = (amdahl_speedup / float(proc)) * 100.0

            speedup_curve.append({
                "processors": proc,
                "speedup": round(amdahl_speedup, 3)
            })

            gustafson_curve.append({
                "processors": proc,
                "scaled_speedup": round(gustafson_speedup, 3)
            })

            efficiency_curve.append({
                "processors": proc,
                "efficiency_pct": round(efficiency, 2)
            })

        return {
            "parallel_fraction": round(p, 4),
            "serial_fraction": round(serial_fraction, 4),
            "theoretical_max_speedup": round(theoretical_max, 2),
            "speedup_curve": speedup_curve,
            "gustafson_scaled_speedup": gustafson_curve,
            "efficiency_curve": efficiency_curve
        }

    @classmethod
    def submit_hpc_job(
        cls,
        job_name: str,
        student_id: str,
        gpu_type: str = "NVIDIA_H100",
        gpu_count: int = 4,
        vram_gb_requested: float = 320.0,
        walltime_minutes: int = 120,
        parallel_fraction: float = 0.92
    ) -> Dict[str, Any]:
        """
        Submits and schedules a distributed parallel research compute job.
        Computes Fair-Share queue priority, node allocation, and estimated wait.
        """
        if not job_name or not job_name.strip():
            raise ValueError("Job name is required for HPC submission")
        if not student_id or not student_id.strip():
            raise ValueError("Student ID is required for HPC submission")

        clean_gpu_type = gpu_type.upper().strip()
        profile = cls.GPU_PROFILES.get(clean_gpu_type, cls.GPU_PROFILES["NVIDIA_H100"])

        gpus = max(1, min(profile["max_cluster_gpus"], int(gpu_count)))
        walltime = max(5, min(1440, int(walltime_minutes)))
        p_frac = max(0.01, min(0.99, float(parallel_fraction)))

        # VRAM validation
        max_available_vram = gpus * profile["vram_per_gpu_gb"]
        requested_vram = min(max_available_vram, max(1.0, float(vram_gb_requested)))

        # Nodes needed (assuming standard 8 GPUs per node)
        gpus_per_node = 8 if clean_gpu_type == "NVIDIA_H100" else 4
        nodes_needed = max(1, (gpus + gpus_per_node - 1) // gpus_per_node)

        # Total compute TFLOPS
        total_tflops = gpus * profile["tflops_per_gpu"]

        # Slurm-style multi-factor priority score:
        # Base (100) + Age bonus + FairShare balance - resource size penalty
        queue_depth = len(cls._active_jobs_queue)
        wait_seconds = max(15, queue_depth * 45)
        priority_score = round(100.0 + (queue_depth * 10.0) - (gpus * 1.5) + (p_frac * 20.0), 2)

        short_id = uuid.uuid4().hex[:8].upper()
        job_id = f"HPC-JOB-{short_id}"
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        job_record = {
            "job_id": job_id,
            "job_name": job_name.strip(),
            "student_id": student_id.strip(),
            "gpu_type": clean_gpu_type,
            "gpu_count": gpus,
            "allocated_nodes": nodes_needed,
            "allocated_vram_gb": round(requested_vram, 1),
            "tflops_allocated": round(total_tflops, 1),
            "walltime_minutes": walltime,
            "parallel_fraction": round(p_frac, 3),
            "priority_score": priority_score,
            "queue_state": "RUNNING" if queue_depth < 4 else "PENDING",
            "estimated_wait_seconds": wait_seconds if queue_depth >= 4 else 0,
            "submitted_at": timestamp
        }

        cls._active_jobs_queue.append(job_record)
        return job_record

    @classmethod
    def list_queue_jobs(cls) -> List[Dict[str, Any]]:
        """Returns all scheduled and running HPC jobs."""
        return list(cls._active_jobs_queue)

    @classmethod
    def get_cluster_status(cls) -> Dict[str, Any]:
        """Returns overall HPC cluster resource utilization."""
        total_gpus = sum(p["max_cluster_gpus"] for p in cls.GPU_PROFILES.values())
        allocated_gpus = sum(j["gpu_count"] for j in cls._active_jobs_queue if j["queue_state"] == "RUNNING")
        total_tflops = sum(j["tflops_allocated"] for j in cls._active_jobs_queue if j["queue_state"] == "RUNNING")

        return {
            "cluster_name": "Agrojatra Supercomputing Pod 1 (BUET-CSE High-Density)",
            "total_cluster_gpus": total_gpus,
            "allocated_gpus": allocated_gpus,
            "available_gpus": max(0, total_gpus - allocated_gpus),
            "utilization_pct": round((allocated_gpus / float(total_gpus)) * 100.0, 1) if total_gpus > 0 else 0.0,
            "active_compute_tflops": round(total_tflops, 1),
            "active_jobs_count": len(cls._active_jobs_queue)
        }

    @classmethod
    def reset_queue_for_testing(cls) -> None:
        """Helper for test isolation."""
        cls._active_jobs_queue.clear()

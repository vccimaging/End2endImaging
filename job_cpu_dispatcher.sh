#!/bin/bash
#SBATCH -N 1
#SBATCH --partition=batch
#SBATCH -J LensDispatcher
#SBATCH -o logs/LensDispatcher.%J.out
#SBATCH -e logs/LensDispatcher.%J.err
#SBATCH --mail-user=xinge.yang@kaust.edu.sa
#SBATCH --mail-type=ALL
#SBATCH --time=7-00:00:00
#SBATCH --mem=4G

# ── Configuration ────────────────────────────────────────────────────────────
MAX_CONCURRENT=24       # Max simultaneous GPU jobs
TOTAL_JOBS=100          # Total experiments to run
SUBMIT_INTERVAL=300     # Seconds between checks (5 min)
JOB_SCRIPT="job_gpu_lens_design.sh"
JOB_NAME="LensDesign"
# ─────────────────────────────────────────────────────────────────────────────

mkdir -p logs

SUBMITTED=0

echo "=== Lens Design Dispatcher ==="
echo "Max concurrent: ${MAX_CONCURRENT}"
echo "Total jobs: ${TOTAL_JOBS}"
echo "Check interval: ${SUBMIT_INTERVAL}s"
echo "Started at: $(date)"
echo "=============================="

# Submit loop
while [ ${SUBMITTED} -lt ${TOTAL_JOBS} ]; do
    # Count running + pending jobs with our job name
    ACTIVE=$(squeue -u "$USER" -n "${JOB_NAME}" -h 2>/dev/null | wc -l)

    SLOTS=$((MAX_CONCURRENT - ACTIVE))
    REMAINING=$((TOTAL_JOBS - SUBMITTED))

    if [ ${SLOTS} -gt 0 ]; then
        # Submit up to SLOTS new jobs, but not more than remaining
        TO_SUBMIT=${SLOTS}
        if [ ${TO_SUBMIT} -gt ${REMAINING} ]; then
            TO_SUBMIT=${REMAINING}
        fi

        for i in $(seq 1 ${TO_SUBMIT}); do
            JOB_ID=$(sbatch "${JOB_SCRIPT}" 2>&1 | awk '{print $4}')
            SUBMITTED=$((SUBMITTED + 1))
            echo "[$(date +%H:%M:%S)] Submitted job ${JOB_ID} (${SUBMITTED}/${TOTAL_JOBS})"
        done
    fi

    echo "[$(date +%H:%M:%S)] Active: ${ACTIVE}, Submitted: ${SUBMITTED}/${TOTAL_JOBS}"

    # If all submitted, break
    if [ ${SUBMITTED} -ge ${TOTAL_JOBS} ]; then
        break
    fi

    sleep ${SUBMIT_INTERVAL}
done

# Wait for all jobs to complete
echo "=== All ${TOTAL_JOBS} jobs submitted. Waiting for completion... ==="
while true; do
    ACTIVE=$(squeue -u "$USER" -n "${JOB_NAME}" -h 2>/dev/null | wc -l)
    if [ ${ACTIVE} -eq 0 ]; then
        echo "=== All jobs completed at $(date) ==="
        break
    fi
    echo "[$(date +%H:%M:%S)] Waiting... ${ACTIVE} jobs still running"
    sleep ${SUBMIT_INTERVAL}
done

#!/bin/bash
# slurm_job_tracker.sh
# Usage:
#   ./slurm_job_tracker.sh save              # Save current jobs with timestamp
#   ./slurm_job_tracker.sh check             # Check latest saved jobs
#   ./slurm_job_tracker.sh check <idfile>    # Check specific saved jobs

LOGDIR="$HOME/slurm_job_logs"
mkdir -p "$LOGDIR"

save_jobs() {
    timestamp=$(date "+%Y-%m-%d_%H-%M-%S")
    logfile="$LOGDIR/slurm_jobs_$timestamp.log"
    idfile="$LOGDIR/slurm_jobs_$timestamp.ids"

    echo "=== Saved at $(date "+%Y-%m-%d %H:%M:%S") ===" > "$logfile"
    squeue -u "$USER" -o "%.18i %.20j %.8T" >> "$logfile"
    echo "" >> "$logfile"

    # Save only job IDs to .ids file
    squeue -u "$USER" -h -o "%.18i" | sort -u > "$idfile"

    echo "Jobs saved to: $logfile"
    echo "Job IDs saved to: $idfile"
}

check_jobs() {
    idfile="$1"

    # If no file specified, pick the latest .ids file
    if [[ -z "$idfile" ]]; then
        idfile=$(ls -1t "$LOGDIR"/slurm_jobs_*.ids 2>/dev/null | head -n 1)
        if [[ -z "$idfile" ]]; then
            echo "No saved job IDs found. Run '$0 save' first."
            exit 1
        fi
        echo "No ID file specified, using latest: $idfile"
    fi

    if [[ ! -f "$idfile" ]]; then
        echo "Job ID file not found: $idfile"
        exit 1
    fi

    # Create a new status log
    timestamp=$(date "+%Y-%m-%d_%H-%M-%S")
    status_log="$LOGDIR/status_$(basename "$idfile" .ids)_$timestamp.log"

    echo "=== Checking jobs from $idfile at $(date "+%Y-%m-%d %H:%M:%S") ===" > "$status_log"

    while read -r jobid; do
        [[ -z "$jobid" ]] && continue

        # First check sacct (finished jobs)
        info=$(sacct -j "$jobid" --format=JobID,JobName,State,Elapsed,ExitCode --parsable2 --noheader | grep -w "$jobid" | head -n 1)
        if [[ -n "$info" ]]; then
            jid=$(echo "$info" | cut -d"|" -f1)
            jname=$(echo "$info" | cut -d"|" -f2)
            state=$(echo "$info" | cut -d"|" -f3)
            elapsed=$(echo "$info" | cut -d"|" -f4)
            exitcode=$(echo "$info" | cut -d"|" -f5)

            if [[ "$state" == "COMPLETED" ]]; then
                echo "Job $jid ($jname): COMPLETED ✅ | Runtime: $elapsed | ExitCode: $exitcode" >> "$status_log"
            elif [[ "$state" == "FAILED" || "$state" == "CANCELLED" || "$state" == "TIMEOUT" ]]; then
                echo "Job $jid ($jname): $state ❌ | Runtime: $elapsed | ExitCode: $exitcode" >> "$status_log"
            else
                echo "Job $jid ($jname): $state ⏳ | Runtime: $elapsed | ExitCode: $exitcode" >> "$status_log"
            fi
        else
            # If not in sacct, maybe still running → check squeue
            sq=$(squeue -j "$jobid" -o "%.18i %.20j %.8T" -h)
            if [[ -n "$sq" ]]; then
                jid=$(echo "$sq" | awk '{print $1}')
                jname=$(echo "$sq" | awk '{print $2}')
                state=$(echo "$sq" | awk '{print $3}')
                echo "Job $jid ($jname): $state ⏳ (still active)" >> "$status_log"
            else
                echo "Job $jobid: UNKNOWN (may be purged or not in accounting)" >> "$status_log"
            fi
        fi
    done < "$idfile"

    # Update symlink to always point to the latest status log
    ln -sf "$status_log" "$LOGDIR/latest_status.log"

    echo "Status written to: $status_log"
    echo "Symlink updated:   $LOGDIR/latest_status.log"
    cat "$status_log"
}

case "$1" in
    save)
        save_jobs
        ;;
    check)
        check_jobs "$2"
        ;;
    *)
        echo "Usage: $0 {save|check [idfile]}"
        ;;
esac


#ALTER SUBSET OF JOBS/FILES FOR RESUBMISSION 
import os
import subprocess
list = [16,23]
for i in list:
    os.chdir(f"dist_{i}")
    with open("amber.sh", "r+") as f:
        file_contents = f.read()
        updated_contents = file_contents.replace(f'prod_{i}.rst', f'prod_{i}_2.rst').replace(f'fram{i}.rst', f'prod_{i}.rst' )
    with open("amber.sh", "w") as file:
        file.write(updated_contents)
    os.chdir("../")

#CANCEL SUBSET OF JOBS
import subprocess

def scancel_jobs(job_ids):
    for job_id in job_ids:
        command = f"scancel {job_id}"
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Successfully cancelled job {job_id}: {result.stdout.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to cancel job {job_id}: {e.stderr.decode('utf-8')}")

if __name__ == "__main__":
    job_ids = range(339931, 339951)  # Job IDs
    scancel_jobs(job_ids)


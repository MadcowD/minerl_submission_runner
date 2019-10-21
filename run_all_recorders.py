import os
import subprocess

from constants import SUBMISSION_IDS
EXECUTION_COMMAND = "NV_GPU=0 python3 launch.py {submission_id}"

if __name__ == "__main__":
    print("hello")
    for id_ in SUBMISSION_IDS:
        try:
            subprocess.check_output(
                EXECUTION_COMMAND.format(
                    submission_id=id_
                ), shell=True, executable='/bin/bash'
            )
        except:
            pass
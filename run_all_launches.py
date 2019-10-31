import os
import subprocess
import time


from constants import SUBMISSION_IDS, J, E, get_submission_dir
EXECUTION_COMMAND = "NV_GPU=0 python3 launch.py {submission_id}"

if __name__ == "__main__":
    for id_ in SUBMISSION_IDS:
        # try:

            docker_file_dir = get_submission_dir(id_)
            recording_dir = J(docker_file_dir, 'recordings')
            ep_9_dir = J(recording_dir, 'MineRLObtainDiamond-v0', 'ep_9')
            # print(recording_dir)
            if E(ep_9_dir):
                continue     
            

            process = subprocess.Popen(
                EXECUTION_COMMAND.format(
                    submission_id=id_
                ), shell=True, executable='/bin/bash'
            )


            should_stop = False
            while not should_stop:
                # check if the process has created ep_9
                # first get the docker_file_dir
                if E(ep_9_dir):
                    should_stop = True
                    process.terminate()
                    continue
                time.sleep(10)


        # except:
            # pass

        
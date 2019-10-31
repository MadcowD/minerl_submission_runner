import os
import subprocess
import itertools
from joblib import Parallel, delayed

from constants import SUBMISSION_IDS, J, E, get_recording_dir, BUILD_DIR


def run(submission_id, ep):
    subprocess.run(['python3', 'render_trajectory.py', BUILD_DIR, submission_id, ep])

if __name__ == '__main__':


    jobs = sum([
        [ 
            (str(_id), ep.split("_")[-1]) for ep in os.listdir(get_recording_dir(_id))
        ] for _id in SUBMISSION_IDS if E(get_recording_dir(_id))
    ], [])

    
#    run(*jobs[0])
    Parallel(32)(delayed(run)(*x) for x in jobs)

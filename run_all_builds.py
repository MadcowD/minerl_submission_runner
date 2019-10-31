import os
import subprocess
from joblib import Parallel, delayed

from constants import SUBMISSION_IDS


def run(submission_id):
    subprocess.run(['python3', 'build.py', '--overwrite', str(submission_id)])

if __name__ == '__main__':
    Parallel(32)(delayed(run)(submission_id) for submission_id in SUBMISSION_IDS)
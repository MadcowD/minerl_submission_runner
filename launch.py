import os
import subprocess
import argparse
import shutil


from constants import BUILD_DIR, TEMPLATE_DIR, SUBMISSION_ID_PLACEHOLDER, J, E, get_submission_dir


COMMAND_STR = """xhost +local:root
nvidia-docker run  \\
    --env="DISPLAY" \\
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \\
    --volume="{recording_dir}:/minerl/recording:rw" \\
                {submission_id}
"""


def parse_args():
    opts = argparse.ArgumentParser(
        description='A script for running competitor docker images.'
    )

    opts.add_argument('submission_id', type=str, help='The submission ID.')


    return opts.parse_args()


def create_recording_dirs(submission_id, overwrite=False):
    docker_file_dir = get_submission_dir(submission_id)
    recording_dir = J(docker_file_dir, 'recordings')

    if E(recording_dir):
        if overwrite:
            shutil.rmtree(recording_dir)
    else:
        os.makedirs(recording_dir)

    return recording_dir


def main():
    opts = parse_args()

    recording_dir = create_recording_dirs(opts.submission_id, False)


    subprocess.check_output(
        COMMAND_STR.format(
            submission_id=opts.submission_id,
            recording_dir=recording_dir
        ), shell=True, executable='/bin/bash'
    )








if __name__ == '__main__':
    main()
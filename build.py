import os
import subprocess
import argparse
import shutil



from constants import BUILD_DIR, TEMPLATE_DIR, SUBMISSION_ID_PLACEHOLDER, TAKEMEDOWN_COUNTRYROAD_FILES, get_submission_dir, J, E


def parse_args():
    opts = argparse.ArgumentParser(
        description='A script for building competitor docker images.'
    )

    opts.add_argument('submission_id', type=str, help='The submission ID.')
    opts.add_argument('--overwrite', action='store_true', help='Overwrite existing image.')
    opts.add_argument('--rm', action='store_true', help='Delete existing image')


    return opts.parse_args()



def make_dockerfile(submission_id, overwrite=False, rm=False):
    docker_file_dir =get_submission_dir(submission_id)

    if E(docker_file_dir):
        if overwrite or rm:
            shutil.rmtree(docker_file_dir)
        else:
            return docker_file_dir
    
    os.makedirs(docker_file_dir)
    
    # Create the docker file
    with open(J(TEMPLATE_DIR, 'Dockerfile'), 'r') as docker:
        dockerfile = docker.read()
        formatted_dockerfile = dockerfile.replace(
            SUBMISSION_ID_PLACEHOLDER, str(submission_id))

    with open(J(docker_file_dir, 'Dockerfile'), 'w') as docker:
        docker.write(formatted_dockerfile)

    # Copy the necessary files
    for f in TAKEMEDOWN_COUNTRYROAD_FILES:
        shutil.copy(f, docker_file_dir)


    return docker_file_dir


def build_docker_image(docker_file_dir, submission_id, rm=False):
    if not rm:
        subprocess.run(['docker', 'build', '-t', str(submission_id), docker_file_dir])
    else:
        subprocess.run(['docker', 'rm', str(submission_id)])

    
def main():
    opts = parse_args()
    
    dfile_dir = make_dockerfile(opts.submission_id, opts.overwrite, opts.rm)
    build_docker_image(dfile_dir, opts.submission_id, opts.rm)
    




if __name__ == '__main__':
    main()
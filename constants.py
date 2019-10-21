
import os

J = os.path.join
E = os.path.exists

BUILD_DIR = os.path.abspath(J('.', 'builds'))
TEMPLATE_DIR = os.path.abspath('.')
SUBMISSION_ID_PLACEHOLDER = '%%%SUBMISSION_ID%%%'

get_submission_dir =  lambda x: J(BUILD_DIR, str(x)) 

SUBMISSION_IDS = [
    19482,
    18764,
    18759,
    18760,
    19311,
    19282,
    18758,
    20380,
    19295,
    18849
]


TAKEMEDOWN_COUNTRYROAD_FILES = [
    J(TEMPLATE_DIR, '10_nvidia.json'),
    J(TEMPLATE_DIR, 'minerl-0.2.9recording.tar.gz'),
    J(TEMPLATE_DIR, 'recorder.sh'),
    J(TEMPLATE_DIR, 'entrypoint_user.sh')
]
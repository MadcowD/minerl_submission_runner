import argparse
import logging
import random
import coloredlogs
import os
import time
import json
import numpy as np
import urllib
import tqdm
from joblib import Parallel, delayed
from PIL import Image

from minerl.viewer.trajectory_display_controller import TrajectoryDisplayController

coloredlogs.install(logging.DEBUG)
logger = logging.getLogger(__name__)


E = os.path.exists
J = os.path.join


def parse_args():

    parser = argparse.ArgumentParser("python3 render_recording.py")
    parser.add_argument("data_root", type=str, 
        help='The base where the submissions are stored. (Should contain folders of the form 11922, 123154, 234234')

    parser.add_argument("submission_id", type=str, 
        help='The base where the submissions are stored.')


    parser.add_argument("episode_num", type=str, 
        help='The base where the submissions are stored.')

    return parser.parse_args()


def get_information(submission_id):
    info = {}
    page = urllib.request.urlopen("https://www.aicrowd.com/challenges/neurips-2019-minerl-competition/submissions/{}".format(submission_id)).read().decode("utf-8")
    
    info['competitor_name'] = page.split("http://gitlab.aicrowd.com/")[1].split("/")[0]   
    info['git_url'] = (
        "http://gitlab.aicrowd.com/" + page.split("http://gitlab.aicrowd.com/")[1].split("</a>")[0]  )

    competitor_page = urllib.request.urlopen("https://www.aicrowd.com/participants/{}".format(info['competitor_name'].lower())).read().decode("utf-8")

    try:
        info['team_name'] =competitor_page.split('href="/teams/')[1].split(">")[0].split('</a>')[0][:-1]
    except:
        info['team_name'] = 'None'

    info['submission_id'] = submission_id
    return info

def main(opts):

    logger.info("Welcome to the MineRL episode viewer!")
    info = get_information(opts.submission_id)

    ep_folder = J(
        os.path.abspath(opts.data_root), 
        str(opts.submission_id),
        "recordings", 
        "MineRLObtainDiamond-v0",
        "ep_{}".format(opts.episode_num))

    # Construct the data frames
    logger.info("Loading data from {}".format(ep_folder))
    assert os.path.exists(ep_folder), "Episode folder not found!"
    
    # Load the obs, next obs, actions, and rewards.
    obs = np.load(J(ep_folder, 'states.npy'), allow_pickle=True)[:-1]
    next_obs = np.load(J(ep_folder, 'next_states.npy'), allow_pickle=True)
    rewards = np.load(J(ep_folder, 'rewards.npy'), allow_pickle=True)
    actions = np.load(J(ep_folder, 'actions.npy'), allow_pickle=True)

    
    data_frames = [
        (obs[i], 
        actions[i], 
        rewards[i], 
        next_obs[i], 
        i == len(obs), 
        {}) for i in range(len(obs))
    ]

    meta = data_frames[0][-1] 
    logger.info("Data loading complete!")

    logger.info(json.dumps(info, indent='\t'))

    header = info['team_name'] if info['team_name'] else info['competitor_name']
    header += " Submission #{}".format(opts.submission_id)



    trajectory_display_controller = TrajectoryDisplayController(
        data_frames, 
        header=header,
        subtext="Episode #{}".format(opts.episode_num),
        instructions="Submitted by:\n {}\n\n\n\n\n\nAction Visualization:".format(info['competitor_name'])
    )

    # Render out the information and the trajectory
    # out_dir = 
    # trajectory_display_controller.render(ep_folder)
    with open(J(ep_folder, 'info.json'), 'w') as f:
        json.dump(info, f, indent="\t")

    # from IPython import embed; embed()

if __name__ == '__main__':
    main(parse_args())
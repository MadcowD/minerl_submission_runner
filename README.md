# Submission Rendering

The submission renderer runs a participants submission by building a custom docker container that forces a modified version
of MineRL and then writes episode data to a mounted render directory. Thereafter, one can use the packaged renderer to
produce videos of the participants agents in minerl.viewer format.

## Requisites

To use the submission rendering toolkit, one must first install the following dependencies
1. ffmpeg
2. python3 w/pip
3. nvidia-docker

Then one needs to install the custom version of MineRL (used for rendering) on the base system:
```
pip3 uninstall minerl -y
pip3 install minerl-0.2.9recording.tar.gz
```

## Usage 
Now to build a submission one uses the following syntax
```
python3 build.py <submission_id>
```
! Important: Add the ``--overwrite`` option if you've updated the Dockerfile or the `recorder.sh`.


To launch a submission (make sure you are on a headed machine or have some xserver with display set!)
```
export DISPLAY=:<display num>
python3 launch.py <submission_id>
```
! Important: If you want to stop a submission from running **make sure to wait for it to reset FULLY for the next episode 
! as it does not write the recording out to a file until the episode is finished and the next reset fully returns.
! Further, stopping launch.py _does not_ kill the docker container. You will have to do this manually.


Once the submission is finished, you can now render a video.
! Important: Make sure you own the build directory (docker has some bad permissions!) 
! You can easily do this by `sudo chown -R user_name builds/`

To render, run the following command:
```
python3 render_trajectory.py ./builds/  <submission_id> <episode_number>
```
This will output an mp4 file in the recordings folder of the submission (contained under ./builds).

## Changing the Seed!
Currently the program is set up to only set the seed of the first episode to '17'. You can
seed any number of the episodes or change the first seed by modifying `recorder.sh` and rerunning `build.py`
with the `--overwrite` option. 

You can likewise change the number of episodes the evaluator will run in the `recorder.sh` file.

## Batch Jobs
To run batch jobs you can modify the `constants.py` with the submission IDS that you want to render and then 
use th corresponding aggregator scripts to each step above. Note: For some reason some submissions
fail to start and have an inference failed error. 

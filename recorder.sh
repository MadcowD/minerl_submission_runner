#!/bin/bash

export MINERL_RECORDING_PATH='/minerl/recording'
export MINERL_MAX_EVALUATION_EPISODES=10

set -e


AICROWD_DATA_ENABLED="NO"
EXTRAOUTPUT=""




# Run local name server
eval "pyro4-ns $EXTRAOUTPUT &"
trap "kill -11 $! > /dev/null 2>&1;" EXIT

# Run instance manager to generate performance report
export EVALUATION_STAGE='manager'
eval "python3 run.py --seeds 420691 4206969 420420 666666 666 666420 123321 456654 6006 60065 $EXTRAOUTPUT &"
trap "kill -11 $! > /dev/null 2>&1;" EXIT

# Run the evaluation
sleep 2
export MINERL_INSTANCE_MANAGER_REMOTE="1"
export EVALUATION_STAGE='testing'
export EVALUATION_RUNNING_ON='local'
export EXITED_SIGNAL_PATH='shared/exited'
rm -f $EXITED_SIGNAL_PATH
export ENABLE_AICROWD_JSON_OUTPUT='False'
eval "python3 run.py $EXTRAOUTPUT && touch $EXITED_SIGNAL_PATH || touch $EXITED_SIGNAL_PATH &"
trap "kill -11 $! > /dev/null 2>&1;" EXIT

# View the evaluation state
export ENABLE_AICROWD_JSON_OUTPUT='True'
python3 utility/parser.py || true
kill $(jobs -p)

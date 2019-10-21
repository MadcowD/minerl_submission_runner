#!/bin/sh

chown -R aicrowd:aicrowd /minerl/recording
exec runuser -u aicrowd "$@"
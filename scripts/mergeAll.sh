#!/bin/bash
for inputDir in "$@"; do
    submit_job.py condorMerge $(basename $inputDir)-merge --gigabytesPerJob 3 --useAFS --inputDirectory $inputDir
done

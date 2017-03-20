#!/bin/bash
for job in "$@"; do
    echo $job
    submit_job.py condorStatus --condorDirectories $job/*
done

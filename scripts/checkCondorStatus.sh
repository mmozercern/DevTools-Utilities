#!/bin/bash
for job in `condor_q "$USER" -format "%d." ClusterId -format "%d\n" ProcId -constraint "JobStatus==2"`; do
    echo $job
    condor_ssh_to_job $job "tail -1 _condor_stdout; tail -1 _condor_stderr"
done

#!/bin/bash
for dir in "$@"; do
    echo $dir
    cp $CMSSW_BASE/src/DevTools/Utilities/data/index.php $dir/index.php
done

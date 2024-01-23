#!/bin/bash

for t in `curl http://cmuflite.org/packed/flite-2.3/voices/us_voices`; do
    curl -o voices/flite/$t http://cmuflite.org/packed/flite-2.3/voices/$t
done
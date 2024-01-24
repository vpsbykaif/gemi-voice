#!/bin/bash

for t in `curl http://cmuflite.org/packed/flite-2.3/voices/us_voices`; do
    if [ ! -f voices/flite/$t ]; then
        curl -o voices/flite/$t http://cmuflite.org/packed/flite-2.3/voices/$t
    fi
done

mkdir tmp
curl -o tmp/vosk-model-en-in-0.5.zip https://alphacephei.com/vosk/models/vosk-model-en-in-0.5.zip

cd models
unzip -o ../tmp/vosk-model-en-in-0.5.zip

cd ..
rm -rf tmp
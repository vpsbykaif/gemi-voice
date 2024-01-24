#!/bin/bash

for t in `curl http://cmuflite.org/packed/flite-2.3/voices/us_voices`; do
    curl -o voices/flite/$t http://cmuflite.org/packed/flite-2.3/voices/$t
done

mkdir tmp
cd tmp

curl -O https://alphacephei.com/vosk/models/vosk-model-en-in-0.5.zip
unzip -o vosk-model-en-in-0.5.zip
mv vosk-model-en-in-0.5 models/vosk-model-en-in-0.5

cd ..
rm -rf tmp
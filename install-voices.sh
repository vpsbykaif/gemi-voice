#!/bin/bash

mkdir hts_tmp
cd hts_tmp/

curl -O http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_clb_arctic_hts-2.1.tar.bz2
curl -O http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_rms_arctic_hts-2.1.tar.bz2
curl -O http://hts.sp.nitech.ac.jp/archives/2.1/festvox_nitech_us_slt_arctic_hts-2.1.tar.bz2
curl -O http://hts.sp.nitech.ac.jp/archives/1.1.1/cmu_us_kal_com_hts.tar.gz
curl -O http://hts.sp.nitech.ac.jp/archives/1.1.1/cstr_us_ked_timit_hts.tar.gz

for t in `ls` ; do tar xvf $t ; done

ls lib/voices/us > ../voices.txt

mv lib/voices/us /usr/share/festival/voices/us
mv lib/hts.scm /usr/share/festival/hts.scm

cd ..
rm -rf hts_tmp

for t in `curl http://cmuflite.org/packed/flite-2.3/voices/us_voices`; do
    curl -O http://cmuflite.org/packed/flite-2.3/voices/$t
done
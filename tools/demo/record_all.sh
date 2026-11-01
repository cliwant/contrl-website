#!/bin/bash
set -e
OUT=/Users/junhocho/contrl-website/images/hero
cd "$(dirname "$0")"
for lang in ${LANGS:-en ko ja zh}; do
  PAGE=problem.html OUTNAME=problem_$lang LANG_CODE=$lang DURATION_MS=54000 node record_hd.js
  ffmpeg -v error -y -ss 0.3 -t 53.5 -i out_hd/problem_$lang.webm -vf "scale=1600:1000,fps=24,format=yuv420p" -c:v libx264 -preset slow -crf 24 -tune animation -movflags +faststart -an $OUT/problem-demo.$lang.mp4
  ffmpeg -v error -y -ss 27 -i out_hd/problem_$lang.webm -frames:v 1 -vf scale=1600:1000 $OUT/problem-demo.$lang.jpg
  PAGE=replay.html OUTNAME=replay_$lang LANG_CODE=$lang DURATION_MS=52000 node record_hd.js
  ffmpeg -v error -y -ss 0.8 -t 49 -i out_hd/replay_$lang.webm -vf "scale=1600:1000,fps=24,format=yuv420p" -c:v libx264 -preset slow -crf 27 -tune animation -movflags +faststart -an $OUT/contrl-demo.$lang.mp4
  ffmpeg -v error -y -ss 31 -i out_hd/replay_$lang.webm -frames:v 1 -vf scale=1600:1000 $OUT/contrl-demo.$lang.jpg
  echo "DONE $lang"
done
echo ALL_DONE

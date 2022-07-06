#!/bin/bash
for i in $(seq 1 50); do
  sed -i -E -e "s/random_seed=\".+\"/random_seed=\"$RANDOM\"/" flam.argos
  argos3 -c flam.argos
done

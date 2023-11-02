#!/bin/bash

instances=(17 20 21)

seeds=(65815233 220823810 278708881 283836340 371917356 378065218 551343601 552346062 608252726 914897360)

for i in "${instances[@]}"
do
    for j in "${seeds[@]}"
    do
      # filename
        python main.py $i $j >> problem_$((i + 1))_seed_${j}.txt
    done
done

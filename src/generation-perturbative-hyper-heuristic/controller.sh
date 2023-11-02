#!/bin/bash

instances=(4 7 8 11 12 14 15 16 17 20 21)

#Generate 50 random seeds between 1 and 999999999
seeds=($(shuf -i 1-999999999 -n 10))


# Loop through instance and loop through seeds and run Python script and write to file
for i in "${instances[@]}"
do
    for j in "${seeds[@]}"
    do
      # filename
        python main.py $i $j >> problem_$((i + 1))_seed_${j}.txt
    done
done

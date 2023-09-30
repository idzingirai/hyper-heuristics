#!/bin/bash

instances=(3 4 7 8 11 12 14 15 16 17 20 21)
seeds=(5778856 16223899 22878896 68625033 101006424 113139835 125838671 213232696 311489368 376423770)

# Loop through instance and loop through seeds and run Python script and write to file
for i in "${instances[@]}"
do
    for j in "${seeds[@]}"
    do
      # filename
        python main.py $i $j >> problem_$((i + 1))_seed_${j}.txt
    done
done

#!/bin/bash

#SBATCH --job-name=test
#SBATCH --output=/home/llama/res.txt
#SBATCH --ntasks=1
#SBATCH --time=10:00

sha1sum /home/llama/firecrest_input_file.txt

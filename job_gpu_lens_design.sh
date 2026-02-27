#!/bin/bash
#SBATCH -N 1
#SBATCH --partition=batch
#SBATCH -J LensDesign
#SBATCH -o logs/LensDesign.%J.out
#SBATCH -e logs/LensDesign.%J.err
#SBATCH --mail-user=xinge.yang@kaust.edu.sa
#SBATCH --mail-type=FAIL
#SBATCH --time=2:00:00
#SBATCH --mem=64G
#SBATCH --gres=gpu:1

mkdir -p logs

module load cuda
source activate deeplens

python batch_sample_and_run.py --category random

conda deactivate

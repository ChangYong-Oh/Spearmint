#!/bin/bash

srun python run_multiple_spearmint.py benchmarks/ branin_20 200 hartmann6_20 200
srun python run_multiple_spearmint.py benchmarks/ rosenbrock_20 200 levy_20 200

srun python run_multiple_spearmint.py benchmarks/ branin_50 400 hartmann6_50 400
srun python run_multiple_spearmint.py benchmarks/ rosenbrock_50 200 levy_50 400

srun python run_multiple_spearmint.py benchmarks/ branin_100 600 hartmann6_100 600
srun python run_multiple_spearmint.py benchmarks/ rosenbrock_100 600 levy_100 600
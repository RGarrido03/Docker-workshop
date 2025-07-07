#!/bin/bash

#SBATCH -p tuthpc
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1

module load udocker/1.3.17

# Run on coordination server
# module load udocker/1.3.17
# udocker pull python:3.13-alpine
# udocker create --name=python-test python:3.13-alpine

udocker run -v ~/Docker-workshop/udocker:/app python-test python3 /app/udocker.py
# udocker run python-test

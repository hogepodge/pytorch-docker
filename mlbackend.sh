#!/bin/bash

alias python=python3

label-studio-ml init /home/pytorch/backend --script /home/pytorch/work/model.py --force
mkdir /home/pytorch/data
cp /home/pytorch/work/data/* /home/pytorch/data/.
label-studio-ml start backend

#!/bin/bash

alias python=python3

label-studio-ml init /home/pytorch/backend --script /home/pytorch/work/model.py --force
label-studio-ml start backend

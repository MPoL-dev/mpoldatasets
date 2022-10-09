#!/bin/bash

qsub -A ipc5094_b_g_sc_default -l walltime=10:00:00 -l nodes=1:ppn=1 -l mem=20gb -I

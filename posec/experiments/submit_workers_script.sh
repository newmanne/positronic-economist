	#!/bin/bash
	#PBS -N PosEcWorkerCamera5
	#PBS -l walltime=720:00:00
	#PBS -l nodes=1:ppn=1
	#PBS -t 1-160
	#PBS -o PosEcWorker-o.txt
	#PBS -e PosEcWorker-e.txt

	if [[ -n "$PBS_O_WORKDIR" ]]; then
	    cd $PBS_O_WORKDIR
	fi

	. ~/.bashrc

	echo "Executing:"
    cd /ubc/cs/research/arrow/newmanne/positronic-economist/
    mkdir -p logs
    mkdir -p metrics
    mkdir -p baggs/GFP
    mkdir -p baggs/GSP
    mkdir -p baggs/VOTES
    python experiments.py --host paxos --port 8888 --qname posec --file metrics/${PBS_JOBNAME}.metrics --logfile camera_logs/${PBS_JOBNAME}.log 	

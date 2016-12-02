	#!/bin/bash
	#PBS -N GNMWorker
	#PBS -l walltime=720:00:00
	#PBS -l nodes=1:ppn=1
	#PBS -t 1-160
	#PBS -o GNMWorker-o.txt
	#PBS -e GNMWorker-e.txt

	if [[ -n "$PBS_O_WORKDIR" ]]; then
	    cd $PBS_O_WORKDIR
	fi

	. ~/.bashrc

	echo "Executing:"
    cd /ubc/cs/research/arrow/newmanne/positronic-economist/
    python gnm_worker.py

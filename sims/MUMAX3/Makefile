SHELL := /bin/bash

sims:
	for FOLDER in 1D 2D 3D ; \
	do \
		echo $${FOLDER} ; cd $${FOLDER} ; \
		for SIM in *.mx3 ; \
		do \
			SIMNAME="$${SIM%.mx3}" && \
			mumax3 $${SIM} ; \
			oommf avf2ovf -grid irreg \
			$${SIMNAME}.out/$${SIMNAME}.ovf $${SIMNAME}.ovf ; \
		done ; \
		cd .. ; \
	done;

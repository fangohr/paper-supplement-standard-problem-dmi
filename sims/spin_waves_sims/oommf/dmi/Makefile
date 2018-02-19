all:
	make relaxation
	make dynamics
	make data

relaxation:
	oommf boxsi -threads 4 OOMMF_static.mif; \
	mv InitialMagnetisation-Oxs*.omf InitialMagnetisation.omf;

dynamics:
	rm -rf omfs; \
	mkdir -p omfs; \
	oommf boxsi -threads 4 OOMMF_dynamics.mif; \

data:
	oommf avf2ovf -grid irreg \
	InitialMagnetisation.omf > InitialMagnetisation_ordered.omf; \
	python ../../data_libs/OOMMF_generate_data.py --omfs "omfs" \
	--initial_state "InitialMagnetisation_ordered.omf" \
	--Ms "0.86e6"; \

plots_squared:
	python ../../data_libs/process_data.py \
	--time_step 1e-12 \
	--vminf 1 --vmaxf 10 --ylim 0 30 \
	--scale power2 --pdf_name "spectra_squared"; \

plots_log:
	python ../../data_libs/process_data.py \
	--vminf 9 --vmaxf 1 --ylim 0 30 --xlim "-0.25" "0.25" \
	--time_step 1e-12 \
	--pdf_name "spectra_log10" \
	--get_data "spectra_log10"; \

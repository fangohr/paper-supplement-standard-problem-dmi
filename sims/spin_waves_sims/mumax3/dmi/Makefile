all:
	mumax3 spin_waves_simulation.mx3
	make convert_files
	make data
	make plots_log

convert_files:
	oommf avf2ovf -grid irreg \
	spin_waves_simulation.out/InitialState.ovf > InitialState.ovf ; \
	#
	mkdir -p ovfs
	for SNAP in spin_waves_simulation.out/m*.ovf; do \
		FILE=`basename $$SNAP`; \
		echo "Converting $$FILE"; \
		oommf avf2ovf -grid irreg \
		$$SNAP > ovfs/$$FILE ;\
	done;

data:
	python ../../data_libs/MUMAX_generate_data.py --ovfs "ovfs" \
	--initial_state "InitialState.ovf"

plots_log:
	python ../../data_libs/process_data.py \
		--vminf 9 --vmaxf 1 --ylim 0 30 --xlim "-0.25" "0.25" \
		--time_step 1e-12 \
		--pdf_name "spectra_log10" \
		--get_data "spectra_log10"

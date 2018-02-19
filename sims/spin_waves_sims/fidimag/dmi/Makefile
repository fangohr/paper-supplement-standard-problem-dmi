all:
	python sw_relaxation.py
	python sw_dynamics.py

generate_data:
	python ../../data_libs/Fidimag_generate_data.py \
		--initial_state initial_state.npy \
		--mesh_lengths 2000 200 1 \
		--mesh_discretisation 2 2 1 \
		--npys_path dynamics_npys;

process_data:
	python ../../data_libs/process_data.py \
		--out_name "" --m_i "x" \
		--vminf 9 --vmaxf 1 \
		--time_step "1e-12" \
		--xlim "-0.25" "0.25" --ylim "0" "30" \
		--scale "log10" --get_data "spectra_log10";

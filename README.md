# Modified Nodal Analysis Simulator
## Folder Structure: ##
1) **Ltspice_circuit_files:** Contains the .cir files of all the circuit design files simulated in the project.
2) **Ltspice_simulation_result_files:** Contains all the results from the LTSpice simulation tool.
3) **MNAS_simulation_result_files**: Contains all the results from the MNAS simulation tool.
4) **circuit_spice_netlist_files**: Contains the spice netlists of the corresponding circuit designs under consideration.

## Files: ##
1) **modified_nodal_analysis_simulator.py**: This is the main simulator file which takes in a circuit design file from _circuit_spice_netlist_folder_ and saves the output file in _MNAS_simulation result_files_.
2) **data_process_functions.py**: This file contains all the necessary functions to create the custom data sets required by the main file. The _data_collect_ function is a wrapper function that performs all the data processing and produces the final data set.
3) **result_analysis.py**: This file reads the necessary output files from the LTSpice tool and the MNAS simulator and compares the voltages across nodes and as an output gives a tuple of matching outputs and different outputs from corresponding output files. 

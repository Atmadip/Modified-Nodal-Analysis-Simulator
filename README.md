# Modified Nodal Analysis Simulator

This project aims to calculate the node voltages of a circuit spice netlist. 
The simulator uses the Modified Nodal Analysis approach implmenting the Matrix 
method of evaluation. The Gmatrix is an (n+m)x(n+m) matrix where n is the number
of nodes and m is the number of independant voltage sources. The upper nxn part 
of the matrix contains the equivalent conductance related to the 
corresponding i^th and j^th node where i and j can be same or different. 
The J_vector is a vector that has (n+m) elements where the n values represent the 
current sources if connected to the respective node. The m represents the voltage 
source values. 
Together the form the equation: 
         **_GV = J_**. The simulator performs nodal analysis and solves for the Vector V 
which is the list of Nodes. 
## Folder Structure: ##
1) **Ltspice_circuit_files:** Contains the .cir files of all the circuit design files simulated in the project.
2) **Ltspice_simulation_result_files:** Contains all the results from the LTSpice simulation tool.
3) **MNAS_simulation_result_files**: Contains all the results from the MNAS simulation tool.
4) **circuit_spice_netlist_files**: Contains the spice netlists of the corresponding circuit designs under consideration.

## Files: ##
1) **modified_nodal_analysis_simulator.py**: This is the main simulator file which takes in a circuit design file from _circuit_spice_netlist_folder_ and saves the output file in _MNAS_simulation result_files_.
2) **data_process_functions.py**: This file contains all the necessary functions to create the custom data sets required by the main file. The _data_collect_ function is a wrapper function that performs all the data processing and produces the final data set.
3) **result_analysis.py**: This file reads the necessary output files from the LTSpice tool and the MNAS simulator and compares the voltages across nodes and as an output gives a tuple of matching outputs and different outputs from corresponding output files. 

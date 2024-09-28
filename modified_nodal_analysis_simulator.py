import numpy as np
from scipy.sparse import coo_array, linalg
import data_process_functions as dp
import time
from pathlib import Path


class MNA_solver:
    def __init__(self, voltage_dict, resistance_dict, current_dict, node_to_node_connection, resistance_val):
        self.voltage_dict = voltage_dict
        self.resistance_dict = resistance_dict
        self.current_dict = current_dict
        self.node_list = list(resistance_dict.keys())
        self.voltage_list = list(voltage_dict.keys())
        self.node_to_node_connection = node_to_node_connection
        self.resistance_val = resistance_val
        self.node_list_length = len(self.node_list)
        self.voltage_list_length = len(self.voltage_list)
        self.merged_list = self.node_list + self.voltage_list
        self.merged_list_length = len(self.merged_list)

    def node_counter(self):
        return self.node_list_length

    def nodes(self):
        return self.node_list

    def g_matrix_row_counter(self):
        return self.merged_list_length

    def node_wise_resistance_counter(self, num_res):
        nodes = {}
        for key, val in self.resistance_dict.items():
            if len(val) == num_res:
                nodes[key] = val
        return nodes

    def element_eval(self, common_elements):
        res_val_list = []
        for i in common_elements:
            res_val_list.append(float(self.resistance_val[i]))
        reciprocal = np.reciprocal(res_val_list)
        cumulative_conductance = np.sum(reciprocal)
        return cumulative_conductance


    def node_index_gen(self):
        node_index = {}
        for i in range(len(self.node_list)):
            node_index[self.node_list[i]] = i
        return node_index

    def g_matrix_builder(self):

        rows = []
        cols = []
        data = []

        node_index_data = self.node_index_gen()

        # Calculating the diagonal values for conductance of respective nodes
        for i in range(len(self.node_list)):
            rows.append(i)
            cols.append(i)
            data.append(self.element_eval(self.resistance_dict[self.node_list[i]]))

        # Calculating Other entries for conductance of respective nodes
        for i in range(len(self.node_list)):
            n = self.node_to_node_connection[self.node_list[i]]
            for j in range(len(n["node"])):
                rows.append(i)
                cols.append(node_index_data[n["node"][j]])
                data.append(-np.reciprocal(float(n["edge"][j])))

        for i in range(len(self.voltage_list)):

            index = node_index_data[self.voltage_dict[self.voltage_list[i]]["pos_node"]]

            # voltage node values for the columns
            rows.append(index)
            cols.append(len(self.node_list) + i)
            data.append(1)

            # voltage node values for the rows
            rows.append(len(self.node_list) + i)
            cols.append(index)
            data.append(1)

        return coo_array((data, (rows, cols))).tocsc()


    def j_vector_builder(self):
        j_vector = []
        for v in range(self.merged_list_length):
            if self.merged_list[v] in self.current_dict:
                j_vector.append(self.current_dict[self.merged_list[v]])
            elif self.merged_list[v] in self.voltage_dict:
                j_vector.append(self.voltage_dict[self.merged_list[v]]["val"])
            else:
                j_vector.append(0.0)

        return j_vector


    def solver(self, output_file_name, output_file_folder):
        print("G_matrix building started.")
        a = self.g_matrix_builder()
        print("G_matrix building completed.")
        print("J_vector building started.")
        b = self.j_vector_builder()
        print("J_vector building completed.")
        result_vector = linalg.spsolve(a, b)
        node_voltage = []
        for i in range(self.node_list_length):
            data = str(self.node_list[i]) + ":" + str(round(result_vector[i], 5)) + "\n"
            node_voltage.append(data)
        output_file = output_file_name.split(".")[0] + "_MNAS.txt"
        # print(output_file)
        with open(output_file_folder+output_file, 'w') as f:
            f.writelines(node_voltage)
        f.close()
        print(f"{output_file} generated.")
        return node_voltage



if __name__ == '__main__':
    current_directory_path = str(Path.cwd())
    # print(current_directory_path)

    netlist_folder = "\circuit_spice_netlist_files\\"
    complete_source_path = current_directory_path + netlist_folder
    # print(complete_source_path)

    output_folder = "\MNAS_simulation_results_files\\"
    complete_destination_path = current_directory_path + output_folder
    # print(complete_destination_path)

    filename = "circuit11.sp"
    my_file = open(complete_source_path+filename, 'r')
    # print(my_file)

    voltage_dict_input, resistance_dict_input, current_dict_input, node_to_node_dict, resistance_val_input = dp.data_collect(my_file)

    MNAS_st = time.time()
    mnas_i = MNA_solver(voltage_dict_input, resistance_dict_input, current_dict_input, node_to_node_dict, resistance_val_input)
    res = mnas_i.solver(filename, complete_destination_path)
    MNAS_et = time.time()
    print('Execution time:', time.strftime("%H:%M:%S", time.gmtime(MNAS_et - MNAS_st)))

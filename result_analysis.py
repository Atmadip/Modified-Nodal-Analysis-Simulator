import os
from pathlib import Path
import re
import matplotlib.pyplot as plt


def file_finder(circuit_name):
    current_path = str(Path.cwd())
    path_to_ltspice_simulations = current_path + "\Ltspice_simulation_result_files"
    ltspice_file = circuit_name + "_LTSPICE.txt"
    ltspice_simulation_contents = [x for x in (os.listdir(path_to_ltspice_simulations)) if x == ltspice_file]
    path_to_mnas_simulations = current_path + "\MNAS_simulation_results_files"
    mnas_file = circuit_name + "_MNAS.txt"
    mnas_simulation_contents = [x for x in (os.listdir(path_to_mnas_simulations)) if x == mnas_file]
    if len(ltspice_simulation_contents) == 1 and len(mnas_simulation_contents) == 1:
        complete_ltspice_path = path_to_ltspice_simulations + "\\" + ltspice_file
        complete_mnas_path = path_to_mnas_simulations + "\\" + mnas_file
        return 1, complete_ltspice_path, complete_mnas_path
    elif len(ltspice_simulation_contents) == 1 and len(mnas_simulation_contents) == 0:
        return 0, 0, -1
    elif len(ltspice_simulation_contents) == 0 and len(mnas_simulation_contents) == 1:
        return 0, -1, 0
    else:
        return 0, 0, 0


def data_extract(ltspice_fp, mnas_fp):
    ltspice_dict = {}
    mnas_dict = {}
    with open(ltspice_fp, "r") as f:
        lines = f.readlines()
        for i in lines:
            if i[0] == "V":
                node = re.findall(r'V\((\w+)\):', i)[0]
                # print(node)
                val = float(re.findall(r'V\(\w+\):\s+([-+]?\d*\.\d+|\d+)', i)[0])
                # print(val)
                ltspice_dict[node] = val
    f.close()

    with open(mnas_fp, "r") as f:
        lines = f.readlines()
        for i in lines:
            val = i.split(":")
            mnas_dict[val[0]] = float(val[1])

    return ltspice_dict, mnas_dict


def data_compare(ltspice_dictionary, mnas_dictionary):
    nodes_l = list(ltspice_dictionary.keys())
    nodes_r = list(mnas_dictionary.keys())
    if len(nodes_l) == len(nodes_r):
        compare_list = [0 for j in range(len(nodes_l))]
        diff_vals = 0
        same_vals = 0
        for i in range(len(nodes_r)):
            if ltspice_dictionary[nodes_l[i]] == mnas_dictionary[nodes_l[i]]:
                compare_list[i] = 1
                same_vals += 1
            else:
                compare_list[i] = 0
                diff_vals += 1
    return compare_list, (same_vals, diff_vals)


def analysis(circuit_name):
    file_found, ltspice_path, mnas_path = file_finder(circuit)
    if file_found == 1:
        l_dict, m_dict = data_extract(ltspice_path, mnas_path)
        _, right_wrong_num = data_compare(l_dict, m_dict)
        scat_plot(l_dict, m_dict)
        return right_wrong_num
    elif file_found == 0:
        return ltspice_path, mnas_path


def scat_plot(spice_dict, mnas_dict):
    x = list(spice_dict.keys())
    l_spice_data = []
    mnas_data = []

    for i in x:
        l_spice_data.append(spice_dict[i])
        mnas_data.append(mnas_dict[i])
    plt.ylim(0.999*min(l_spice_data), 1.001*max(l_spice_data))
    plt.xlim(0.999*min(l_spice_data), 1.001*max(l_spice_data))
    colors = ['blue' if a == b else 'red' for a, b in zip(l_spice_data, mnas_data)]
    # symbol = ['o' if a == b else 'x' for a, b in zip(l_spice_data, mnas_data)]
    plt.xlabel('LTSpice Values')
    plt.ylabel('MNAS Values')
    plt.scatter(l_spice_data, mnas_data, c=colors, marker='x', s=20)
    plt.show()





if __name__ == '__main__':
    circuit = "circuit8"
    right_v_wrong_num = analysis(circuit)
    if sum(right_v_wrong_num) == 0:
        print(f"The simulation results of the design {circuit} were not found")
    elif sum(right_v_wrong_num) == -1:
        if right_v_wrong_num[0] == -1:
            print(f"Corresponding Ltspice simulation results for design {circuit} was not found.")
        elif right_v_wrong_num[1] == -1:
            print(f"Corresponding MNAS simulation results for design {circuit} was not found.")
    else:
        print(f"There are {sum(right_v_wrong_num)} nodes in the design.")
        print(f"Node-Voltage Comparison Result:\nCorrect:\t {right_v_wrong_num[0]}\nIncorrect:\t {right_v_wrong_num[1]}")





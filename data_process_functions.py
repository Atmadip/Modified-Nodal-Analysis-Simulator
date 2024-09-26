def component_divider(file_name):
    resistance_data = []
    voltage_data = []
    current_data = []
    lines = file_name.readlines()
    for line in lines:
        if line[0] == "R":
            resistance_data.append(list(line.strip().split(" ")))
        elif line[0] == "V":
            voltage_data.append(list(line.strip().split(" ")))
        elif line[0] == "I":
            current_data.append(list(line.strip().split(" ")))
    return resistance_data, voltage_data, current_data


def node_resistance_connectivity_generator(resistance_data):
    res_dict = {}
    for i in range(len(resistance_data)):
        if resistance_data[i][1] not in res_dict:
            res_dict[resistance_data[i][1]] = [resistance_data[i][0]]
        else:
            res_dict[resistance_data[i][1]].append(resistance_data[i][0])
    for i in range(len(resistance_data)):
        if resistance_data[i][2] not in res_dict:
            res_dict[resistance_data[i][2]] = [resistance_data[i][0]]
        else:
            res_dict[resistance_data[i][2]].append(resistance_data[i][0])
    return res_dict


def node_neighbour_data_gen(res_data):
    node_neighbour_dict = {}
    for i in range(len(res_data)):
        if res_data[i][1] not in node_neighbour_dict:
            node_neighbour_dict[res_data[i][1]] = {"node": [res_data[i][2]], "edge": [res_data[i][3]]}
        else:
            node_neighbour_dict[res_data[i][1]]["node"].append(res_data[i][2])
            node_neighbour_dict[res_data[i][1]]["edge"].append(res_data[i][3])

    for i in range(len(res_data)):
        if res_data[i][2] not in node_neighbour_dict:
            node_neighbour_dict[res_data[i][2]] = {"node": [res_data[i][1]], "edge": [res_data[i][3]]}
        else:
            node_neighbour_dict[res_data[i][2]]["node"].append(res_data[i][1])
            node_neighbour_dict[res_data[i][2]]["edge"].append(res_data[i][3])

    return node_neighbour_dict


def resistance_value_dict_generator(resistance_data):
    res_val = {}
    for i in range(len(resistance_data)):
        if resistance_data[i][0] not in res_val:
            res_val[resistance_data[i][0]] = float(resistance_data[i][-1])
    return res_val


def voltage_dict_generator(voltage_data):
    voltage_dict = {}
    for i in range(len(voltage_data)):
        if voltage_data[i][0] not in voltage_dict:
            voltage_dict[voltage_data[i][0]] = {"pos_node": voltage_data[i][1], "neg_node": voltage_data[i][2],
                                                'val': float(voltage_data[i][-1])}
    return voltage_dict


def current_dict_generator(current_data):
    current_dict = {}
    for i in range(len(current_data)):
        if current_data[i][1] not in current_dict:
            current_dict[current_data[i][1]] = 0 - float(current_data[i][-1])
    return current_dict


def data_collect(filename):
    resistance_data, voltage_data, current_data = component_divider(filename)
    node_neighbour_connect = node_neighbour_data_gen(resistance_data)
    voltage_dict = voltage_dict_generator(voltage_data)
    resistance_dict = node_resistance_connectivity_generator(resistance_data)
    current_dict = current_dict_generator(current_data)
    resistance_value = resistance_value_dict_generator(resistance_data)

    return voltage_dict, resistance_dict, current_dict, node_neighbour_connect, resistance_value

#
# def node_graph_dict(resistance_data, voltage_data):
#     node_graph = {}
#     for i in range(len(resistance_data)):
#         if resistance_data[i][1] not in node_graph:
#             node_graph[resistance_data[i][1]] = [resistance_data[i][3]]
#         else:
#             node_graph[resistance_data[i][1]].append(resistance_data[i][3])
#
#     for i in range(len(resistance_data)):
#         if resistance_data[i][2] not in node_graph:
#             node_graph[resistance_data[i][2]] = [resistance_data[i][3]]
#         else:
#             node_graph[resistance_data[i][2]].append(resistance_data[i][3])


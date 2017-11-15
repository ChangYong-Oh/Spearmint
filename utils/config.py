import sys
import json


def generate_json(func_name, ndim, filename):
	config_dict = dict()
	config_dict["language"] = "PYTHON"
	config_dict["main-file"] = func_name + ".py"
	config_dict["experiment-name"] = func_name + '_D' + str(ndim)
	config_dict["likelihood"] = "GAUSSIAN"

	variables_dict = dict()
	for i in range(1, ndim + 1):
		variable_name = 'x' + str(i)
		variable_info = dict()
		variable_info["type"] = "FLOAT"
		variable_info["size"] = 1
		variable_info["min"] = -1
		variable_info["max"] = 1
		variables_dict[variable_name] = variable_info

	config_dict["variables"] = variables_dict

	json_file = open(filename, 'w')
	json_file.write(json.dumps(config_dict, sort_keys=True, indent=4, separators=(',', ': ')))
	json_file.close()


if __name__ == '__main__':
	generate_json(sys.argv[1], int(sys.argv[2]), sys.argv[3])

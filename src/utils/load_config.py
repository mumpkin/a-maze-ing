from typing import Any
import sys


def decrypt_config_line(file: Any) -> list[Any]:
    """

    """
    line = file.readline()
    config_values = list()
    try:
        line_data = line.split(' ')[0].split()
        print(line_data)
        config_values = line_data[0].split('=')
    except Exception:
        print('All configs have been loaded')
    return config_values


def load_config() -> dict[str, Any]:
    """
    Parses the configuration file
    Returns a dict with every value and their respective keys
    """
    configs = dict()
    repo_rootpath = ''
    prefix_parts = sys.prefix.split('/')
    for i in range(len(prefix_parts) - 1):
        repo_rootpath += prefix_parts[i] + "/"
    try:
        with open(f"{repo_rootpath}config.txt", 'r') as file:
            config_values = decrypt_config_line(file)
            while len(config_values) == 2:
                configs.update({config_values[0]: config_values[1]})
                config_values = decrypt_config_line(file)
    except FileNotFoundError as fe:
        print(fe)
    configs['WIDTH'] = int(configs['WIDTH'])
    configs['HEIGHT'] = int(configs['HEIGHT'])
    configs['PERFECT'] = bool(configs['PERFECT'])
    return configs


if __name__ == '__main__':
    print(load_config())

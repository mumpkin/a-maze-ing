from enum import Enum


class ConfigKey(str, Enum):
    WIDTH = "width"
    HEIGHT = "height"
    ENTRY = "entry"
    EXIT = "exit"
    OUTPUT_FILE = "output_file"
    PERFECT = "perfect"
    SEED = "seed"

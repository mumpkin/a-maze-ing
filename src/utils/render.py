"Render module."

from globals import config

def _parse_line(line: str) -> None:
    pass

def render() -> None:
    with open(config.output_file, "r") as file:

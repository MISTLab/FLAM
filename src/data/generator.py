"""This program generates ground truth data for DBM-SMS.
The data is in JSON formats and represents radiation sources on a 2D grid.

The format is the following:
{"sources": [
    {"x": 0.5, "y": 2.1, "intensity": 0.75},
    {"x": 1.5, "y": 0.0, "intensity": 0.05}
]}
"""


import json
from random import uniform


NB_SOURCE_FILES = 10
NB_RADIATION_SOURCES = 2
MIN_MAP_X = -8
MAX_MAP_X = 8
MIN_MAP_Y = -8
MAX_MAP_Y = 8

def generate_source() -> dict:
    return {"x": uniform(MIN_MAP_X, MAX_MAP_X), "y": uniform(MIN_MAP_Y, MAX_MAP_Y), "intensity": uniform(0.2, 1.0)}


def main():
    for i in range(NB_SOURCE_FILES):
        with open(f"radiation_sources{i}.json", "w") as f:
            sources = {"sources": [generate_source() for _ in range(NB_RADIATION_SOURCES)]}
            json.dump(sources, f, indent=2)


if __name__ == "__main__":
    main()

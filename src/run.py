"""
This program's purpose is simply to run multiple ARGoS experiments in a headless way.
To do so, it is necessary to comment out the <visualization> section 
in the experiment file (./dora-mesh.argos).
"""


import subprocess


NB_RUNS = 10


def main() -> None:
    command = ["argos3 -c dora-mesh.argos"]
    for i in range(NB_RUNS):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        
        for line in process.stdout:
            print(line.decode())

        process.wait()
        print(f"Experiment #{i} finished with code {process.returncode}")


if __name__ == "__main__":
    main()

import csv
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


figures_folder = "figures"
topology = "average"
full_topology = "Average"
folders = [f"dora_mesh", f"hop_count", f"stigmergy"]
MAX_NB_STEPS = 500
NB_ROBOTS = 100
METRIC = ["storage", "reliability", "speed"]


def find_nb_run() -> int:
    with open(f"../results/results_grid/dora_mesh/concatenated_storage.csv", "r") as f1:
        last_line = f1.readlines()[-1]

    # return 3
    return int(last_line.split(",")[1]) + 1

def parse_mean_storage() -> np.ndarray:
    storage_capacity = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        names = [
            f"../results/results_grid/{folder_name}/concatenated_storage.csv",
            f"../results/results_lennard/{folder_name}/concatenated_storage.csv",
            f"../results/results_random/{folder_name}/concatenated_storage.csv",
            f"../results/results_scale/{folder_name}/concatenated_storage.csv"
        ]

        with open(names[0], "r") as res_grid, open(names[1], "r") as res_lj, open(names[2], "r") as res_random, open(names[3], "r") as res_scale:
            readers = [csv.reader(res) for res in [res_grid, res_lj, res_random, res_scale]]
            row_count = min(count_lines(n) for n in names)

            step = 0
            previous_step, previous_run = 0, 0
            step_storage_sum = 0
            for i in range(row_count):
                try:
                    lines = [next(r) for r in readers]
                except:
                    break

                run = int(lines[0][1])
                if run >= storage_capacity.shape[1]:
                    break
                step = int(lines[0][2])

                if step == previous_step and run == previous_run:
                    step_storage_sum += int(np.mean([int(lines[i][3]) for i in range(len(lines))]))
                elif step < MAX_NB_STEPS:
                    storage_capacity[folder_id, run, step - 1] = step_storage_sum
                    step_storage_sum = int(np.mean([int(lines[i][3]) for i in range(len(lines))]))
                
                previous_step, previous_run = step, run
                storage_capacity[folder_id, run, step] = step_storage_sum

    return storage_capacity

def count_lines(filename: str) -> int:
    with open(filename, "r") as f:
        return sum(1 for _ in f)

def parse_mean_reliability() -> np.ndarray:
    reliability = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        names = [f"../results/results_grid/{folder_name}/concatenated_reliability.csv", f"../results/results_lennard/{folder_name}/concatenated_reliability.csv", f"../results/results_random/{folder_name}/concatenated_reliability.csv", f"../results/results_scale/{folder_name}/concatenated_reliability.csv"]
        with open(names[0], "r") as res_grid, open(names[1], "r") as res_lj, open(names[2], "r") as res_random, open(names[3], "r") as res_scale:
            readers = [csv.reader(res) for res in [res_grid, res_lj, res_random, res_scale]]
            row_count = min(count_lines(n) for n in names)

            step = 0
            previous_step, previous_run = 0, 0
            created_sum = 0
            lost_sum = 0

            for i in range(row_count):
                try:
                    lines = [next(r) for r in readers]
                except:
                    break


                run = int(lines[0][1])
                if run >= reliability.shape[1]:
                    break
                step = int(lines[0][2])

                if step == previous_step and run == previous_run:
                    created_sum += int(np.mean([int(lines[i][3]) for i in range(len(lines))]))
                    lost_sum += int(np.mean([int(lines[i][4]) for i in range(len(lines))]))
                elif step < MAX_NB_STEPS:
                    reliability[folder_id, run, step - 1] = max((created_sum - lost_sum), 0) / created_sum if created_sum != 0 else 1
                    created_sum = int(np.mean([int(lines[i][3]) for i in range(len(lines))]))
                    lost_sum = int(np.mean([int(lines[i][4]) for i in range(len(lines))]))
                
                previous_step, previous_run = step, run
                reliability[folder_id, run, step] = max((created_sum - lost_sum), 0) / created_sum if created_sum != 0 else 1
                
    return reliability

def parse_storage() -> np.ndarray:
    storage_capacity = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))
    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_storage.csv", "r") as res:
            step = 0
            previous_step, previous_run = 0, 0
            step_storage_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                if run >= storage_capacity.shape[1]:
                    break
                step = int(line[2])

                if step == previous_step and run == previous_run and "stigmergy" not in folder_name:
                    step_storage_sum += int(line[3])
                elif step < MAX_NB_STEPS:
                        storage_capacity[folder_id, run, step - 1] = step_storage_sum
                        step_storage_sum = int(line[3])
                
                previous_step, previous_run = step, run
                storage_capacity[folder_id, run, step] = step_storage_sum


    return storage_capacity

def parse_avg_storage() -> np.ndarray:
    storage_avg = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))
    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_storage.csv", "r") as res:
            step = 0
            previous_step, previous_run = 0, 0
            step_storage_sum = 0
            storage_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                if run >= storage_avg.shape[1]:
                    break

                step = int(line[2])

                if int(line[0]) != 0:

                    if step == previous_step and run == previous_run:
                        step_storage_sum += int(line[3])
                    elif step < MAX_NB_STEPS:
                        storage_avg[folder_id, run, step - 1] = step_storage_sum / NB_ROBOTS
                        step_storage_sum = int(line[3])
                    
                    previous_step, previous_run = step, run
                    storage_avg[folder_id, run, step] = step_storage_sum / NB_ROBOTS

        print("AVG storage used = ", 2 * np.mean(storage_avg[folder_id, :, :]))
    return storage_avg

def parse_reliability():
    reliability = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_reliability.csv", "r") as res:
            step = 0
            previous_step, previous_run = 0, 0
            created_sum = 0
            lost_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                if run >= reliability.shape[1]:
                    break
                step = int(line[2])

                if step == previous_step and run == previous_run:
                    created_sum += int(line[3])
                    lost_sum += int(line[4])
                elif step < MAX_NB_STEPS:
                    reliability[folder_id, run, step - 1] = max((created_sum - lost_sum), 0) / created_sum if created_sum != 0 else 1
                    created_sum = int(line[3])
                    lost_sum = int(line[4])
                
                previous_step, previous_run = step, run
                reliability[folder_id, run, step] = max((created_sum - lost_sum), 0) / created_sum if created_sum != 0 else 1

    return reliability

def parse_data_lost():
    data_lost = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_reliability.csv", "r") as res:
            step = 0
            previous_step, previous_run = 0, 0
            lost_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                if run >= data_lost.shape[1]:
                    break

                step = int(line[2])

                if step == previous_step and run == previous_run:
                    lost_sum += int(line[4])
                elif step < MAX_NB_STEPS:
                    data_lost[folder_id, run, step - 1] = lost_sum
                    lost_sum = int(line[4])
                
                previous_step, previous_run = step, run
                data_lost[folder_id, run, step] = lost_sum

    return data_lost

def parse_speed():
    speed_dict = {}
    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        speed_dict[folder_id] = {}
        number_of_item = 0
        total_hops = 0
        with open(f"{folder_name}/0_speed.csv", "r") as res:
            reader = csv.reader(res)
            next(reader)
            for line in reader:
                speed = int(line[3]) - int(line[4])
                
                number_of_item += 1
                total_hops += speed

                if speed not in speed_dict[folder_id]:
                    speed_dict[folder_id][speed] = 1
                else:
                    speed_dict[folder_id][speed] += 1

        # print("Average hop = ", total_hops / number_of_item)

    return speed_dict


def parse_memory(data_lost: np.ndarray, storage: np.ndarray) -> np.ndarray:
    memory = {}

    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        memory[folder_id] = {}

        with open(f"{folder_name}/storage.csv", "r") as res:
            step = 0
            previous_step, previous_run = 0, 0
            lost_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                step = int(line[2])

                if step == previous_step and run == previous_run:
                    lost_sum += int(line[4])
                elif step < MAX_NB_STEPS:
                    data_lost[folder_id, run, step - 1] = lost_sum
                    lost_sum = int(line[4])
                
                previous_step, previous_run = step, run
                data_lost[folder_id, run, step] = lost_sum

                
def plot_single_metric(metric_data: np.ndarray, dependant_variable: str, metric: str, title: str) -> None:
    x_axis = np.arange(MAX_NB_STEPS)
    colors = ["cornflowerblue", "lightcoral","orchid", "steelblue", "crimson", "darkorchid"]

    fig = plt.figure()
    ax = fig.gca()

    for f in range(len(folders)):
        std = np.array([0.5 * np.nanstd(metric_data[f, :, i]) for i in range(MAX_NB_STEPS)])
        mean = np.mean(metric_data[f, :, :], axis=0)
        ax.scatter(x_axis, mean, c=colors[f], s = 10)
        ax.fill_between(x_axis, mean-std, mean+std, alpha=0.25, color=colors[f], label='_nolegend_')
    
    ax.set_xlabel("Step")
    ax.set_ylabel(dependant_variable)
    ax.legend(['RASS', 'Hop count', 'Stigmergy'])
    # ax.set_title(f"{title} for {full_topology} Topology")
    ax.set_title(f"Average {title}")

    plt.savefig(f"{figures_folder}/{topology}_{metric}.png", transparent=True)


def plot_speed_metric(metric_data: np.ndarray, dependant_variable: str, metric: str) -> None:
    colors = ["cornflowerblue", "lightcoral","orchid", "steelblue", "crimson", "darkorchid"]
    fig = plt.figure()

    for f in range(len(folders)):
        plt.bar(list(metric_data[f].keys()), np.array(list(metric_data[f].values())) / find_nb_run(), color=colors[f])

    ax = fig.gca()
    ax.set_xlabel("Transfer speed (step)")
    ax.set_ylabel(dependant_variable)
    ax.set_xlim([0,50])
    ax.set_title(f"Transfer Speeds for {full_topology} Topology")
    ax.legend(['RASS', 'Hop count'])
    plt.savefig(f"{figures_folder}/{topology}_{metric}.png", transparent=True)


def plot_metrics() -> None:
    reliability = parse_mean_reliability()
    # lost = parse_data_lost()
    storage = parse_mean_storage()

    #memory = parse_memory(lost, storage)
    # speed = parse_speed()
    plot_single_metric(reliability, "Retained data (%)", "reliability", "Reliability")
    # plot_single_metric(lost, "Amount of data lost", "lost_data", "Lost Data")
    plot_single_metric(storage, "Amount of data stored in the system", "storage", "Total Storage Capacity")
    # plot_single_metric(parse_avg_storage(), "Average amount of data stored on individual robots", "storage_individual.png")
    # plot_speed_metric(speed,"Number of data routed to base station", "speed")


def main() -> None:
    plot_metrics()


if __name__ == "__main__":
    main()

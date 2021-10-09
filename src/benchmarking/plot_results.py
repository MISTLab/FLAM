import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


figures_folder = "figures/"
folders = ["../results/physical_dora_mesh", "../results/physical_hop_count"]#, "../results/stigmergy"]#,"../results/results_grid_100/dora_mesh", "../results/results_grid_100/hop_count", "../results/results_grid_100/stigmergy"]
MAX_NB_STEPS = 2000
NB_ROBOTS = 5
METRIC = ["storage", "reliability", "speed"]


def find_nb_run() -> int:
    with open("../results/physical_dora_mesh/concatenated_storage.csv", "r") as f1:
        last_line = f1.readlines()[-1]

    return 3
    return int(last_line.split(",")[1]) + 1


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
                step = int(line[2])

                if run < 3:

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
                step = int(line[2])

                if run < 3 and int(line[0]) != 0:

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
                step = int(line[2])

                if run < 3:

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
                step = int(line[2])

                if run < 3:

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
        with open(f"{folder_name}/5_speed.csv", "r") as res:
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

        print("Average hop = ", total_hops / number_of_item)

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

                if run < 3:

                    if step == previous_step and run == previous_run:
                        lost_sum += int(line[4])
                    elif step < MAX_NB_STEPS:
                        data_lost[folder_id, run, step - 1] = lost_sum
                        lost_sum = int(line[4])
                    
                    previous_step, previous_run = step, run
                    data_lost[folder_id, run, step] = lost_sum

    return
    
                
def plot_single_metric(metric_data: np.ndarray, dependant_variable: str, file_name: str) -> None:
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
    plt.savefig(figures_folder + file_name)


def plot_speed_metric(metric_data: np.ndarray, dependant_variable: str, file_name: str) -> None:
    colors = ["cornflowerblue", "lightcoral","orchid", "steelblue", "crimson", "darkorchid"]
    fig = plt.figure()

    for f in range(len(folders)):
        plt.bar(list(metric_data[f].keys()), np.array(list(metric_data[f].values())) / find_nb_run(), color=colors[f])

    ax = fig.gca()
    ax.set_xlabel("Transfer speed (step)")
    ax.set_ylabel(dependant_variable)
    ax.set_xlim([0,50])
    ax.legend(['RASS', 'Hop count'])
    plt.savefig(figures_folder + file_name)


def plot_metrics() -> None:
    reliability = parse_reliability()
    lost = parse_data_lost()
    storage = parse_storage()

    #memory = parse_memory(lost, storage)
    speed = parse_speed()
    plot_single_metric(reliability, "Retained data (%)", "reliability.png")
    plot_single_metric(lost, "Amount of data lost", "lost_data.png")
    plot_single_metric(storage, "Amount of data stored in the system", "storage.png")
    # plot_single_metric(parse_avg_storage(), "Average amount of data stored on individual robots", "storage_individual.png")
    plot_speed_metric(speed,"Number of data routed to base station","speed.png")


def main() -> None:
    plot_metrics()


if __name__ == "__main__":
    main()

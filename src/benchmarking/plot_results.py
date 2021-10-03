import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


figures_folder = "figures/"
folders = ["../results/dora_mesh", "../results/hop_count"]
MAX_NB_STEPS = 500
METRIC = ["storage", "reliability", "speed"]


def find_nb_run() -> int:
    with open("../results/dora_mesh/concatenated_storage.csv", "r") as f1:
        last_line = f1.readlines()[-1]

    return int(last_line.split(",")[1]) + 1


def parse_storage() -> np.ndarray:
    storage_capacity = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))
    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_storage.csv", "r") as res:
            step = 0
            previous_step = 0
            step_storage_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                step = int(line[2])

                if step == previous_step:
                    step_storage_sum += int(line[3])
                else:
                    storage_capacity[folder_id, run, step - 1] = step_storage_sum
                    step_storage_sum = int(line[3])
                
                previous_step = step


            storage_capacity[folder_id, run, step:MAX_NB_STEPS] = step_storage_sum

    return storage_capacity

def parse_reliability():
    reliability = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_reliability.csv", "r") as res:
            step = 0
            created_sum = 0
            lost_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                step = int(line[2]) - 1
                created_sum += int(line[3])
                lost_sum += int(line[4])

                reliability[folder_id, run, step] = (created_sum - lost_sum) / created_sum if created_sum != 0 else 1


            reliability[folder_id, run, step:MAX_NB_STEPS] = reliability[folder_id, run, step]

    return reliability

def parse_data_lost():
    data_lost = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_reliability.csv", "r") as res:
            step = 0
            lost_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                step = int(line[2]) - 1
                lost_sum += int(line[4])

                data_lost[folder_id, run, step] = lost_sum


            data_lost[folder_id, run, step:MAX_NB_STEPS] = data_lost[folder_id, run, step]

    return data_lost

def parse_data_generated():
    data_generated = np.zeros((len(folders), find_nb_run(), MAX_NB_STEPS))

    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        with open(f"{folder_name}/concatenated_reliability.csv", "r") as res:
            step = 0
            generated_sum = 0
            for line in csv.reader(res):
                run = int(line[1])
                step = int(line[2]) - 1
                generated_sum += int(line[3])

                data_generated[folder_id, run, step] = generated_sum


            data_generated[folder_id, run, step:MAX_NB_STEPS] = data_generated[folder_id, run, step]

    return data_generated

def parse_speed():
    speed_dict = {}
    for folder_id, folder_name in enumerate(folders):
        print(f"---Processing {folder_name}---")
        speed_dict[folder_id] = {}
        with open(f"{folder_name}/0_speed.csv", "r") as res:
            reader = csv.reader(res)
            next(reader)
            for line in reader:
                speed = int(line[3]) - int(line[4])
                
                if speed not in speed_dict[folder_id]:
                    speed_dict[folder_id][speed] = 1
                else:
                    speed_dict[folder_id][speed] += 1

    return speed_dict
    
                
def plot_single_metric(metric_data: np.ndarray, dependant_variable: str, file_name: str) -> None:
    x_axis = np.arange(MAX_NB_STEPS)
    colors = ["lightcoral","orchid", "cornflowerblue"]

    fig = plt.figure()
    ax = fig.gca()

    for f in range(len(folders)):
        std = np.array([0.5 * np.nanstd(metric_data[f, :, i]) for i in range(MAX_NB_STEPS)])
        mean = metric_data[f, :, :].mean(0)
        ax.scatter(x_axis, mean, c=colors[f])
        ax.fill_between(x_axis, mean-std, mean+std, alpha=0.25, color=colors[f], label='_nolegend_')
    
    ax.set_xlabel("Step")
    ax.set_ylabel(dependant_variable)
    ax.legend(['DORA-Mesh', 'Hop-count', 'Stigmergy'])
    plt.savefig(figures_folder + file_name)


def plot_speed_metric(metric_data: np.ndarray, dependant_variable: str, file_name: str) -> None:
    colors = ["lightcoral","orchid", "cornflowerblue"]
    fig = plt.figure()

    for f in range(len(folders)):
        plt.bar(list(metric_data[f].keys()), metric_data[f].values(), color=colors[f])

    ax = fig.gca()
    ax.set_xlabel("Transfer speed (step)")
    ax.set_ylabel(dependant_variable)
    ax.legend(['DORA-Mesh', 'Hop-count', 'Stigmergy'])
    plt.savefig(figures_folder + file_name)


def plot_metrics() -> None:       
    plot_single_metric(parse_reliability(), "Retained data (%)", "reliability.png")
    plot_single_metric(parse_data_lost(), "Lost data", "lost_data.png")
    plot_single_metric(parse_data_generated(), "Generated data", "generated_data.png")
    plot_single_metric(parse_storage(), "Amount of data stored", "storage.png")
    plot_speed_metric(parse_speed(),"Number of data","speed.png")


def main() -> None:
    plot_metrics()


if __name__ == "__main__":
    main()

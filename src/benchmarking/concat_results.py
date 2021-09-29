import csv


FOLDER_RESULTS_DORA_MESH = "../results/dora_mesh"
FOLDER_RESULTS_HOP_COUNT = "../results/hop_count"
FOLDER_RESULTS_STIGMERGY = "../results/stigmergy"
ROBOT_IDS = [0, 1, 2, 3, 4]
METRIC = ["storage", "reliability"]

def aggregate_results(folder, metric) -> dict:
    stepwise_results = {}

    for robot_id in ROBOT_IDS:
        with open(f"{folder}/{robot_id}_{metric}.csv", "r") as result_file:
            store_stepwise_results(csv.reader(result_file), stepwise_results)

    return stepwise_results


def store_stepwise_results(file_reader, stepwise_results: dict) -> None:
    next(file_reader)  # Skip header

    for line in file_reader:
        step = line[2]
        
        if step in stepwise_results:
            stepwise_results[step].append(line)
        else:
            stepwise_results[step] = [line]


def main():
    for folder in [FOLDER_RESULTS_DORA_MESH, FOLDER_RESULTS_HOP_COUNT, FOLDER_RESULTS_STIGMERGY]:
        for metric in METRIC:
            stepwise_results = aggregate_results(folder, metric)

            with open(f"{folder}/concatenated_{metric}.csv", "w") as aggregated_file:
                writer = csv.writer(aggregated_file)
                for step in stepwise_results.values():
                    for result_line in step:
                        writer.writerow(result_line)
    
                    

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


def main():
    failure_time = {}
    detect_time = {}
    location_ok = {}
    num_true_positives = 0
    num_false_positives = 0
    num_false_negatives = 0
    with open("907998-knn2.log", "r") as file:
        for line in file:
            fields = line.split(" ")
            timestep = int(fields[0])
            robot = int(fields[1][-1])
            tag = fields[2]

            if tag == "[flt]":
                if robot not in failure_time:
                    failure_time[robot] = [timestep]
                elif fields[3] == "exit":
                    num_false_negatives += 1 # enter should have been detected
                    failure_time[robot].pop()
                    if not failure_time[robot]:
                        failure_time.pop(robot)
                elif fields[3] == "enter":
                    failure_time[robot].append(timestep)
                else:
                    failure_time[robot][-1] = timestep
            elif tag == "[map]":
                pos_x = float(fields[5][:-1].replace(',', '.'))
                pos_y = float(fields[6].replace(',', '.'))
                if pos_x < -4.0 and pos_y > 6.0:
                    location_ok[robot] = True
                elif pos_x > 4.0 and pos_y < -6.0:
                    location_ok[robot] = True
            elif tag == "[cns:1]":
                target = int(fields[4])
                detect_time[target] = timestep

    print(failure_time)
    print(detect_time)
    for robot in range(10):
        if robot in detect_time and robot in failure_time:
            if failure_time[robot][-1] <= detect_time[robot]:
                num_true_positives += 1
        elif robot in detect_time and not robot in failure_time:
            if robot in location_ok:
                num_true_positives += 1
            else:
                num_false_positives += 1

    print(f"TP {num_true_positives}")
    print(f"FP {num_false_positives}")
    print(f"FN {num_false_negatives}")


if __name__ == '__main__':
    main()

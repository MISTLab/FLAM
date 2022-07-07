#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Rectangle

the_map = set()
num_true_positives = 0
num_false_positives = 0
num_false_negatives = 0


def process_file(name):
    global the_map
    global num_true_positives
    global num_false_positives
    global num_false_negatives
    failure_time = {}
    detect_time = {}
    location_ok = {}
    with open(name, "r") as file:
        for line in file:
            fields = line.split(" ")
            timestep = int(fields[0])
            robot = int(fields[1][-1])
            tag = fields[2]

            if tag == "[flt]":
                if robot not in failure_time:
                    failure_time[robot] = [timestep]
                elif fields[3] == "exit":
                    num_false_negatives += 1  # enter should have been detected
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
                the_map.add((pos_x, pos_y))
                if pos_x < -4.0 and pos_y > 6.0:
                    location_ok[robot] = True
                elif pos_x > 4.0 and pos_y < -6.0:
                    location_ok[robot] = True
            elif tag == "[cns:1]":
                target = int(fields[4])
                detect_time[target] = timestep

    for robot in range(10):
        if robot in detect_time and robot in failure_time:
            if failure_time[robot][-1] <= detect_time[robot]:
                num_true_positives += 1
        elif robot in detect_time and not robot in failure_time:
            if robot in location_ok:
                num_true_positives += 1
            else:
                num_false_positives += 1


def draw():
    x = []
    y = []
    for px, py in the_map:
        x.append(px)
        y.append(py)
    x = np.array(x) + 10
    y = np.array(y) + 10

    fig, ax = plt.subplots()

    _, xedges, yedges, _ = ax.hist2d(x, y, bins=20, cmin=1, cmap='Blues')

    ax.set_xlim([0, 20])
    ax.set_xticks(np.arange(0, 21, 5))
    ax.set_ylim([0, 20])
    ax.set_yticks(np.arange(0, 21, 5))

    ax.add_patch(
        Rectangle((-10, yedges[17]),
                  abs(-10 - xedges[5]),
                  abs(10 - yedges[17]),
                  color='blue',
                  alpha=0.25))
    ax.add_patch(Rectangle((xedges[16], -10), abs(10 - xedges[16]), abs(-10 - yedges[3]), color='green', alpha=0.25))

    rad_x = np.array([-6.5, -3.5, 0.5, 3.5]) + 10
    rad_y = np.array([-5.5, -3.5, 6.5, 4.5]) + 10
    ax.scatter(rad_x, rad_y, c='red', marker='*')

    plt.show()


def main():
    entries = os.scandir('.')
    for entry in entries:
        if entry.name.endswith('.log'):
            process_file(entry.name)

    print(f"TP {num_true_positives}")
    print(f"FP {num_false_positives}")
    print(f"FN {num_false_negatives}")

    draw()


if __name__ == '__main__':
    main()

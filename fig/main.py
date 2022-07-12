#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.patches import Rectangle

the_map = set()
the_faults_over_time = []
the_faults_time = []
the_detected_faults_over_time = []
the_detected_faults_time = []
num_true_positives = 0
num_false_positives = 0
num_false_negatives = 0


def process_file(name):
    global the_map
    global the_faults_over_time
    global the_faults_time
    global the_detected_faults_over_time
    global the_detected_faults_time
    global num_true_positives
    global num_false_positives
    global num_false_negatives
    failure_time = {}
    detect_time = {}
    location_ok = {}
    failed = {}
    num_alive = 10

    faults_over_time = [0]
    faults_time = [0]

    detected_faults_over_time = [0]
    detected_faults_time = [0]

    with open(name, "r") as file:
        for line in file:
            fields = line.split(" ")
            timestep = int(fields[0])
            robot = int(fields[1][-1])
            tag = fields[2]

            if timestep > 1200:
                continue

            if tag == "[flt]":
                if fields[3] == "enter":
                    faults_over_time.append(faults_over_time[-1] + 1)
                    faults_time.append(timestep)
                elif fields[3] != "exit":
                    if robot not in failed:
                      faults_over_time.append(faults_over_time[-1] + 1)
                      faults_time.append(timestep)
                      failed[robot] = True
                      num_alive -= 1
                      if num_alive < 4:
                        break

                if robot not in failure_time:
                    failure_time[robot] = [timestep]
                else:
                    failure_time[robot].append(timestep)
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

    for robot, timestep in detect_time.items():
        detected_faults_time.append(timestep)
        detected_faults_over_time.append(detected_faults_over_time[-1] + 1)
    detected_faults_time.sort()

    the_faults_over_time.append(faults_over_time)
    the_faults_time.append(faults_time)

    the_detected_faults_over_time.append(detected_faults_over_time)
    the_detected_faults_time.append(detected_faults_time)

    for robot in range(10):
        if robot in detect_time and robot in failure_time:
            if failure_time[robot][-1] <= detect_time[robot]:
                if detect_time[robot] - failure_time[robot][-1] < 100:
                  num_true_positives += 1
                else:
                  num_false_negatives += len(failure_time[robot])
        elif robot in detect_time and not robot in failure_time:
            if robot in location_ok:
                num_true_positives += 1
            else:
                num_false_positives += 1
        elif robot in failure_time and robot not in detect_time:
            num_false_negatives += 1


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

    timesteps = set()
    for ft in the_faults_time:
        for t in ft:
            timesteps.add(t)
    faults_time = list(timesteps)
    faults_time.sort()
    faults_over_time = np.zeros(len(faults_time))[:, np.newaxis]

    detected_faults_over_time = np.zeros(len(faults_time))[:, np.newaxis]

    for fot, ft in zip(the_faults_over_time, the_faults_time):
        faults_over_time = np.concatenate((faults_over_time, np.interp(faults_time, ft, fot)[:, np.newaxis]), axis=1)
    for dfot, dft in zip(the_detected_faults_over_time, the_detected_faults_time):
        detected_faults_over_time = np.concatenate((detected_faults_over_time, np.interp(faults_time, dft, dfot)[:, np.newaxis]), axis=1)

    faults_over_time = faults_over_time[:, 1:]
    detected_faults_over_time = detected_faults_over_time[:, 1:]

    plt.plot(faults_time, np.mean(faults_over_time, axis=1))
    plt.fill_between(faults_time, np.min(faults_over_time, axis=1), np.max(faults_over_time, axis=1), color='blue', alpha=.25)

    plt.plot(faults_time, np.mean(detected_faults_over_time, axis=1))
    plt.fill_between(faults_time, np.min(detected_faults_over_time, axis=1), np.max(detected_faults_over_time, axis=1), color='orange', alpha=.25)

    plt.show()

    df = pd.DataFrame()
    df['t'] = faults_time
    df['min'] = np.min(faults_over_time, axis=1)
    df['avg'] = np.mean(faults_over_time, axis=1)
    df['max'] = np.max(faults_over_time, axis=1)

    df['dmin'] = np.min(detected_faults_over_time, axis=1)
    df['davg'] = np.mean(detected_faults_over_time, axis=1)
    df['dmax'] = np.max(detected_faults_over_time, axis=1)

    df.to_csv('r.csv')

    draw()


if __name__ == '__main__':
    main()

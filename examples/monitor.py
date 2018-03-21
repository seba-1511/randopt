#!/usr/bin/env python3

"""
Usage:
    python monitor.py randopt_results/simple_example/
"""

import sys
import os
import time
import curses

import randopt as ro

USE_MPL = True
USE_CURSES = True

try:
    from terminaltables import AsciiTable, SingleTable
except:
    raise('run pip install terminaltables')

try:
    import matplotlib.pyplot as plt
except:
    print('matplotlib not found, live plotting disable.')
    USE_MPL = False


def table_statistics(counts, timings, minimums, maximums, name='Experiment'):
    minimum = "{0:.3f}".format(minimums[-1])
    maximum = "{0:.3f}".format(maximums[-1])
    timing = "{0:.2f}".format(timings[-1])
    data = [
        ['Results Count', 'Minimum Result', 'Maximum Result', 'Time Elapsed'],
        [counts[-1], minimum, maximum, timing],
    ]
    if USE_CURSES:
        table = AsciiTable(data, name)
    else:
        table = SingleTable(data, name)
#    table = SingleTable(data, name)
    table.inner_heading_row_border = True
    table.inner_row_border = True
    table.inner_column_border = True
    table.outer_border = False
    table.justify_columns = {0: 'center', 1: 'center', 2: 'center', 3: 'center'}
    return table.table


def plot_statistics(counts, timings, minimums, maximums, name='Experiment'):
    plt.ion()
    plt.clf()

    # Min subplot
    plt.subplot(211)
    plt.title('Experiment ' + name + ' Statistics')
    plt.plot(counts, minimums, label='Minimum')
    plt.legend()
    plt.ylabel('Result')

    # Min subplot
    plt.subplot(212)
    plt.plot(counts, maximums, label='Maximum')
    plt.legend()
    plt.xlabel('Number of experiments')
    plt.ylabel('Result')

    # This renders the figure
    plt.pause(0.05)


if __name__ == '__main__':
    exp_path = sys.argv[1]
    if exp_path[-1] == '/':
        exp_path = exp_path[:-1]
    exp_dir, exp_name = os.path.split(exp_path)
    exp = ro.Experiment(exp_name, directory=exp_dir)

    # init interactive display
    if USE_CURSES:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        screen.keypad(True)

    start_time = time.time()
    timings = []
    minimums = []
    maximums = []
    counts = []
    try:
        while True:
            minimums.append(exp.minimum().result)
            maximums.append(exp.maximum().result)
            counts.append(exp.count())
            timings.append(time.time() - start_time)
            if USE_MPL:
                plot_statistics(counts, timings, minimums, maximums, exp_name)
            table = table_statistics(
                counts, timings, minimums, maximums, exp_name)
            if USE_CURSES:
                screen.addstr(0, 0, 'Experiment ' + exp_name + ' Statistics')
                for i, line in enumerate(table.split('\n')):
                        line = line.replace('-', u'\u2500')
                        line = line.replace('|', u'\u2502')
                        line = line.replace('+', u'\u253c')
                        screen.addstr(2 + i, 0, line)
                screen.refresh()
            else:
                print(table)
            if USE_MPL:
                plt.pause(5)
            else:
                time.sleep(5)
    finally:
        if USE_CURSES:
            curses.echo()
            curses.nocbreak()
            screen.keypad(True)
            curses.endwin()
        
        

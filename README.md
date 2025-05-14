# Disk Scheduling Simulator

A command-line Python application that simulates and analyzes various disk scheduling algorithms, including:

- First-Come First-Served (FCFS)
- Shortest Seek Time First (SSTF)
- SCAN
- C-SCAN
- LOOK
- C-LOOK

Developed for **CSCI 447: Operating Systems** (Spring 2024) as a way to examine the efficiency and behavior of different disk scheduling strategies under randomized conditions.

## Project Overview

This simulator compares the performance of six disk scheduling algorithms based on two key metrics:

- **C (Direction Changes)** – The number of times the disk head changes direction.
- **M (Total Movement)** – The total distance moved by the disk head.

The simulator accepts multiple input modes (including full randomization) and generates results from 1,000 disk I/O requests. It prints out comparative data and logs results that can be used for analysis.

## Features

- Full simulation of major disk scheduling algorithms
- Randomized or user-defined starting positions and request sequences
- Supports reproducible testing
- Output includes detailed logs of direction changes and total movement per run

## Example Test Output

Ten runs with 1,000 random requests each produced the following results:

| Algorithm | Avg. Direction Changes (C) | Avg. Total Movement (M) |
|-----------|-----------------------------|--------------------------|
| FCFS      | 668.3                       | 3323456.3                |
| SSTF      | 1.9                         | 15528.5                  |
| SCAN      | 1.0                         | 14596.7                  |
| C-SCAN    | 1.0                         | 16767.5                  |
| LOOK      | 1.3                         | 16793.0                  |
| C-LOOK    | 1.0                         | 16732.9                  |

> FCFS was found to be the **most fair but least efficient**, while SCAN had the **best overall efficiency** by minimizing costly direction changes.

See [`diskSchedulingAnalysis.txt`](./diskSchedulingAnalysis.txt) for the full report and interpretation.

## Usage

```bash
python3 DiskSim.py
```

You'll be prompted to choose from various simulation options, including:

- Manually input requests and starting head position
- Generate a fixed or randomized sequence of I/O requests
- Run multiple tests automatically for statistical analysis

## File Structure

`DiskSim.py` – Main program with algorithm implementations and CLI interface

`diskSchedulingAnalysis.txt` – Summary of 10 randomized simulation runs and algorithm efficiency analysis

## Author

Andrew Cox
Western Washington University
Spring 2024

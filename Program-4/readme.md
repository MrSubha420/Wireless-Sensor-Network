# Network Simulation Project

A Python-based network simulation tool that allows you to model and analyze various network topologies and routing protocols. Customize your simulation parameters to study network behavior under different configurations.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Features

- Supports multiple routing protocols: AODV, DSR
- Customizable network topologies: Grid, Random, Cluster
- Adjustable simulation parameters:
  - Number of nodes
  - Number of simulation steps
  - Number of random links between nodes
- Command-line interface for easy configuration and execution

## Prerequisites

- **Python 3.6+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Required Python Packages**: Install necessary packages using `pip`.

## bash
pip install -r requirements.txt

-- Step1: git clone https://github.com/MrSubha420/Wireless-Sensor-Network/tree/main/wsn-sim-master
-- Step2: python -m compileall node.py
-- step3: python -m compileall network.py
-- Step4: setup cli.py according to you need
Routing Protocol: Choose between AODV or DSR.
Number of Simulation Steps: Define how many steps the simulation will run.
Number of Nodes: Specify the total number of nodes in the network.
Number of Random Links Between Nodes: Determine how many random connections exist between nodes.
Network Topology: Select from grid, random, or cluster.

-- Step5: python -m compileall cli.py
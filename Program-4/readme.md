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

- **Multiple Routing Protocols**: Supports AODV and DSR.
- **Customizable Network Topologies**: Choose from Grid, Random, or Cluster topologies.
- **Adjustable Simulation Parameters**:
  - **Number of Nodes**: Specify the total number of nodes in the network.
  - **Number of Simulation Steps**: Define how many steps the simulation will run.
  - **Number of Random Links Between Nodes**: Determine the number of random connections between nodes.
- **Command-Line Interface**: Easy configuration and execution through the CLI.

## Prerequisites

Before installing the Network Simulation Project, ensure you have the following prerequisites:

- **Python 3.6+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: Required for cloning the repository. Download from [git-scm.com](https://git-scm.com/downloads).
- **pip**: Python package installer, typically included with Python. Verify by running `pip --version` in your terminal.

## Installation

Follow these steps to set up the Network Simulation Project on your local machine:

### 1. Clone the Repository

- First, clone the repository to your local machine using Git:

- git clone https://github.com/MrSubha420/Wireless-Sensor-Network.git

### 2. Navigate to the project directory
- cd Wireless-Sensor-Network/wsn-sim-master

### 3. Install Required Python Packages
- pip install -r requirements.txt

### 4. Compile Python Modules
- python -m compileall node.py
- python -m compileall network.py
### 5.  Configure cli.py
- protocol: Routing protocol to use (AODV or DSR). Required.
- steps: Number of simulation steps. Default: 100
- nodes: Number of nodes in the network. Default: 50
- random-links: Number of random links between nodes. Default: 10
- topology: Network topology (Grid, Random, or Cluster). Default: Random
- Example : python cli.py --protocol AODV --steps 100 --nodes 50 --random-links 10 --topology Grid

# Wireless and Sensor Networks Laboratory  
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/MrSubha420/Wireless-Sensor-Network)

This repository contains a set of laboratory experiments on **Wireless and Sensor Networks (WSNs)**. These experiments are part of the **Wireless and Sensor Networks Laboratory** course [PGIT(IoT)292] for the **M.Tech. Internet of Things** program at Maulana Abul Kalam Azad University of Technology.

---

## Table of Contents  
- [Introduction](#introduction)  
- [Experiments](#experiments)  
- [Setup Instructions](#setup-instructions)  
- [How to Run](#how-to-run)  
- [Output and Visualizations](#output-and-visualizations)  
- [Author](#author)  
- [License](#license)  

---

## Introduction  
Wireless Sensor Networks (WSNs) play a vital role in modern IoT applications such as environmental monitoring, smart agriculture, and industrial automation. This repository demonstrates various WSN simulations using Python for:  
- Creating network models.  
- Implementing communication protocols.  
- Simulating routing protocols.  
- Exploring energy-efficient clustering mechanisms like LEACH.

---

## Experiments  

### 1. Network Simulation and Data Communication  
- Simulates a WSN with random connections.  
- Implements 3-step communication: **Request**, **Acknowledgment**, and **Data Transfer**.  

[View Code](https://github.com/MrSubha420/Wireless-Sensor-Network/blob/main/program1.py)  

---

### 2. CSMA/CD Protocol Implementation  
- Implements **Carrier Sense Multiple Access with Collision Detection (CSMA/CD)**.  
- Simulates medium access control in WSNs with collision detection and resolution mechanisms.  

[View Code](https://github.com/MrSubha420/Wireless-Sensor-Network/blob/main/program2.py)  

---

### 3. TDMA and FDMA Protocol Implementation  
- **TDMA (Time Division Multiple Access)**: Divides communication into time slots for each node.  
- **FDMA (Frequency Division Multiple Access)**: Allocates unique frequency bands to each node for data transmission.  

[View Code](https://github.com/MrSubha420/Wireless-Sensor-Network/blob/main/program3.py)  

---

### 4. Routing Protocols Simulation (AODV & DSR)  
- Implements reactive routing protocols:  
  - **AODV (Ad hoc On-Demand Distance Vector)**.  
  - **DSR (Dynamic Source Routing)**.  
- Simulates packet routing in various network topologies: grid, random, and clustered.  

[View Code](https://github.com/MrSubha420/Wireless-Sensor-Network/tree/main/Program-4)

---

### 5. LEACH Protocol Simulation  
- Implements **Low-Energy Adaptive Clustering Hierarchy (LEACH)** for energy-efficient communication.  
- Groups nodes into clusters with designated cluster heads for data aggregation and transmission.  

[View Code](https://github.com/MrSubha420/Wireless-Sensor-Network/blob/main/program5.py)  

---

## Setup Instructions  

### Prerequisites  
1. Python 3.12+  
2. IDE: Visual Studio Code or any Python-compatible editor.  

### Install Dependencies  
```bash
pip install networkx matplotlib numpy plotly dash
```
## How to Run  

### Run Experiments 
- (Let program1 )
1. Clone the repository:  
   ```bash
   git clone https://github.com/MrSubha420/Wireless-Sensor-Network.git
   cd Wireless-Sensor-Network
   ```
2. Navigate to the desired experiment file and run:
```bash
 python program1.py
```
## Output and Visualizations
- program1 output :
  <img align="center" src="img/mybanner.JPG" alt="MrSubha420"/>
- program2 output :
  <img align="center" src="img/mybanner.JPG" alt="MrSubha420"/>
- program3 output :
  <img align="center" src="img/mybanner.JPG" alt="MrSubha420"/>
- program4 output :
  <img align="center" src="img/mybanner.JPG" alt="MrSubha420"/>
- program5 output :
  <img align="center" src="img/mybanner.JPG" alt="MrSubha420"/>
## License  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



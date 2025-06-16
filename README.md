# ZOD CLFT

This project provides tools for processing and visualizing the Zenseact Open Dataset (ZOD) using camera and LiDAR data.

## Prerequisites

- Docker
- ZOD dataset files (mini or full version)

## Setup and Installation

### 1. Data Preparation
Copy the unpacked ZOD data files to the `/data` folder:
- `drives_mini.tar.gz`
- `frames_mini.tar.gz` 
- `sequences_mini.tar.gz`

### 2. Start the Application
```bash
docker compose -f compose.yml run --rm nvidia-pytorch bash
```

This will:
- Build the Docker container with NVIDIA PyTorch base image
- Install required dependencies
- Extract the data files to `/data_zod`
- Launch an interactive bash session

## Output Structure

All processed images are saved in the `/workspace/output/` directory with the following structure:

## Running Individual Modules

Once inside the Docker container, you can run any of the processing modules:

### Camera Processing
Process camera images with annotations:
```bash
python3 camera.py
```

<div align="center">
<table>
<tr>
<td><img src="examples/camera/camera_009158.png" width="300"></td>
<td><img src="examples/camera/camera_018591.png" width="300"></td>
</tr>
<tr>
<td><img src="examples/camera/camera_062592.png" width="300"></td>
<td><img src="examples/camera/camera_083430.png" width="300"></td>
</tr>
</table>
</div>

### LiDAR Visualization
Generate pure LiDAR visualizations:
```bash
python3 lidar.py
```

<div align="center">
<table>
<tr>
<td><img src="examples/lidar/lidar_009158.png" width="300"></td>
<td><img src="examples/lidar/lidar_018591.png" width="300"></td>
</tr>
<tr>
<td><img src="examples/lidar/lidar_062592.png" width="300"></td>
<td><img src="examples/lidar/lidar_083430.png" width="300"></td>
</tr>
</table>
</div>

### Aggregated LiDAR
Create multi-frame aggregated LiDAR visualizations:
```bash
python3 lidar_aggregated.py
```

<div align="center">
<table>
<tr>
<td><img src="examples/lidar_aggregated/lidar_aggregated_009158.png" width="300"></td>
<td><img src="examples/lidar_aggregated/lidar_aggregated_018591.png" width="300"></td>
</tr>
<tr>
<td><img src="examples/lidar_aggregated/lidar_aggregated_062592.png" width="300"></td>
<td><img src="examples/lidar_aggregated/lidar_aggregated_083430.png" width="300"></td>
</tr>
</table>
</div>

### Motion-Compensated LiDAR
Generate motion-compensated LiDAR visualizations:
```bash
python3 lidar_compensated.py
```

<div align="center">
<table>
<tr>
<td><img src="examples/lidar_compensated/lidar_compensated_009158.png" width="300"></td>
<td><img src="examples/lidar_compensated/lidar_compensated_018591.png" width="300"></td>
</tr>
<tr>
<td><img src="examples/lidar_compensated/lidar_compensated_062592.png" width="300"></td>
<td><img src="examples/lidar_compensated/lidar_compensated_083430.png" width="300"></td>
</tr>
</table>
</div>

### Camera-LiDAR Fusion
Create fused camera-LiDAR visualizations:
```bash
python3 camera_lidar.py
```

<div align="center">
<table>
<tr>
<td><img src="examples/camera_lidar/camera_lidar_009158.png" width="300"></td>
<td><img src="examples/camera_lidar/camera_lidar_018591.png" width="300"></td>
</tr>
<tr>
<td><img src="examples/camera_lidar/camera_lidar_062592.png" width="300"></td>
<td><img src="examples/camera_lidar/camera_lidar_083430.png" width="300"></td>
</tr>
</table>
</div>

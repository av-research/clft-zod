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
```
output/
├── camera/           # Enhanced camera images with annotations
├── lidar/            # Pure LiDAR visualizations
├── lidar_aggregated/ # Multi-frame aggregated LiDAR
├── lidar_compensated/# Motion-compensated LiDAR
└── camera_lidar/     # Fused camera-LiDAR visualizations
```

## Running Individual Modules

Once inside the Docker container, you can run any of the processing modules:

```bash
# Process camera images with annotations
python camera.py

# Generate LiDAR visualizations
python lidar.py

# Create aggregated LiDAR visualizations
python lidar_aggregated.py

# Generate motion-compensated LiDAR
python lidar_compensated.py

# Create camera-LiDAR fusion images
python camera_lidar.py
```

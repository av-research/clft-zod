#!/bin/bash

# Create /data_zod directory
mkdir -p /data_zod

# Define file paths
DRIVES_FILE="/workspace/data/drives_mini.tar.gz"
FRAMES_FILE="/workspace/data/frames_mini.tar.gz"
SEQUENCES_FILE="/workspace/data/sequences_mini.tar.gz"

# Function to extract a file if it exists and target doesn't exist
extract_if_needed() {
    local file_path="$1"
    local file_name="$2"
    local target_check="$3"

    if [ -f "$file_path" ]; then
        if [ ! -d "$target_check" ] && [ ! -f "$target_check" ]; then
            echo "Extracting $file_name..."
            local extract_start=$(date +%s)
            cd /data_zod
            tar -xzf "$file_path" -C /data_zod
            local extract_end=$(date +%s)
            local extract_time=$((extract_end - extract_start))
            if [ $? -eq 0 ]; then
                echo "$file_name extracted in ${extract_time}s"
            else
                echo "Failed to extract $file_name"
            fi
        else
            echo "$file_name already extracted"
        fi
    else
        echo "$file_name not found"
    fi
}

# Extract each file if present
extract_if_needed "$DRIVES_FILE" "drives_mini.tar.gz" "/data_zod/drives"
extract_if_needed "$FRAMES_FILE" "frames_mini.tar.gz" "/data_zod/frames"  
extract_if_needed "$SEQUENCES_FILE" "sequences_mini.tar.gz" "/data_zod/sequences"

# Quick status
if [ -d "/data_zod/drives" ] || [ -d "/data_zod/frames" ] || [ -d "/data_zod/sequences" ]; then
    echo "ZOD data ready at /data_zod"
else
    echo "No ZOD data found - place .tar.gz files in ./data/"
fi

# Execute the command passed to the container (usually bash)
exec "$@"

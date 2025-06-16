from zod import ZodFrames
from zod.visualization.lidar_on_image import visualize_lidar_on_image
import numpy as np
import os
from PIL import Image

# NOTE! Set the path to dataset and choose a version
dataset_root = "../data_zod"  # your local path to zod
version = "mini"  # "mini" or "full"

# Create output directory if it doesn't exist
output_dir = '/workspace/output/lidar_compensated'
os.makedirs(output_dir, exist_ok=True)

# initialize ZodFrames
zod_frames = ZodFrames(dataset_root=dataset_root, version=version)
print(f"Total frames available: {len(zod_frames)}")

# Get training and validation frame IDs (since "all" is not supported)
train_frame_ids = list(zod_frames.get_split("train"))
val_frame_ids = list(zod_frames.get_split("val"))
all_frame_ids = train_frame_ids + val_frame_ids

print(f"Processing {len(all_frame_ids)} frames ({len(train_frame_ids)} train + {len(val_frame_ids)} val)...")

for i, frame_id in enumerate(all_frame_ids):
    try:
        print(f"Processing frame {i+1}/{len(all_frame_ids)}: {frame_id}")
        
        # Get the frame object
        zod_frame = zod_frames[frame_id]
        metadata = zod_frame.metadata
        print(f"Metadata attributes: {dir(metadata)}")
        
        # Use the frame_id from the iterator since metadata doesn't have frameId
        print(f"Frame ID from iterator: {frame_id}")
        
        # Use iterator frame_id for filename
        frame_id_for_filename = int(frame_id)
        
        # Get the original camera image to get dimensions
        original_image = zod_frame.get_image()

        image_timestamp = zod_frame.info.keyframe_time.timestamp()

        # Get a single Lidar point cloud
        core_lidar = zod_frame.get_lidar()[0]
        # Plot aggregated Lidar point cloud
        compensated_lidar = zod_frame.compensate_lidar(core_lidar, image_timestamp)
        lid_image = visualize_lidar_on_image(
            compensated_lidar,
            zod_frame.calibration,
            original_image,
        )

        # Convert numpy array to PIL Image if needed
        if isinstance(lid_image, np.ndarray):
            # If image is in RGB format (height, width, 3)
            if len(lid_image.shape) == 3 and lid_image.shape[2] == 3:
                pil_image = Image.fromarray(lid_image.astype(np.uint8))
            else:
                # Handle other formats if needed
                pil_image = Image.fromarray(lid_image)
        else:
            # If image is already a PIL Image
            pil_image = lid_image
        
        # Save the image using metadata frameId
        output_path = f'{output_dir}/lidar_compensated_{frame_id_for_filename:06d}.png'
        pil_image.save(output_path, 'PNG', optimize=True, quality=95)
        
        if i % 10 == 0:  # Print progress every 10 frames
            print(f"  Saved: {output_path}")
            
    except Exception as e:
        print(f"  Error processing frame {frame_id}: {e}")
        continue

print(f"Finished processing all frames. Images saved to: {output_dir}")

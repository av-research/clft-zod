from zod import ZodFrames
from zod.visualization.lidar_on_image import visualize_lidar_on_image
from typing import List
import numpy as np
import os
from PIL import Image

def initialize_zod_frames(dataset_root: str = "../data_zod", version: str = "mini") -> ZodFrames:
    """
    Initialize ZodFrames object with specified dataset root and version.
    
    Args:
        dataset_root: Path to the ZOD dataset root directory
        version: Dataset version to use ("mini" or "full")
        
    Returns:
        Initialized ZodFrames object
    """
    zod_frames = ZodFrames(dataset_root=dataset_root, version=version)
    print(f"Initialized ZOD dataset from: {dataset_root}")
    print(f"Version: {version}")
    print(f"Total frames available: {len(zod_frames)}")
    return zod_frames

def get_all_frame_ids(zod_frames: ZodFrames) -> List[str]:
    """
    Get all available frame IDs from training and validation splits.
    
    Args:
        zod_frames: ZodFrames object
        
    Returns:
        List of all frame IDs (train + validation)
    """
    train_frame_ids = list(zod_frames.get_split("train"))
    val_frame_ids = list(zod_frames.get_split("val"))
    all_frame_ids = train_frame_ids + val_frame_ids
    
    print(f"Found {len(all_frame_ids)} total frames ({len(train_frame_ids)} train + {len(val_frame_ids)} val)")
    return all_frame_ids

def process_frame_with_lidar_visualization(zod_frames: ZodFrames, frame_id: str) -> Image.Image:
    """
    Process a single frame and return a LiDAR visualization on white background.
    
    Args:
        zod_frames: ZodFrames object for accessing frame data
        frame_id: The frame ID to process
        
    Returns:
        PIL Image with LiDAR point cloud visualization
    """
    # Get the frame object
    zod_frame = zod_frames[frame_id]
    
    # Get the original camera image to get dimensions
    original_image = zod_frame.get_image()
    height, width = original_image.shape[:2]

    # Create a white image with the same dimensions as the camera image
    white_image = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Get image timestamp for LiDAR aggregation
    image_timestamp = zod_frame.info.keyframe_time.timestamp()

    # Plot aggregated LiDAR point cloud
    aggregated_lidar = zod_frame.get_aggregated_lidar(num_before=1, num_after=1, timestamp=image_timestamp)
    lid_image = visualize_lidar_on_image(
        aggregated_lidar,
        zod_frame.calibration,
        white_image,
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
    
    return pil_image

def main():
    """
    Main function to process all frames with LiDAR visualization.
    
    This function handles the complete workflow:
    1. Initialize ZodFrames dataset
    2. Get all available frame IDs
    3. Process each frame with LiDAR visualization
    4. Save LiDAR visualizations to output directory
    """
    # Configuration variables
    dataset_root = "../data_zod"  # your local path to zod
    version = "mini"  # "mini" or "full"
    output_dir = '/workspace/output/lidar'
    
    # Initialize ZodFrames
    zod_frames = initialize_zod_frames(dataset_root, version)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all available frame IDs
    all_frame_ids = get_all_frame_ids(zod_frames)

    print(f"Processing {len(all_frame_ids)} frames...")

    for i, frame_id in enumerate(all_frame_ids):
        try:
            print(f"Processing frame {i+1}/{len(all_frame_ids)}: {frame_id}")
            
            # Process frame and get LiDAR visualization
            lidar_image = process_frame_with_lidar_visualization(zod_frames, frame_id)
            
            # Use iterator frame_id for filename
            frame_id_for_filename = int(frame_id)
            
            # Save the image
            output_path = f'{output_dir}/lidar_{frame_id_for_filename:06d}.png'
            lidar_image.save(output_path, 'PNG', optimize=True, quality=95)
            
            if i % 10 == 0:  # Print progress every 10 frames
                print(f"  Saved: {output_path}")
                
        except Exception as e:
            print(f"  Error processing frame {frame_id}: {e}")
            continue

    print(f"Finished processing all frames. Images saved to: {output_dir}")


if __name__ == "__main__":
    main()

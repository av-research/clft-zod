#!/usr/bin/env python3
"""
Script to resize example images for README display.
Converts large 4K images to smaller, web-friendly sizes while maintaining aspect ratio.
"""

import os
from PIL import Image
import argparse

def resize_image(input_path, output_path, max_width=800, quality=85):
    """
    Resize an image to a maximum width while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the resized image
        max_width (int): Maximum width in pixels (default: 800)
        quality (int): JPEG quality (1-100, default: 85)
    """
    try:
        with Image.open(input_path) as img:
            # Get original dimensions
            original_width, original_height = img.size
            
            # Calculate new dimensions if resizing is needed
            if original_width > max_width:
                ratio = max_width / original_width
                new_width = max_width
                new_height = int(original_height * ratio)
                
                # Resize the image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save with optimization
                if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                    resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
                elif output_path.lower().endswith('.png'):
                    resized_img.save(output_path, 'PNG', optimize=True)
                else:
                    resized_img.save(output_path, optimize=True)
                
                print(f"Resized {input_path}: {original_width}x{original_height} -> {new_width}x{new_height}")
            else:
                # Image is already small enough, just copy with optimization
                if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
                    img.save(output_path, 'JPEG', quality=quality, optimize=True)
                elif output_path.lower().endswith('.png'):
                    img.save(output_path, 'PNG', optimize=True)
                else:
                    img.save(output_path, optimize=True)
                
                print(f"Optimized {input_path}: {original_width}x{original_height} (no resize needed)")
                
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_examples_folder(max_width=800, quality=85, source_dir="output", target_dir="examples"):
    """
    Process all images from source folder and save resized versions to target folder.
    
    Args:
        max_width (int): Maximum width for resized images
        quality (int): JPEG quality (1-100)
        source_dir (str): Source directory containing original images
        target_dir (str): Target directory for resized images
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found!")
        return
    
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created target directory: {target_dir}")
    
    # Process each subfolder in source directory
    for subfolder in os.listdir(source_dir):
        source_subfolder_path = os.path.join(source_dir, subfolder)
        
        if os.path.isdir(source_subfolder_path):
            print(f"\nProcessing folder: {subfolder}")
            
            # Create corresponding subfolder in target directory
            target_subfolder_path = os.path.join(target_dir, subfolder)
            if not os.path.exists(target_subfolder_path):
                os.makedirs(target_subfolder_path)
                print(f"Created target subfolder: {target_subfolder_path}")
            
            # Process each image in the source subfolder
            for filename in os.listdir(source_subfolder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    input_path = os.path.join(source_subfolder_path, filename)
                    output_path = os.path.join(target_subfolder_path, filename)
                    
                    resize_image(input_path, output_path, max_width, quality)

def main():
    parser = argparse.ArgumentParser(description="Resize images from output folder to examples folder")
    parser.add_argument("--width", type=int, default=1024, 
                       help="Maximum width in pixels (default: 1024)")
    parser.add_argument("--quality", type=int, default=100, 
                       help="JPEG quality 1-100 (default: 100)")
    parser.add_argument("--source", type=str, default="output", 
                       help="Source directory with original images (default: output)")
    parser.add_argument("--target", type=str, default="examples", 
                       help="Target directory for resized images (default: examples)")
    
    args = parser.parse_args()
    
    print("Starting image resize process...")
    print(f"Source directory: {args.source}")
    print(f"Target directory: {args.target}")
    print(f"Target width: {args.width}px")
    print(f"Quality: {args.quality}")
    
    process_examples_folder(args.width, args.quality, args.source, args.target)
    
    print(f"\nImage resize process completed!")
    print(f"Resized images saved to '{args.target}' folder")
    print("The examples folder now contains web-optimized versions of your images.")

if __name__ == "__main__":
    main()

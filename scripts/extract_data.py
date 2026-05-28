"""
Extract Data Script
===================
This script extracts the GSE279208_RAW.tar archive and then extracts
all .gz files found. The files are extracted to the data/raw directory.
"""

import tarfile
import gzip
import os
import shutil
from pathlib import Path

# Define the paths
tar_file_path = "data/raw/GSE279208_RAW.tar"
extract_base_dir = "data/raw"


def extract_tar_file(tar_path, extract_to):
    """
    Extract all files from a .tar archive.
    
    Args:
        tar_path (str): .tar file path
        extract_to (str): Directory where files will be extracted
    """
    print(f"Starting extraction of {tar_path}...")
    
    try:
        # Open the tar file in read mode
        with tarfile.open(tar_path, "r") as tar:
            # Extract all members to the specified directory
            tar.extractall(path=extract_to)
        print(f"Successfully extracted {tar_path}")
    except Exception as e:
        print(f"Error extracting tar file: {e}")
        raise


def extract_gz_files(base_dir):
    """
    Find and extract all .gz files in a directory (recursively).
    
    Args:
        base_dir (str): Base directory to search for .gz files
    """
    print(f"\n Searching for .gz files in {base_dir}...")
    
    # Find all .gz files recursively
    gz_files = list(Path(base_dir).rglob("*.gz"))
    
    if not gz_files:
        print("  No .gz files found!")
        return
    
    print(f"Found {len(gz_files)} .gz file(s) to extract\n")
    
    # Extract each .gz file
    for gz_file in gz_files:
        extract_single_gz_file(str(gz_file))


def extract_single_gz_file(gz_path):
    """
    Extract a single .gz file.
    The extracted file is saved in the same directory as the original .gz file,
    with the .gz extension removed from its name.
    
    Args:
        gz_path (str): Path to the .gz file to extract
    """
    try:
        # Create the output path by removing .gz from the filename
        output_path = gz_path[:-3]  # Remove the last 3 characters (.gz)
        
        print(f"  Extracting: {os.path.basename(gz_path)}")
        
        # Open the .gz file in binary read mode
        with gzip.open(gz_path, "rb") as gz_file:
            # Open the output file in binary write mode
            with open(output_path, "wb") as out_file:
                # Copy the decompressed data from gz_file to out_file
                shutil.copyfileobj(gz_file, out_file)
        
        print(f"    → Saved as: {os.path.basename(output_path)}")
    except Exception as e:
        print(f"    Error extracting {gz_path}: {e}")


def delete_gz_files(base_dir):
    """
    Delete all .gz files recursively after extraction.
    
    Args:
        base_dir (str): Base directory to search for .gz files
    """
    gz_files = list(Path(base_dir).rglob("*.gz"))
    
    if not gz_files:
        print("\nNo .gz files to delete.")
        return
    
    print(f"\nDeleting {len(gz_files)} .gz file(s)...")
    
    for gz_file in gz_files:
        try:
            os.remove(gz_file)
            print(f"  Deleted: {gz_file.name}")
        except Exception as e:
            print(f"  Error deleting {gz_file.name}: {e}")


def main():
    print("=" * 60)
    print("Starting Data Extraction Process")
    print("=" * 60)
    
    # Check if the tar file exists
    if not os.path.exists(tar_file_path):
        print(f"Error: {tar_file_path} not found!")
        return
    
    # Step 1: Extract the tar file
    extract_tar_file(tar_file_path, extract_base_dir)
    
    # Step 2: Extract all .gz files
    extract_gz_files(extract_base_dir)

    # Step 3: Delete .gz files
    delete_gz_files(extract_base_dir)
    
    print("\n" + "=" * 60)
    print("Extraction process completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

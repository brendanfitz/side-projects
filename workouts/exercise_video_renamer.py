# Import the necessary libraries
from pathlib import Path
import argparse
import ffmpeg
import re
from datetime import datetime


GOPRO_FILENAME_PAT = r'GX(\d+).MP4'

def is_in_gopro_format(filename):
    return re.match(GOPRO_FILENAME_PAT, filename) is not None
    

def get_video_creation_date(video_path):
    try:
        metadata = ffmpeg.probe(video_path)["streams"][0]
    except Exception as e:
        print(f'Error on path: {video_path}')
        raise e
    created_datetime = datetime.strptime(metadata['tags']['creation_time'],
                                         '%Y-%m-%dT%H:%M:%S.%fZ')
    created_date_string = created_datetime.strftime('%Y-%m-%d')
    return created_date_string

# Define the function to rename files
def rename_files_in_directory(parent_directory):
    parent_path = Path(parent_directory)
    
    # Check if the parent directory exists
    if not parent_path.exists() or not parent_path.is_dir():
        print(f"The directory {parent_directory} does not exist or is not a directory.")
        return
    
    # Traverse through all subdirectories and files
    cnt_renamed = 0
    for current_path in parent_path.rglob('*'):
        # Check if the current path is a file
        if current_path.is_file() and is_in_gopro_format(current_path.name):
            # Get video creation date
            vid_created_date_string = get_video_creation_date(current_path)

            # Generate the new file name by appending the parent directory name to the original file name
            new_file_name = f"{current_path.parent.name} -- {vid_created_date_string} ({current_path.stem}).MP4"
            
            # Generate the new file path
            new_file_path = current_path.parent / new_file_name
            
            # Rename the file
            current_path.rename(new_file_path)
            # print(f"Renamed {current_path} to {new_file_path}")
            cnt_renamed += 1
    
    return cnt_renamed

# Setup argparse to accept a directory argument
def setup_argparse():
    parser = argparse.ArgumentParser(description="Rename files by prefixing the directory name.")
    parser.add_argument("directory", type=str, nargs='?', help="The parent directory to start renaming files in.")
    return parser.parse_args()

# Example usage
if __name__ == "__main__":
    # args = setup_argparse()
    # directory = args.directory
    directory = Path('/mnt') / 'Fitness' / 'Workout Videos' 
    cnt_renamed = rename_files_in_directory(directory)
    print(f"Renamed {cnt_renamed} files in {directory}")
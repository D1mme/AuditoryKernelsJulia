import pandas as pd
from pathlib import Path
from argparse import ArgumentParser
import glob 
import os
from time import sleep
import csv

def merge_duration_column(folder: str):
    folder_path = Path(folder)
    
    # Check if test_m.tsv already exists --> this indicates that the thing was succesfull and does not need to be reran.
    file_path_check = folder_path / "test_m.tsv"
    if file_path_check.exists():
        return
    
    duration_file = folder_path / "clip_durations.tsv"
    
    # Load the duration data
    durations_df = pd.read_csv(duration_file, sep='\t')
    
    # Process each dataset file
    for file_name in ["dev.tsv", "train.tsv", "test.tsv"]:
        file_path = folder_path / file_name
        if file_path.exists():
            df = pd.read_csv(file_path, sep='\t', low_memory = False, quoting=csv.QUOTE_NONE)
            
            # Merge on 'path' and 'clip' columns
            df = df.merge(durations_df, left_on='path', right_on='clip', how='left')
            
            # Drop duplicate 'clip' column
            df.drop(columns=['clip'], inplace=True)
            
            # Reorder columns to place 'duration[ms]' after 'path'
            if 'duration[ms]' in df.columns:
                cols = df.columns.tolist()
                cols.insert(cols.index('path') + 1, cols.pop(cols.index('duration[ms]')))
                df = df[cols]
            
            # Save as modified TSV
            output_file = folder_path / file_name.replace('.tsv', '_m.tsv')
            df.to_csv(output_file, index=False, sep='\t')
            print(f"Processed and saved: {output_file}")
        else:
            print(f"File not found: {file_name}")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help='Directory containing the data')
    args = parser.parse_args()

    # Use glob to find all subdirectories inside the given directory
    directories = sorted(glob.glob(os.path.join(args.dir, '*/')))  # This matches directories under args.dir
    print(directories)
    sleep(3)
    exception_list = []
    if not directories:
        print(f"No directories found in {args.dir}")
    else:
        print(f"Found {len(directories)} directories.")
        # Iterate over each directory and apply the function
        for directory in directories:
            print("Doing directory ", directory)
            try:
                merge_duration_column(directory)
            except Exception as e:
                print(e)
                print("Exception occured in ", directory)
                exception_list.append(directory)
    print(" ")
    print("Exceptions occurred in:")
    print(exception_list)

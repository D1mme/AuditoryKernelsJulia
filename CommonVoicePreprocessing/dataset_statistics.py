import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from argparse import ArgumentParser
import glob
import os
from time import sleep

def get_duration(folder: str):
    folder_path = Path(folder)

    # Initialize empty dataframes for dev, test, train
    dev, test, train = None, None, None

    # Process each dataset file
    for file_name in ["dev_m.tsv", "train_m.tsv", "test_m.tsv"]:
        file_path = folder_path / file_name

        if file_path.exists():
            df = pd.read_csv(file_path, sep='\t', low_memory=False)

            # Assign dataframes for dev, test, train
            if "dev_m.tsv" == file_name:
                dev = df
            elif "test_m.tsv" == file_name:
                test = df
            elif "train_m.tsv" == file_name:
                train = df
        else:
            print(f"File not found: {file_name}")

    # Ensure we have dataframes for dev, test, train
    if dev is not None and test is not None and train is not None:
        # Combine the data into a single DataFrame with an additional 'dataset' column
        dev['dataset'] = 'Dev'
        train['dataset'] = 'Train'
        test['dataset'] = 'Test'

        # Concatenate the datasets
        combined_df = pd.concat([dev[['duration[ms]', 'dataset']], 
                                 train[['duration[ms]', 'dataset']], 
                                 test[['duration[ms]', 'dataset']]])

        # Plot the distribution of durations for dev, test, and train using violinplot
        plt.figure(figsize=(10, 6))
        sns.violinplot(x='dataset', y='duration[ms]', data=combined_df)
        plt.title("Duration Distribution (ms) for Dev, Train, and Test")
        plt.ylabel("Duration (ms)")

        # Calculate total duration in hours for each dataset
        dev_total_duration = dev['duration[ms]'].sum() / (1000 * 3600)  # Convert ms to hours
        train_total_duration = train['duration[ms]'].sum() / (1000 * 3600)  # Convert ms to hours
        test_total_duration = test['duration[ms]'].sum() / (1000 * 3600)  # Convert ms to hours
        dev_nbr_samples = dev.shape[0]
        train_nbr_samples = train.shape[0]
        test_nbr_samples = test.shape[0]
        
        # Add total duration text annotations on the plot
        plt.text(0, 1000, f"{dev_total_duration:.2f} hrs", 
                 horizontalalignment='center', fontsize=12, color='red')
        plt.text(1, 1000, f"{train_total_duration:.2f} hrs", 
                 horizontalalignment='center', fontsize=12, color='red')
        plt.text(2, 1000, f"{test_total_duration:.2f} hrs", 
                 horizontalalignment='center', fontsize=12, color='red')
        plt.text(0, 12000, f"{dev_nbr_samples} smpls", 
                 horizontalalignment='center', fontsize=12, color='red')
        plt.text(1, 12000, f"{train_nbr_samples} smpls", 
                 horizontalalignment='center', fontsize=12, color='red')
        plt.text(2, 12000, f"{test_nbr_samples} smpls", 
                 horizontalalignment='center', fontsize=12, color='red')
        
        # Save the plot as .svg
        plt.savefig(folder_path / "duration_distribution.svg", format='svg')
        
        # Display the plot
        #plt.show()
        plt.close()
        print(f"Total duration for Dev: {dev_total_duration:.2f} hours")
        print(f"Total duration for Train: {train_total_duration:.2f} hours")
        print(f"Total duration for Test: {test_total_duration:.2f} hours")

        return dev, test, train
    else:
        print("One or more dataset files are missing.")
        return None, None, None

   
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--dir", type=str, required=True, help='Directory containing the data')
    args = parser.parse_args()

    # Use glob to find all subdirectories inside the given directory
    directories = sorted(glob.glob(os.path.join(args.dir, '*/')))  # This matches directories under args.dir
    print(directories)
    sleep(3)
    
    # Looperdieloop over all directories
    exception_list = []
    if not directories:
        print(f"No directories found in {args.dir}")
    else:
        print(f"Found {len(directories)} directories.")
        # Iterate over each directory and apply the function
        for directory in directories:
            print("Doing directory ", directory)
            try:
                get_duration(directory)
            except Exception as e:
                print(e)
                print("Exception occured in ", directory)
                exception_list.append(directory)
    print(" ")
    print("Exceptions occurred in:")
    print(exception_list)

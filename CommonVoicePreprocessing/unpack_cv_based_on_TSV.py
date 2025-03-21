import tarfile
import os
import glob
import pandas as pd
import time
from argparse import ArgumentParser

def extract_tar_filtered(tar_path, tsv_path):
    """Extract only files listed in a TSV from a large tar archive efficiently."""
    
    # Load valid paths into a set for fast lookup
    df = pd.read_csv(tsv_path, sep='\t', usecols=['path'])
    valid_files = set(df['path'].astype(str))

    with tarfile.open(tar_path, 'r') as tar:
        for member in tar:
            # Remove the leading directory structure
            parts = member.name.split('/')
            
            if len(parts) > 1:  # Ensure it's not a root-level directory
                
                file_name = parts[-1]  
                if file_name in valid_files:
                    # Ensure output directory exists
                    os.makedirs(os.path.join(*parts[1:-1]), exist_ok=True)
            
                    # Extract the file efficiently
                    extracted_file = tar.extractfile(member)
                    if extracted_file:  # Ensure file extraction is successful
                        with open(os.path.join(*parts[1:]), 'wb') as out_f:
                            out_f.write(extracted_file.read())


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--id", type=str, required=True, help='language identifier (i.e. "bas")')
    parser.add_argument("--tsv", type=str, required=True, help='tsv file (i.e. "train_m_short.tsv")')
    args = parser.parse_args()

    identifier = args.id
    tsv = args.tsv
    
    # Each file of common voice is named as follows:
    tarFile = "cv-corpus-20.0-2024-12-06-" + identifier + ".tar.gz"
    failure_flag = False

    # check if isfile
    if os.path.isfile(tarFile):
        print("Found " + tarFile)
    else:
        print("Did not find " + tarFile)
        failure_flag = True
            
    # We will be unpacking based on a certain .tsv: train_m_short.tsv. This file is located in identifier/ folder
    target_tsv = os.path.join(identifier,tsv)
    if os.path.isfile(target_tsv):
        print("Found " + target_tsv)
    else:
        print("Did not find " + target_tsv)
        failure_flag = True

    if failure_flag:
        print("Could not find the necessary files corresponding to identifier " + identifier + " and to .tsv " + target_tsv)
    else:
        print("Extracting clips. This could take a while")
        start = time.time()
        extract_tar_filtered(tarFile, target_tsv)
        end = time.time()
        print("Elapsed time: ", end-start)

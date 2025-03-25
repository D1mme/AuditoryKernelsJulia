import argparse
import pandas as pd
import os

def update_tsv(tsv_file, wavpath, tsv_file_out):
    # Load the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, sep='\t')

    # Check if the "path" column exists
    if "path" not in df.columns:
        raise ValueError("The TSV file does not contain a 'path' column.")

    # Create the "path_wav" column
    df["path_wav"] = df["path"].apply(lambda x: os.path.join(wavpath, os.path.splitext(x)[0] + ".wav"))

    # Save the updated DataFrame back to the TSV file
    df.to_csv(tsv_file_out, sep='\t', index=False)
    print(f"Updated TSV file saved: {tsv_file_out}")

def main():
    parser = argparse.ArgumentParser(description="Update TSV file to include 'path_wav' column.")
    parser.add_argument("--tsv_file", required=True, help="Path to the input TSV file.")
    parser.add_argument("--tsv_file_out", required=True, help="Output path for the tsv file.")
    parser.add_argument("--wavpath", required=True, help="Base path for the WAV files.")

    args = parser.parse_args()

    update_tsv(args.tsv_file, args.wavpath, args.tsv_file_out)

if __name__ == "__main__":
    main()
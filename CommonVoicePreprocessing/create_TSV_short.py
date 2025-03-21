import os
import pandas as pd
from argparse import ArgumentParser
from sklearn.model_selection import train_test_split
import shutil


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--id", type=str, required=True, help='language identifier (i.e. "bas"). Also the name of the folder in which --tsv_in should be stored')
    parser.add_argument("--tsv_in", type=str, required=True, help='tsv file input (i.e. "train_m.tsv")')
    parser.add_argument("--tsv_out", type=str, required=True, help='tsv file in which output is stored (i.e. "train_short_m.tsv")')
    parser.add_argument("--TMIN", type=float, required=False, default=2.0, help='Minimum duration before creating new set')
    parser.add_argument("--TMAX", type=float, required=False, default=10.0, help='Maximum duration new training set (expected value, we do not explicitly enforce this)')
    args = parser.parse_args()

    identifier = args.id
    tsv_in = args.tsv_in
    tsv_out = args.tsv_out
    TMIN = args.TMIN
    TMAX = args.TMAX
    
    failure_flag = False

    # We will first check if the input tsv exists
    target_tsv = os.path.join(identifier,tsv_in)
    tsv_out = os.path.join(identifier,tsv_out)
    if os.path.isfile(target_tsv):
        print("Found " + target_tsv)
    else:
        print("Did not find " + target_tsv)
        failure_flag = True

    # We will now check if it has a column duration[ms]
    df = pd.read_csv(target_tsv,  sep='\t', low_memory=False)
    if 'duration[ms]' not in df.columns:
        print("the input .tsv did not contain column: duration[ms]")
        failure_flag = True
    
    if failure_flag:
        print("Creating short dataset failed for ", identifier, " and file ", tsv_in)
    else:
        duration = df['duration[ms]'].sum()/(1000*3600)
        n_samples = len(df['duration[ms]'])
        if duration < TMIN:
            print("Duration ", identifier, " shorter than TMIN: ", duration , " < ", TMIN)
        elif duration > TMAX:
            print("Duration ", identifier, " larger than TMAX: ", duration , " > ", TMAX)
            percentage = TMAX/duration

            print("Creating shorter set...")
            df_train, df_temp = train_test_split(df, test_size=(1 - percentage), random_state=0, shuffle = False)
            df_train.to_csv(tsv_out, index=False, sep="\t")
            resulting_duration = df_train['duration[ms]'].sum()/(1000*3600)
            print("Stored ", tsv_out,". Duration: ", resulting_duration, " h")
        else:
            print("Duration between TMIN, TMAX: ", TMIN, " < ", duration, " < ", TMAX)
            print("Copying ", target_tsv, " to ", tsv_out)
            shutil.copy2(target_tsv, tsv_out)  # Preserve metadata
            print("Stored ", tsv_out,". Duration: ", duration, " h")
            
    print(" ")

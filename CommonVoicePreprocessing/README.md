order:
(0) down_cv.py;                 run locally. Downloads common voice 20.
(1) unpack_tsv.py; 			    extracts only the .tsv files. These files contain data about the training, testing and development splits
(2) create_test_dev_train.py;	apply to directory containing all common voice files. Creates the files test_m, dev_m and train_m (.tsv). These contain also the durations of the file
(3) dataset_statistics.py;		apply to each language. Stores a .svg containing data about the distribution in terms of duration, total duration, etc.
(4) create_TSV_short.py;        apply to each language. Creates a .tsv with a limited duration (training) set if the total length of training set is longer than TMAX (10 hrs). No set is created if the trianing time is shorter than TMIN (2 hrs). Can also be used for dev and test sets (but with different TMAX TMIN parameters)
    NOTE: (4) is efficiently done using bash_create_tsv_short.sh
(5) unpack_cv_based_on_TSV.py:  apply to each language. Creates the folder clips within the folder with the language ID. Unpacks the data based on the .tsv (i.e. the one created by (4).
created if total length is smaller than TMIN (2 hrs). 
(6) MP3_to_wav.py:              apply to each language. Creates the folder clips_wav containing the same files as clips but as 16 kHz filtered .wav (filter passband from 100 to 6000 Hz)
(7) update_TSV_to_include_wav.py:       apply to each language. Adds column `path_wav` with the path to the wav-file to the .tsv (i.e. /scratch/ddegroot/CommonVoice20/<LanID>/clips_wav/1234.wav




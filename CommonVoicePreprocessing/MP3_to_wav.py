import argparse
import glob
import os
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import firwin, lfilter


def is_mono(audio):
    return len(audio.shape) == 1


def band_pass_filter(audio, lowcut, highcut, fs, numtaps=512):
    fir_coeff = firwin(numtaps, [lowcut, highcut], fs=fs, pass_zero='bandpass')
    filtered_audio = lfilter(fir_coeff, 1.0, audio)
    return filtered_audio


def resample_audio(audio, orig_sr, target_sr):
    return librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)


def process_mp3_to_wav(input_dir, output_dir, lowcut_freq, highcut_freq):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mp3_files = glob.glob(os.path.join(input_dir, "*.mp3"))
    for mp3_file in mp3_files:
        try:
            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(mp3_file))[0] + ".wav")
            if os.path.exists(output_file):
                print(f"Skipping {mp3_file}: WAV file already exists")
                continue

            # Load MP3 file
            audio, sr = librosa.load(mp3_file, sr=None, mono=False)
            
            # Check if audio is mono
            if not is_mono(audio):
                print(f"Skipping {mp3_file}: not mono")
                continue
            
            # Apply band-pass filter
            filtered_audio = band_pass_filter(audio, lowcut_freq, highcut_freq, sr)
            
            # Resample to 16 kHz
            target_sr = 16000
            resampled_audio = resample_audio(filtered_audio, sr, target_sr)
            
            # Save as WAV
            sf.write(output_file, resampled_audio, target_sr)
            print(f"Processed and saved: {output_file}")
        except Exception as e:
            print(f"Error processing {mp3_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process MP3 files to WAV with filtering and resampling.")
    parser.add_argument("--input_dir", type=str, help="Directory containing MP3 files.")
    parser.add_argument("--output_dir", type=str, help="Directory to save processed WAV files.")
    parser.add_argument("--lowcut_freq", type=float, default=100.0, help="Low cutoff frequency for band-pass filter (Hz).")
    parser.add_argument("--highcut_freq", type=float, default=6000.0, help="High cutoff frequency for band-pass filter (Hz).")
    args = parser.parse_args()

    process_mp3_to_wav(args.input_dir, args.output_dir, args.lowcut_freq, args.highcut_freq)

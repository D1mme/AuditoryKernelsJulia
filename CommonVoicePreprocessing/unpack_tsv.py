import tarfile
import os
import glob

def extract_tar_filtered(tar_path):
    with tarfile.open(tar_path, 'r') as tar:
        for member in tar: # More efficients than: for member in tar.getmembers(), since only one member is grabbed per iteration, and we only need the first few members. 
            # Check if the file is a .tsv file
            if member.name.endswith('.tsv'):
                # Remove the leading directory structure
                parts = member.name.split('/')
                if len(parts) > 1:  # Ensure there's a nested structure
                    new_name = os.path.join(*parts[1:])  # Skip the first directory
                    member.name = new_name  # Rename before extraction
                tar.extract(member)
            elif member.name.endswith('.mp3'):
                print(f"Found first .mp3 file: {member.name}, stopping extraction.")
                break

# Use glob to find all tar files
tar_list = sorted(glob.glob("*.tar.gz"))
print("Number of files to unzip: ", len(tar_list))

# Extract
for tarFile in tar_list:
    print("Extracting", tarFile)
    extract_tar_filtered(tarFile)

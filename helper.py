import os
import platform
import urllib.request
import zipfile
import tarfile
import shutil

def get_exiftool(base_path):
    """
    Detects OS, downloads the appropriate ExifTool binary, and extracts it.
    """
    bin_dir = os.path.join(base_path, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    system = platform.system()
    
    # Define paths and URLs based on OS
    if system == "Windows":
        target_path = os.path.join(bin_dir, "exiftool.exe")
        url = "https://exiftool.org/exiftool-13.58_64.zip"
        is_zip = True
    elif system == "Linux" or system == "Darwin": # Linux or macOS
        target_path = os.path.join(bin_dir, "exiftool")
        url = "https://exiftool.org/Image-ExifTool-13.58.tar.gz"
        is_zip = False
    else:
        print(f"Unsupported OS: {system}")
        return None

    if os.path.exists(target_path):
        return target_path

    print(f"--- T3MN Comfy: Downloading ExifTool for {system} ---")
    
    archive_path = os.path.join(bin_dir, "temp_archive")
    
    try:
        # 1. Download
        urllib.request.urlretrieve(url, archive_path)
        
        # 2. Extract
        if is_zip:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(bin_dir)
            # The zip contains 'exiftool(-k).exe', rename it for script use
            raw_exe = os.path.join(bin_dir, "exiftool(-k).exe")
            if os.path.exists(raw_exe):
                os.rename(raw_exe, target_path)
        else:
            with tarfile.open(archive_path, "r:gz") as tar_ref:
                tar_ref.extractall(bin_dir)
            # For Linux/Mac, point to the perl execution script
            # and ensure it's executable
            source_folder = os.path.join(bin_dir, "Image-ExifTool-13.58")
            shutil.move(os.path.join(source_folder, "exiftool"), target_path)
            os.chmod(target_path, 0o755) 

        print(f"--- T3MN Comfy: ExifTool Ready ---")
        
    except Exception as e:
        print(f"Error downloading ExifTool: {e}")
        return None
    finally:
        if os.path.exists(archive_path):
            os.remove(archive_path)
            
    return target_path
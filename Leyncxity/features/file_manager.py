import os
import glob

def find_file(filename):
    """Search for a file on the PC, prioritizing common locations."""
    user_home = os.path.expanduser("~")
    priority_paths = [
        os.path.join(user_home, "Desktop"),
        os.path.join(user_home, "Downloads")
    ]
    
    matches = []
    # Check priority paths first
    for path in priority_paths:
        if os.path.exists(path):
            # Shallow search first in priority folders
            for root, dirs, files in os.walk(path):
                for f in files:
                    if filename.lower() == f.lower():
                        matches.append(os.path.join(root, f))
                if matches: break # Stop if found in priority
        if matches: break

    # If not found, do a broader search
    if not matches:
        for root, dirs, files in os.walk(user_home):
            # Skip priority paths since already checked
            if any(priority in root for priority in priority_paths):
                continue
            if filename.lower() in [f.lower() for f in files]:
                matches.append(os.path.join(root, filename))
                if len(matches) > 3: break
    return matches

def create_file(path, content=""):
    """Create a new file with optional content."""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        return str(e)

def rename_file(old_path, new_path):
    """Rename/Move a file."""
    try:
        os.rename(old_path, new_path)
        return True
    except Exception as e:
        return str(e)

def delete_file(path):
    """Delete a file."""
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
        else:
            return "File not found."
    except Exception as e:
        return str(e)

def list_directory(path):
    """List all files and folders in a directory."""
    try:
        # Expand user path if it starts with ~
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            items = os.listdir(path)
            # Separate files and folders for better AI handling
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]
            folders = [d for d in items if os.path.isdir(os.path.join(path, d))]
            return {"files": files, "folders": folders}
        else:
            return "Not a valid directory."
    except Exception as e:
        return str(e)

def find_folder(foldername):
    """Search for a directory on the PC, prioritizing common locations."""
    user_home = os.path.expanduser("~")
    priority_paths = [
        os.path.join(user_home, "Desktop"),
        os.path.join(user_home, "Downloads")
    ]
    
    matches = []
    for path in priority_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                if foldername.lower() in [d.lower() for d in dirs]:
                    matches.append(os.path.join(root, foldername))
                if matches: break
        if matches: break

    if not matches:
        for root, dirs, files in os.walk(user_home):
            if any(priority in root for priority in priority_paths):
                continue
            if foldername.lower() in [d.lower() for d in dirs]:
                matches.append(os.path.join(root, foldername))
                if len(matches) > 3: break
    return matches

def create_folder(path):
    """Create a new folder."""
    try:
        path = os.path.expanduser(path)
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        return str(e)

def delete_folder(path):
    """Delete a folder and its contents."""
    import shutil
    try:
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
            return True
        else:
            return "Folder not found."
    except Exception as e:
        return str(e)

def open_folder(path):
    """Open a folder in the OS file explorer."""
    try:
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            os.startfile(path)
            return True
        else:
            return "Folder not found."
    except Exception as e:
        return str(e)

def format_size(size_bytes):
    """Convert bytes to human-readable format."""
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def get_path_info(path):
    """Get metadata and size of a file or folder."""
    import time
    try:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return "Path not found."
        
        is_dir = os.path.isdir(path)
        stats = os.stat(path)
        
        info = {
            "name": os.path.basename(path),
            "type": "folder" if is_dir else "file",
            "created": time.ctime(stats.st_ctime),
            "modified": time.ctime(stats.st_mtime),
            "readable_path": path
        }

        if is_dir:
            total_size = 0
            file_count = 0
            for root, dirs, files in os.walk(path):
                file_count += len(files)
                for f in files:
                    fp = os.path.join(root, f)
                    total_size += os.path.getsize(fp)
            info["size_bytes"] = total_size
            info["size_human"] = format_size(total_size)
            info["file_count"] = file_count
        else:
            size = stats.st_size
            info["size_bytes"] = size
            info["size_human"] = format_size(size)
            
        return info
    except Exception as e:
        return str(e)

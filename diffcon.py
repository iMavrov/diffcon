import os
import json
from collections import deque
import hashlib

snapshot = []

def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def handle_file(file):
  metadata = file.stat(follow_symlinks=False)
  last_modified = metadata.st_mtime

  checksum = calculate_checksum(file.path)

  snapshot.append((file.path, last_modified, checksum))


def traverse(root, skip_directories=[]):
    root = os.path.abspath(root)
    if not os.path.exists(root) or not os.path.isdir(root):
        return
    
    directories = deque([root])
    while directories:
      directory = directories.popleft()
      if directory in skip_directories:
         continue  
      with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                directories.append(entry.path)
            elif entry.is_file(follow_symlinks=False):
              handle_file(entry)


def main():
    # config = json.load("config.json")
    root = "/home/mavrov/Downloads"
    traverse(root)
    print(snapshot)


if __name__ == "__main__":
    main()

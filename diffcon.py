import argparse
from collections import deque
import hashlib
import json
import os
import time

class Snapshot:

  def __init__(self):
    self.snapshot = {}

  def add(self, root, skip_directories=[]):
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
            self.handle_file(entry)

  def dump(self, output_directory):
    timestamp = int(time.time())
    file_name = 'snapshot-{}.json'.format(timestamp)
    file_path = os.path.join(output_directory, file_name)
    with open(file_path, 'w') as file:
      json.dump(self.snapshot, file)

  def load(self, snapshot_file_path):
    with open(snapshot_file_path, 'r') as file:
        self.snapshot = json.load(file)

  def compare(self, older):
    common_items = self.snapshot.keys() & older.snapshot.keys()
    new_items = self.snapshot.keys() - common_items
    deleted_items = older.snapshot.keys() - common_items
    modified_items = set([item for item in common_items if self.snapshot[item][2] != older.snapshot[item][2]])
    return new_items, deleted_items, modified_items
  
  def handle_file(self, file):
    metadata = file.stat(follow_symlinks=False)
    last_modified = metadata.st_mtime
    size = metadata.st_size
    checksum = self.calculate_checksum(file.path)
    self.snapshot[file.path] = (last_modified, size, checksum)

  def calculate_checksum(self, file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
      for chunk in iter(lambda: file.read(4096), b''):
        sha256.update(chunk)
    return sha256.hexdigest()


def main():
  cmd_parser = argparse.ArgumentParser()
  cmd_parser.add_argument('config_path', help='Path to the JSON config file')
  cmd_args = cmd_parser.parse_args()

  config_path = cmd_args.config_path
  if not os.path.exists(config_path):
    print('{} does not exist!'.format(config_path))
  if not os.path.isfile(config_path):
    print('{} is not a file!'.format(config_path))

  snapshot = Snapshot()
  with open(config_path) as config_file:
    config_json = json.load(config_file)
    for root in config_json['roots']:
      snapshot.add(root['path'], root['skip'] if 'skip' in root else [])

  config_directory = os.path.dirname(config_path)
  snapshot.dump(config_directory)

  last_snapshot = Snapshot()
  last_snapshot.load('snapshot-1703894247.json')
  new_items, deleted_items, modified_items = snapshot.compare(last_snapshot)
  print(new_items)
  print(deleted_items)
  print(modified_items)


if __name__ == '__main__':
  main()

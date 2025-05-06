import argparse
import hashlib
import json
import os


def load_snapshot(snapshot_path):
  if not os.path.exists(snapshot_path):
    print('{} does not exist!'.format(snapshot_path))
    return
  if not os.path.isfile(snapshot_path):
    print('{} is not a file!'.format(snapshot_path))
    return

  with open(snapshot_path, 'r') as file:
    snapshot = json.load(file)

  return snapshot


def calculate_hash(file_path):
  if not os.path.exists(file_path):
    print('{} does not exist!'.format(file_path))
    return
  if not os.path.isfile(file_path):
    print('{} is not a file!'.format(file_path))
    return

  sha256 = hashlib.sha256()
  with open(file_path, 'rb') as file:
    for chunk in iter(lambda: file.read(4096), b''):
      sha256.update(chunk)
  return sha256.hexdigest()


def find_content(snapshot, hash):
  return [key for key, value in snapshot.items() if value[2] == hash]


def main():
  cmd_parser = argparse.ArgumentParser()
  cmd_parser.add_argument('snapshot_path', help='Path to the JSON snapshot file')
  cmd_parser.add_argument('file_path', help='Path to the file to look for')
  cmd_args = cmd_parser.parse_args()

  snapshot = load_snapshot(cmd_args.snapshot_path)
  hash = calculate_hash(cmd_args.file_path)
  matches = find_content(snapshot, hash)

  print('Find results: {}'.format(matches))


if __name__ == '__main__':
  main()

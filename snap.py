import argparse
import json
import os

from snapshot import Snapshot


def main():
  cmd_parser = argparse.ArgumentParser()
  cmd_parser.add_argument('config_path', help='Path to the JSON config file')
  cmd_args = cmd_parser.parse_args()

  config_path = cmd_args.config_path
  if not os.path.exists(config_path):
    print('{} does not exist!'.format(config_path))
    return
  if not os.path.isfile(config_path):
    print('{} is not a file!'.format(config_path))
    return

  new_snapshot = Snapshot()
  with open(config_path) as config_file:
    config_json = json.load(config_file)
    for root in config_json['roots']:
      new_snapshot.add(root['path'], root['skip'] if 'skip' in root else [])

  config_directory = os.path.dirname(config_path)
  new_snapshot.dump(config_directory)


if __name__ == '__main__':
  main()

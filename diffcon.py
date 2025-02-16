import argparse
import os

from snapshot import Snapshot


def load_snapshot(snapshot_path):
  if not os.path.exists(snapshot_path):
    print('{} does not exist!'.format(snapshot_path))
  if not os.path.isfile(snapshot_path):
    print('{} is not a file!'.format(snapshot_path))
  new_snapshot = Snapshot()
  new_snapshot.load(snapshot_path)
  return new_snapshot


def main():
  cmd_parser = argparse.ArgumentParser()
  cmd_parser.add_argument('new_snapshot', help='Path to the newer snapshot')
  cmd_parser.add_argument('old_snapshot', help='Path to the older snapshot')
  cmd_args = cmd_parser.parse_args()

  new_snapshot = load_snapshot(cmd_args.new_snapshot)
  old_snapshot = load_snapshot(cmd_args.old_snapshot)

  new_items, deleted_items, modified_items = new_snapshot.compare(old_snapshot)
  print(new_items)
  print(deleted_items)
  print(modified_items)


if __name__ == '__main__':
  main()

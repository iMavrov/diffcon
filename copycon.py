import argparse
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


def find_collisions(snapshot):
  collisions = {}
  for key, value in snapshot.items():
    hash = value[2]
    if hash in collisions:
      collisions[hash].append(key)
    else:
      collisions[hash] = [key]
  return collisions


def cluster_candidates(snapshot, candidates):
  sizes = set([snapshot[candidate][1] for candidate in candidates])
  if len(sizes) == 1:
    print(candidates)

  for size in sizes:
    same_size_candidates = []
    for candidate in candidates:
      if snapshot[candidate][1] == size:
        same_size_candidates.append(candidate)
    print(same_size_candidates)


def main():
  cmd_parser = argparse.ArgumentParser()
  cmd_parser.add_argument('snapshot_path', help='Path to the JSON snapshot file')
  cmd_args = cmd_parser.parse_args()

  snapshot = load_snapshot(cmd_args.snapshot_path)

  collisions = find_collisions(snapshot)

  for hash, candidates in collisions.items():
    if 1 < len(candidates):
      cluster_candidates(snapshot, candidates)


if __name__ == '__main__':
  main()

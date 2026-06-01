#!/usr/bin/env python3

from pathlib import Path
import sys


"""Find redundant items in domain lists.

For example, ``bar.foo.com`` is redundant when ``foo.com`` already exists.
"""


def load_domains(path):
    results = []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            domain_labels = line.lower().split('.')
            results.append(domain_labels)

    results.sort(key=len)
    return results


def find_redundant_domains(label_sets):
    tree = {}
    leaf = object()
    redundant_domains = []

    for labels in label_sets:
        domain = '.'.join(labels)
        node = tree
        pending_labels = list(labels)

        while pending_labels:
            label = pending_labels.pop()
            if label in node:
                if node[label] is leaf:
                    redundant_domains.append(domain)
                    break
            else:
                if pending_labels:
                    node[label] = {}
                else:
                    node[label] = leaf
            node = node[label]

    return redundant_domains


def main(argv):
    if len(argv) != 3:
        print(f"Usage: {argv[0]} INPUT_LIST OUTPUT_LIST", file=sys.stderr)
        return 2

    redundant_domains = find_redundant_domains(load_domains(argv[1]))
    with Path(argv[2]).open("w", encoding="utf-8") as f:
        for domain in redundant_domains:
            f.write(f"{domain}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

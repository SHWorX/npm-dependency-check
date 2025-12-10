#!/usr/bin/python3

# Project: NPM Dependency Check
# File: dependency-check.py
# Date: 26.11.2025
# Copyright: 2025 Steffen Haase <shworx.development@gmail.com>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import csv
import json
import sys
from pathlib import Path

def load_csv(csv_path):
    packages = {}
    with open(csv_path, newline="", encoding="utf8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue

            pkg = row[0].strip()
            versions = [v.strip() for v in row[1].split("||")]

            packages[pkg] = versions
    return packages


def walk_dependencies(node, found, packages_to_check):
    """Recursively walk dependency tree."""
    deps = node.get("dependencies", {})
    for name, info in deps.items():
        installed_version = info.get("version")

        if name in packages_to_check:
            allowed_versions = packages_to_check[name]
            exact_match = installed_version in allowed_versions

            found.append({
                "package": name,
                "installed": installed_version,
                "allowed": allowed_versions,
                "match": exact_match
            })

        walk_dependencies(info, found, packages_to_check)


def main():
    if len(sys.argv) < 3:
        print("Usage: python check_deps.py <packages.csv> <deps.json>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    deps_path = Path(sys.argv[2])

    if not csv_path.exists() or not deps_path.exists():
        print("CSV or deps.json file not found.")
        sys.exit(1)

    # Load data
    packages_to_check = load_csv(csv_path)
    dependency_tree = json.loads(deps_path.read_text(encoding="utf8"))

    found = []
    walk_dependencies(dependency_tree, found, packages_to_check)

    # Output
    if not found:
        print("No listed packages found in the dependency tree.")
        return

    print("\nResults:")
    for item in found:
        if item["match"]:
            print(
                f"✔ {item['package']}@{item['installed']} "
                f"matches allowed versions ({' OR '.join(item['allowed'])})"
            )
        else:
            print(
                f"✖ {item['package']}@{item['installed']} "
                f"is installed but does NOT match allowed versions "
                f"({' OR '.join(item['allowed'])})"
            )

    print("\nDone.")


if __name__ == "__main__":
    main()
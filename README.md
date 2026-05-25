# NPM Dependency Check
This tool checks if installed NPM dependencies match against a provided list of packages, which are infected by the Shai-Hulud NPM worm.

## VERY IMPORTANT NOTE
\########################################################################

This repository has moved to **CODEBERG.ORG**.
The repository here on Github will **NOT RECEIVE ANY UPDATES ANYMORE**.
The repository here on Github is now **ARCHIVED AND READ-ONLY**.

**NEW REPOSITORY URL:** [https://codeberg.org/SHWorX/npm-dependency-check](https://codeberg.org/SHWorX/npm-dependency-check)

\########################################################################


## Usage
1. Generate a list of all installed dependencies:<br>
   `npm ls --all --json > deps.json`
2. Copy the generated `deps.json` file into the root of this tool.
2. Execute `dependency_check.py`:<br>
   `python dependency_check.py shai-hulud-2-packages.csv deps.json`

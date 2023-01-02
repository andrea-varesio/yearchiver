# ⚠️ WARNING ⚠️
This project is no longer being maintained. Use at your own risk.

# yearchiver

## What is it
This script will search all subdirectories within the specified root folder, and then sort files by year by moving them into automatically created directories.

It can be useful for archiving photos, media or any other file, as you can easily move files by extension.

## Requirements
Install python requirements with: `pip install -r requirements.txt`

## How to use it
You can either place this script into the desired root folder or run it from anywhere and pass `-i /path/to/input-dir` and eventually `-o /path/to/output-dir` if you want to change where the files will be moved to. Full usage below.

Usage:
```
yearchiver.py [-h] [-i INPUT] [-o OUTPUT] [-q] [-a | -m | -f FILTER | --advanced-filter] [--dry-run]
```

Short | Argument | Info
---|---|---
`-h` | `--help` | show this help message and exit
`-i INPUT` | `--input INPUT` | Specify input directory
`-o OUTPUT` | `--output OUTPUT` | Specify output directory
`-q` | `--quiet` | Disable prompts and verbosity
`-a` | `--all` | Archive all files, regardless of extension
`-m` | `--media` | Archive files matching media extensions (default)
`-f FILTER` | `--filter FILTER` | Only archive files matching this extension (ie .png)
/ | `--advanced-filter` | Select file extensions to process through a prompt
/ | `--dry-run` | Visually display what files would be moved, without making any changes


## Contributions
Contributions are welcome and appreciated, feel free to submit issues and/or pull requests.

## LICENSE

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

"yearchiver" - Automatically sort files into folders by year.<br />
Copyright (C) 2023 Andrea Varesio <https://www.andreavaresio.com/>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a [copy of the GNU General Public License](https://github.com/andrea-varesio/yearchiver/blob/main/LICENSE)
along with this program.  If not, see <https://www.gnu.org/licenses/>.

<div align="center">
<a href="https://github.com/andrea-varesio/yearchiver/">
  <img src="http://hits.dwyl.com/andrea-varesio/yearchiver.svg?style=flat-square" alt="Hit count" />
</a>
</div>

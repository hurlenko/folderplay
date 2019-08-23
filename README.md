# folderplay

[![Latest Github release](https://img.shields.io/github/release/hurlenko/folderplay.svg)](https://github.com/hurlenko/folderplay/releases/latest)
![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
<!-- [![PyPI version](https://img.shields.io/pypi/v/edlib.svg)](https://pypi.python.org/pypi/edlib) -->
[![Build Status](https://dev.azure.com/hurlenko/folderplay/_apis/build/status/hurlenko.folderplay?branchName=master)](https://dev.azure.com/hurlenko/folderplay/_build/latest?definitionId=1&branchName=master)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/hurlenko/folderplay.svg)](https://github.com/hurlenko/folderplay/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/hurlenko/folderplay.svg)](https://github.com/hurlenko/folderplay/pulls)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-default.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**folderplay** is a small tool that helps you remember watched tv episodes. Its goal is to resume playback from the episode you left off with a single button press. It doesn't use any integrated players so you can still use your favourite one.

## Basic view

![image](https://user-images.githubusercontent.com/18035960/63596332-adff6000-c5c3-11e9-9174-0c3b5a75d48f.png)

## Advanced view

![image](https://user-images.githubusercontent.com/18035960/63596754-9ecce200-c5c4-11e9-8012-8ce539e36470.png)

## 🚩 Table of Contents

- [Features](#features)
- [Installation](#-installation)
  - [Compiled binary](#using-precompiled-binaries)
  - [PyPi](#using-pypi)
- [Usage](#-usage)
- [Building](#-building)
- [Command line interface](#command-line-interface)

## 🎨 Features

- Continue playback with a single button press.
- Play with your favoure video player
- Filter and search your playlist
- Displays general media info
- Supports basic [command line interface](#command-line-interface)
- Minimalistic GUI
- No dependencies
- No installation required - the whole program is a single executable file
- Cross platform - supports all three major platforms (Windows, MacOS, Linux) thanks to `python` and `pyqt`

## 💾 Installation

### Using precompiled binaries

Just go to the [releases](https://github.com/hurlenko/folderplay/releases) page and download the latest version for your platform.

### Using PyPi

Use following command to download the latest version from PyPi:

```bash
pip install folderplay
```

Note, currently only `python3.7` is supported.

## 📙 Usage

Simply drop the executable into the directory where you media resides and run it. The application will scan all directories and subdirectories for known extensions.

By default the app runs in `basic` view mode. You can toggle to the more advanced view by pressing the gear button. From there you can select the video player to use (`folderplay` will try to search for existing video players and will warn you on start up if it didn't find one).

You can filter your media list using the search form. The list also has supports context menu with some handy commands.

## 🔨 Building

Clone master branch or checkout a specific tag

```bash
git clone https://github.com/hurlenko/folderplay.git
```

Create new virtual environment inside of the `folderplay` directory

```bash
python3.7 -m venv venv

source venv/bin/activate # Linux / MacOs

venv\Scripts\activate # Windows
```

Install dependencies

```bash
pip install -r requirements.txt
```

Now either run the application

```bash
python -m folderplay
```

Or create an executable (will be save inside of the `dist` directory)

```bash
python -m PyInstaller folderplay.spec
```

## Command line interface

Currently `folderplay` supports these commands

```bash
Usage: folderplay [OPTIONS]

Options:
    --version                  Show the version and exit.
    -w, --workdir <directory>  Working directory
    -p, --player <path>        Host player binary
    --help                     Show this message and exit.
```

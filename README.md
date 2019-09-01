# folderplay

[![PyPI version](https://img.shields.io/pypi/v/folderplay.svg)](https://pypi.python.org/pypi/folderplay)
[![Latest Github release](https://img.shields.io/github/release/hurlenko/folderplay.svg)](https://github.com/hurlenko/folderplay/releases/latest)
![Python](https://img.shields.io/badge/python-v3.5+-blue.svg)
[![Build Status](https://dev.azure.com/hurlenko/folderplay/_apis/build/status/hurlenko.folderplay?branchName=master)](https://dev.azure.com/hurlenko/folderplay/_build/latest?definitionId=1&branchName=master)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## **folderplay** is a small tool that helps you remember watched tv episodes :sparkles:

![image](https://user-images.githubusercontent.com/18035960/64080320-5b2c5380-ccfb-11e9-808f-c370ca7951c2.png)

Its goal is to resume playback from the episode you left off with a single button press. It doesn't use any integrated players so you can still use your favourite one.

## Advaced view

![image](https://user-images.githubusercontent.com/18035960/64080371-0e954800-ccfc-11e9-965f-7910966da277.png)

## 🚩 Table of Contents

- [Features](#-features)
- [How it works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [Building](#-building)
- [Command line interface](#%EF%B8%8F-command-line-interface)
- [Credits](#credits)

## 🎨 Features

- Continue playback with a single button press
- Play with your favoure video player
- Filter and search your playlist
- Displays general media info
- Supports basic [command line interface](#%EF%B8%8F-command-line-interface)
- Minimalistic GUI
- Supports multiple color styles
- Supports multiple icon sets
- No dependencies
- No installation required - the whole program is a single executable file
- Cross platform - supports all three major platforms (Windows, MacOS, Linux) thanks to `python` and `pyqt`

## ⚙️ How it works

`folderplay` scans for known extensions in the current working directory and all subdirectories. It marks the files as `watched` or `unwatched` by checking for a specific prefix in the filename. It also searches for a list of predefined players for current operating systems. If the application can't find one, it will throw a warning and will ask you to select the player. When you hit the play button `folderplay` spawns a new process with the selected player, freezes the UI and waits for the process to exit. When the playes process exits `folderplay` will rename the media file by prepending a prefix to its filename to mark it as watched.

## 💾 Installation

Prebuilt binaries for macOS and Windows can be downloaded from the [GitHub releases page](https://github.com/hurlenko/folderplay/releases).

:warning: Note that the binaries were not thoroughly tested across different platforms and might not work correctly.

The recommended installation method is using `pip`:

```bash
pip install folderplay
```

If you're on Linux, you have to additionally install `libmediainfo-dev`. For Debian-based systems it's as simple as running

```bash
sudo apt-get install libmediainfo-dev
```

After installation, the `fplay` command will be available. Check the [command line](%EF%B8%8F-command-line-interface) section for supported commands.

## 📙 Usage

Simply drop the executable into the directory where your media resides and run it. The application will scan all directories and subdirectories for known extensions.

By default the app runs in `basic` view mode. You can toggle to the more advanced view by pressing the gear button. From there you can select the video player to use (`folderplay` will try to search for existing video players and will warn you on start up if it didn't find one).

You can filter your media list using the search form. The list also has supports context menu with some handy commands.

## 🔨 Building

Clone master branch or checkout a specific tag

```bash
git clone https://github.com/hurlenko/folderplay.git
```

Create new virtual environment inside of the `folderplay` directory

```bash
python3 -m venv venv

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

## 🖥️ Command line interface

Currently `fplay` supports these commands

```bash
Usage: fplay [OPTIONS] <directory>

Options:
  --version            Show the version and exit.
  -p, --player <path>  Host player binary
  -s, --style <name>   Color style: dark, light, fusion, native
  -i, --icons <name>   Icon set: material, feather
  --help               Show this message and exit.
```

## :octocat: Credits

Work from these open source projects is used by this application

- [qtmodern](https://github.com/gmarull/qtmodern) - PyQt/PySide Widgets Modern User Interface
- [feathericons](https://feathericons.com/) - Simply beautiful open source icons
- [material icons](https://material.io/resources/icons/) - Material icons

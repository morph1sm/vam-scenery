# VaM Scenery

## A scene manager for Virt-A-Mate.

- browse .vac files in a gallery inside VaM
- sort and search .vac files by name
- search .vac files by scene content, e.g. type "breathe" to find all .vacs with scenes that use the Breathe.cs plugin 
- preview .vac files without creating duplicate scene folders
- TODO: install .vac files in a consistent structure to improve referencing scene dependencies
- TODO: analyze and repair intsalled scenes with broken references

## Requirements

- Virta-A-Mate
- Python 3

## Installation

- download the [latest release](//morph1sm/vam-scenery/releases) into your VAM installation, e.g.
  `\VAM\Custom\Mods\`

If you prefer to build the tool yourself, you can also:
- clone this repo into a subfolder of your Vam installation
- run the config.bat
- run the build.bat

## Usage

- run scenery.exe before you run VAM
- in VAM, click the cloud icon in the Quick Panel
- type in `localhost:6969` and click Go
- to autostart VaM Scenery every time VaM is started:
  - click the ellipsis icon in the top right corner
  - check the autostart checkbox for the appropriate mode

# VaM Scenery

## A scene manager for Virt-A-Mate.

- browse all downloaded scenes visually in a gallery inside VaM
- sort and search your scenes
- preview .vac files
- TODO: install .vac files in a consistent structure to improve referencing scene dependencies
- TODO: list your currently installed plugins, assets, textures, etc. and see what
  scenes depend on them
- TODO: move scenes without breaking presets
- TODO: analyze and repair scenes with broken references

## Requirements

Virta-A-Mate
Python 3

## Installation

- download the [latest release](//morph1sm/vam-scenery/releases) into your VAM installation, e.g.
  `\VAM\Custom\Mods\Morph1sm\VAMScenery`

If you prefer to build the tool yourself, you can also:

- clone or download and unzip this repo into any subfolder in your Vam installation
- run the config.bat
- run the build.bat

## Usage

- run scenery.exe before you run VAM
- in VAM, click the cloud icon the Quick Panel
- type in `localhost:6969` and click Go
- to autostart VaM Scenery when VaM is started:
  - click the gear icon in the top right corner
  - check the auto start checkbox for the mode(s) should autostart the gallery

# ESConfigEdit

This program provides the functions for setting or removing system configurations of [EmulationStation](www.emulationstation.org), a graphical front-end.


## Installation

To install this tool, you can download the current release directly from the repository with the command 
```bash
git clone https://github.com/petrockblog/ESConfigEdit.git
```
This downloads the current repository into the folder `ESConfigEdit`. You can make the program executable with the command `chmod +x esconfig.edit.py`.


## Usage

Here is the generic usage information that is also provided from command line:
```bash
usage: esconfedit.py [-h] [-f FULLNAME] [-n NAME] [-d DIRECTORY]
                     [-e EXTENSION] [-c COMMAND] [-p PLATFORM] [-t THEME]
                     {set,remove} inputfile outputfile

Sets or removes system information from system configuration files of
EmulationStation (see emulationstation.org).

positional arguments:
  {set,remove}          Sets the mode
  inputfile             path and name of input XML file
  outputfile            path and name of output XML file

optional arguments:
  -h, --help            show this help message and exit

optional arguments, system-specific::
  -f FULLNAME, --fullname FULLNAME
                        full name of the system
  -n NAME, --name NAME  name of the system
  -d DIRECTORY, --directory DIRECTORY
                        path of the ROMs of the system
  -e EXTENSION, --extension EXTENSION
                        Extensions of the ROMs
  -c COMMAND, --command COMMAND
                        Command to start the emulator with a ROM
  -p PLATFORM, --platform PLATFORM
                        Platform name for EmulationStation
  -t THEME, --theme THEME
                        Theme name for EmulationStation
```

The program can run in various __modes__:

1. __Set mode__: In this mode the program reads _sourcefile_, adds the given system information to it and writes the result to _outputfile_. If a system with the same name already exists, the existing system information are changed.
2. __Remove mode__: In this mode the program reads _sourcefile_, removes the system with the given name, and writes the result to _outputfile_. If the system does not exist, _outputfile_ will have the same content as _inputfile_.


## Example

### Setting System Configurations

Here is an exemplary function call to add/edit a system. Please note that the backslashes:

```
python esconfedit.py -f "Super Nintendo" \
-n "snes2" \
-d "~/RetroPie/roms/snes" \
-e ".smc .sfc .fig .swc .SMC .SFC .FIG .SWC" \
-c "/opt/retropie/supplementary/runcommand/runcommand.sh 4 \"/opt/retropie/emulators/RetroArch/installdir/bin/retroarch -L /opt/retropie/emulatorcores/pocketsnes-libretro/libretro.so --config /opt/retropie/configs/all/retroarch.cfg --appendconfig /opt/retropie/configs/snes/retroarch.cfg %ROM%\"" \
-p "snes" \
-t "snes" \
set es_systems.xml new_es_systems.xml
```


### Removing System Configurations

Here is an exemplary function call to remove a system:

```
python esconfedit.py -n "snes2" remove es_systems.xml new_es_systems.xml
```

If you have any comments or ideas ofr enhancements feel free to post a comment or issue at [https://github.com/petrockblog/ESConfigEdit](https://github.com/petrockblog/ESConfigEdit).


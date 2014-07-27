#!/usr/bin/env python

"""esconfig.py: Sets or removes system information from system configuration \
files of EmulationStation. """

__author__ = "Florian Mueller"
__copyright__ = "Copyright 2014, Florian Mueller"
__credits__ = ["Florian Mueller"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Florian Mueller"
__email__ = "contact@petrockblock.com"

import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
import os.path
import sys


class Systemlist(object):

    REPLENT_TOXML = 0
    REPLENT_FROMXML = 1

    def __init__(self):
        """ Initializes the system as empty list """
        super(Systemlist, self).__init__()
        self.__systemlist = []

    def __iter__(self):
        self.__currentIndex = 0
        if len(self.__systemlist) > 0:
            return self
        else:
            raise StopIteration

    def next(self):
        if self.__currentIndex < len(self.__systemlist):
            self.__currentIndex += 1
            return self.__systemlist[self.__currentIndex - 1]
        else:
            raise StopIteration

    def loadSystems(self, sourcefile):
        self.__sourcefile = sourcefile
        if not os.path.isfile(sourcefile):
            print "Cannot find input file", sourcefile
            sys.exit(1)

        self.__transformEntities(sourcefile, Systemlist.REPLENT_TOXML)
        self.__tree = ET.parse(self.__sourcefile)
        self.__transformEntities(sourcefile, Systemlist.REPLENT_FROMXML)
        self.__root = self.__tree.getroot()
        for system in self.__root.findall('system'):
            self.__systemlist.append(Systementry(system.find('fullname').text,
                                                 system.find('name').text,
                                                 system.find('path').text,
                                                 system.find('extension').text,
                                                 system.find('command').text,
                                                 system.find('platform').text,
                                                 system.find('theme').text))

    def saveSystems(self, targetfile):
        newroot = ET.Element("systemList")
        for system in self.__systemlist:
            system.addToTree(newroot)

        outputfile = open(targetfile, 'w')
        outputfile.write(self.__prettify(newroot))
        outputfile.close()
        self.__transformEntities(targetfile, Systemlist.REPLENT_FROMXML)

    def existsSystem(self, searchname):
        entry = self.__findSystem(searchname)
        if entry is None:
            return None
        else:
            return entry

    def setSystem(self, systementry):
        existingSystem = self.__findSystem(systementry.getName())
        if existingSystem is None:
            self.__systemlist.append(systementry)
        else:
            index = self.__systemlist.index(existingSystem)
            self.__systemlist[index] = systementry

    def removeSystem(self, systemname):
        existingSystem = self.__findSystem(systemname)
        if existingSystem is not None:
            self.__systemlist.remove(existingSystem)

    def __findSystem(self, searchname):
        for system in self.__systemlist:
            if system.getName() == searchname:
                return system
        return None

    def __prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def __transformEntities(self, sourcefile, direction):
        if direction == Systemlist.REPLENT_TOXML:
            replacements = {'&&': '&amp;&amp;'}
        elif direction == Systemlist.REPLENT_FROMXML:
            replacements = {'&amp;&amp;': '&&', '&quot;': '"'}

        with open(sourcefile, "r") as workfile:
            data = workfile.read()
            workfile.close()
        for src, target in replacements.iteritems():
            data = data.replace(src, target)
        outfile = open(sourcefile, 'w')
        outfile.write(data)
        outfile.close()


class Systementry(object):

    ENABLEDTRUE = "True"
    ENABLEDFALSE = "False"

    """docstring for Systementry"""

    def __init__(self, fullname, name, path, extension, command, platform,
                 theme):
        super(Systementry, self).__init__()
        self.__fullname = fullname
        self.__name = name
        self.__path = path
        self.__extension = extension
        self.__command = command
        self.__platform = platform
        self.__theme = theme

    def __str__(self):
        return str(self.__name)

    def __eq__(self, other):
        return self.__name == other.getName()

    def addToTree(self, root):
        newnode = ET.SubElement(root, 'system')
        newsubnode = ET.SubElement(newnode, "fullname")
        newsubnode.text = self.__fullname
        newsubnode = ET.SubElement(newnode, "name")
        newsubnode.text = self.__name
        newsubnode = ET.SubElement(newnode, "path")
        newsubnode.text = self.__path
        newsubnode = ET.SubElement(newnode, "extension")
        newsubnode.text = self.__extension
        newsubnode = ET.SubElement(newnode, "command")
        newsubnode.text = self.__command
        newsubnode = ET.SubElement(newnode, "platform")
        newsubnode.text = self.__platform
        newsubnode = ET.SubElement(newnode, "theme")
        newsubnode.text = self.__theme

    def getFullname(self):
        return self.__fullname

    def getName(self):
        return self.__name

    def getPath(self):
        return self.__path

    def getExtension(self):
        return self.__extension

    def getCommand(self):
        return self.__command

    def getPlatform(self):
        return self.__platform

    def getTheme(self):
        return self.__theme

    def setFullname(self, fullname):
        self.__fullname = fullname
        return True

    def setName(self, name):
        self.__name = name
        return True

    def setPath(self, path):
        self.__path = path
        return True

    def setExtension(self, extension):
        self.__extension = extension
        return True

    def setCommand(self, command):
        self.__command = command
        return True

    def setPlatform(self, platform):
        self.__platform = platform
        return True

    def setTheme(self, theme):
        self.__theme = theme
        return True


def checkArguments(args):
    result = True
    if args.mode == "set":
        if args.fullname is None or args.name is None or \
            args.directory is None or args.extension is None or \
            args.command is None or args.platform is None or args.theme is None:
            result = False
    elif args.mode == "remove":
        if args.name is None:
            result = False
    return result


class Toolparser(object):

    def __init__(self):
        super(Toolparser, self).__init__()
        self.__parser = argparse.ArgumentParser(
            description='Sets or removes system information from system \
                         configuration files of EmulationStation (see \
                         emulationstation.org).')
        self.__parser.add_argument("mode", help="Sets the mode",
                                   choices=["set", "remove"])
        self.__parser.add_argument(
            "inputfile", help="path and name of input XML file")
        self.__parser.add_argument(
            "outputfile", help="path and name of output XML file")
        group = self.__parser.add_argument_group(
            'optional arguments, system-specific:')
        group.add_argument("-f", "--fullname", help="full name of the system")
        group.add_argument("-n", "--name", help="name of the system")
        group.add_argument(
            "-d", "--directory", help="path of the ROMs of the system")
        group.add_argument("-e", "--extension", help="Extensions of the ROMs")
        group.add_argument("-c", "--command",
                           help="Command to start the emulator with a ROM")
        group.add_argument("-p", "--platform",
                           help="Platform name for EmulationStation")
        group.add_argument("-t", "--theme",
                           help="Theme name for EmulationStation")

    def parse_args(self):
        return self.__parser.parse_args()


if __name__ == "__main__":

    parser = Toolparser()
    args = parser.parse_args()

    if args.mode == "set":
        if checkArguments(args):
            systemlist = Systemlist()
            systemlist.loadSystems(args.inputfile)
            entry = Systementry(args.fullname,
                                args.name,
                                args.directory,
                                args.extension,
                                args.command,
                                args.platform,
                                args.theme)
            systemlist.setSystem(entry)
            systemlist.saveSystems(args.outputfile)
            print "Successfully saved to file", args.outputfile
        else:
            print "System arguments are incomplete."

    elif args.mode == "remove":
        if checkArguments(args):
            systemlist = Systemlist()
            systemlist.loadSystems(args.inputfile)
            systemlist.removeSystem(args.name)
            systemlist.saveSystems(args.outputfile)
            print "Removed system " + str(args.name) + " from " +\
                str(args.inputfile)
        else:
            print "System name is missing as argument."

    sys.exit(0)

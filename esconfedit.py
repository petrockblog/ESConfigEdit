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

from lxml import etree
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

    def loadSystems(self, sourcefile, dontstop):
        self.__sourcefile = sourcefile

        self.__assure_path_exists(os.path.dirname(sourcefile))
        if not os.path.isfile(sourcefile):
            if not dontstop:
                print "[" + str(os.path.basename(__file__)) + \
                    "] Cannot find input file", sourcefile
                sys.exit(1)
            else:
                emptyfile = open(sourcefile, "w")
                emptyfile.writelines(["<?xml version=\"1.0\" ?>\n",
                                      "<systemList>\n", "</systemList>"])
                emptyfile.close()

        inputfile = open(sourcefile, 'r')
        xmlstring = inputfile.read()
        inputfile.close()
        xmlstring = self.__transformEntities(
            xmlstring, Systemlist.REPLENT_TOXML)
        xmlparser = etree.XMLParser(encoding='utf-8', recover=True)
        self.__root = etree.XML(xmlstring, parser=xmlparser)
        for system in self.__root.findall('system'):
            self.__systemlist.append(Systementry(system.find('fullname').text,
                                                 system.find('name').text,
                                                 system.find('path').text,
                                                 system.find('extension').text,
                                                 system.find('command').text,
                                                 system.find('platform').text,
                                                 system.find('theme').text))

    def saveSystems(self, targetfile):
        self.__assure_path_exists(os.path.dirname(targetfile))
        if os.path.isfile(targetfile):
            fileName, fileExtension = os.path.splitext(targetfile)
            os.renames(targetfile, str(fileName) + "BAK" +
                       fileExtension)

        newroot = etree.Element("systemList")
        for system in self.__systemlist:
            system.addToTree(newroot)

        prettyxml = self.__prettify(newroot)
        prettyxml = self.__transformEntities(
            prettyxml, Systemlist.REPLENT_FROMXML)
        outputfile = open(targetfile, 'w')
        outputfile.write(prettyxml)
        outputfile.close()

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
        rough_string = etree.tostring(elem)
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def __transformEntities(self, inputstring, direction):
        if direction == Systemlist.REPLENT_TOXML:
            replacements = {'&&': '&#038;&#038;'}
        elif direction == Systemlist.REPLENT_FROMXML:
            replacements = {
                '&amp;&amp;': '&&', '&#038;&#038;': '&&', '&quot;': '"'}

        for src, target in replacements.iteritems():
            inputstring = inputstring.replace(src, target)
        return inputstring

    def __assure_path_exists(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
                os.makedirs(dir)


class Systementry(object):

    """Systementry represents a single entry in the EmulationStation file for \
    the system configurations."""

    ENABLEDTRUE = "True"
    ENABLEDFALSE = "False"

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
        newnode = etree.SubElement(root, 'system')
        newsubnode = etree.SubElement(newnode, "fullname")
        newsubnode.text = self.__fullname
        newsubnode = etree.SubElement(newnode, "name")
        newsubnode.text = self.__name
        newsubnode = etree.SubElement(newnode, "path")
        newsubnode.text = self.__path
        newsubnode = etree.SubElement(newnode, "extension")
        newsubnode.text = self.__extension
        newsubnode = etree.SubElement(newnode, "command")
        newsubnode.text = self.__command
        newsubnode = etree.SubElement(newnode, "platform")
        newsubnode.text = self.__platform
        newsubnode = etree.SubElement(newnode, "theme")
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
        if args.fullname is None or args.name is None or args.directory is None or args.extension is None or args.command is None or args.platform is None or args.theme is None:
            result = False
    elif args.mode == "remove":
        if args.name is None:
            result = False
    return result


class Toolparser(object):

    def __init__(self):
        super(Toolparser, self).__init__()
        self.__parser = argparse.ArgumentParser(
            description='Adds/sets or removes system information from system \
            configuration files of EmulationStation \
            (see emulationstation.org).')
        self.__parser.add_argument("mode", help="Sets the mode",
                                   choices=["add", "remove"])
        self.__parser.add_argument(
            "inputfile", help="path and name of input XML file")
        self.__parser.add_argument(
            "outputfile", help="path and name of output XML file")
        self.__parser.add_argument(
            "--dontstop", help="Do not stop, if inputfile does not exist.\
             Continue with empty systems list then.", action='store_true')
        group = self.__parser.add_argument_group(
            'optional arguments, system-specific')
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

    returnvalue = 0
    parser = Toolparser()
    args = parser.parse_args()

    if args.mode == "add":
        if checkArguments(args):
            systemlist = Systemlist()
            systemlist.loadSystems(args.inputfile, args.dontstop)
            entry = Systementry(args.fullname,
                                args.name,
                                args.directory,
                                args.extension,
                                args.command,
                                args.platform,
                                args.theme)
            systemlist.setSystem(entry)
            systemlist.saveSystems(args.outputfile)
            print "[" + str(os.path.basename(__file__)) + \
                "] Successfully saved to file " + str(args.outputfile)
            returnvalue = 0
        else:
            print "[" + str(os.path.basename(__file__)) + \
                "] System arguments are incomplete."
            returnvalue = 1

    elif args.mode == "remove":
        if checkArguments(args):
            systemlist = Systemlist()
            systemlist.loadSystems(args.inputfile)
            systemlist.removeSystem(args.name)
            systemlist.saveSystems(args.outputfile)
            print "[" + str(os.path.basename(__file__)) + \
                "] Removed system " + str(args.name) + " from " +\
                str(args.inputfile)
        else:
            print "[" + str(os.path.basename(__file__)) + \
                "] System name is missing as argument."
            returnvalue = 1

    sys.exit(returnvalue)

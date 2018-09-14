#!/bin/python
import argparse
import re
import pdb

def notEmptyLine(line):
    if re.search("^\s*$", line):
        return False
    return True

def lineToStruct(line):
#    pdb.set_trace()
    fullyQualifiedClassName = line[7:-2]
    words = fullyQualifiedClassName.split(".")
    className = words[-1]
    packageName = ".".join(words[:-1])
    return [packageName, className]

parser = argparse.ArgumentParser()
parser.add_argument("outputDirectory")
arguments = parser.parse_args();
if arguments.outputDirectory[-1] == "/":
    outputDirectory = arguments.outputDirectory[:-1]
else:
    outputDirectory = arguments.outputDirectory
with open("missing_classes") as missing_classfile:
    missing_class_lines = missing_classfile.readlines()

nonempty_class_lines = filter(notEmptyLine, missing_class_lines)
packages_and_classes = map(lineToStruct, nonempty_class_lines)

for p in packages_and_classes:
    lines = ["package "+p[0]+";", "", "public class "+p[1]+ " {", " }"]
    with open(outputDirectory+"/"+ p[1] + ".java", "w+") as generated_sourcefile:
        generated_sourcefile.write("\n".join(lines))




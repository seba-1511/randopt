#!/usr/bin/env python3

"""
Modification of the following gist: 

https://gist.github.com/dvirsky/30ffbd3c7d8f37d4831b30671b681c24

Usage:
    ./gendocs.py my.module 
    ./gendocs.py my.module SpecificClassToDocument

"""

import pydoc
import os, sys

module_header = "# {} Documentation\n"
class_header = "## Class {}"
function_header = "### {}"


def getmarkdown(module, class_to_doc=None):
    if class_to_doc is None:
        output = [module_header.format(module.__name__) ]
    else:
        output = [module_header.format(class_to_doc) ]
    
    if module.__doc__:
        output.append(module.__doc__)
    
    output.extend(getclasses(module, class_to_doc))
    return "\n".join((str(x) for x in output))

def getclasses(item, class_to_doc=None):
    output = list()
    for cl in pydoc.inspect.getmembers(item, pydoc.inspect.isclass):

        if class_to_doc is None:
            if cl[0] != "__class__" and not cl[0].startswith("_"):
                # Consider anything that starts with _ private
                # and don't document it
                output.append(class_header.format(cl[0]))
                # Get the docstring
                output.append(pydoc.inspect.getdoc(cl[1]))
                # Get the functions
                output.extend(getfunctions(cl[1]))
                # Recurse into any subclasses
                output.extend(getclasses(cl[1]))
                output.append('\n')
        else:
            if cl[0] == class_to_doc:
                # Consider anything that starts with _ private
                # and don't document it
                output.append(class_header.format(cl[0]))
                # Get the docstring
                output.append(pydoc.inspect.getdoc(cl[1]))
                # Get the functions
                output.extend(getfunctions(cl[1]))
                output.append('\n')
    return output


def getfunctions(item):
    output = list()
    #print item
    for func in pydoc.inspect.getmembers(item, pydoc.inspect.isfunction):
        
        if func[0].startswith('_'):
            continue

        output.append(function_header.format(func[0].replace('_', '\\_')))

        # Get the signature
        output.append ('```py\n')
        output.append('def %s%s\n' % (func[0], pydoc.inspect.formatargspec(*pydoc.inspect.getargspec(func[1]))))
        output.append ('```\n')

        # get the docstring
        if pydoc.inspect.getdoc(func[1]):
            output.append('\n')
            output.append(pydoc.inspect.getdoc(func[1]))

        output.append('\n')
    return output

def generatedocs(module, class_to_doc=None):
    try:
        sys.path.append(os.getcwd())
        # Attempt import
        mod = pydoc.safeimport(module)
        if mod is None:
           print("Module not found")
        
        # Module imported correctly, let's create the docs
        return getmarkdown(mod, class_to_doc)
    except pydoc.ErrorDuringImport as e:
        print("Error while trying to import " + module)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print(generatedocs(sys.argv[1], sys.argv[2]))
    else:
        print(generatedocs(sys.argv[1]))

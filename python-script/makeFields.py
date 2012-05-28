#!/usr/bin/env python
# $Author$
# $Date$

#import easy to use xml parser called minidom:
from xml.dom.minidom import parse
import sys
import commands
import re

def detectNumericType(type):
    if type.lower() == "number":
        return "long"
        
fields=dict()

def makeFieldDict(filename):  
    dom = parse(filename)
    regions = dom.getElementsByTagName('Region')

    for r in regions:
        if (fields.has_key(r.getAttribute("field")) and 
            fields[r.getAttribute("field")] !=  r.getAttribute("type")):
            print "Conflict Field[%s] type [%s] %s [%s]"%(r.getAttribute("field"),
                fields[r.getAttribute("field")],filename,r.getAttribute("type"))
#			print re.match('.*Date',r.getAttribute("field"))

        else:
            fields[r.getAttribute("field")]=r.getAttribute("type")


existDict = dict()
def readSchema(filename):
    dom = parse(filename)
    exists = dom.getElementsByTagName('field')
    
    for  r in exists:
        existDict[r.getAttribute('name')]=r.getAttribute('type')

def makeOutput(filename):
    for fn in existDict.viewkeys():
        if (fields.has_key(fn)):
            continue

        fields[fn]=existDict[fn]
    
    outFile = open(filename,"w")

    for f in sorted(fields.iterkeys()):
        outFile.write('<field name="%s" type="%s" indexed="true" store="true" />\n' %( f,  fields[f]))

    outFile.close()

def main(args):
    if(len(args)<3):
        print "It needs 'schema.xml' 'contact.xml'..."
        exit()
        
    readSchema(args[1])
 
    args.pop(0); # args 0
    args.pop(0); # args 1

    for arg in args:
        makeFieldDict(arg)

    makeOutput('schema_snapit.xml')
    

if __name__ == '__main__':
    main(sys.argv)

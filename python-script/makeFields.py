#!/usr/bin/env python
# $Author$
# $Date$

#import easy to use xml parser called minidom:
from xml.dom.minidom import parse
import sys


def detectNumericType(type):
    if type.lower() == "number":
        return "long"
        
def main(args):
    if(len(args)<3):
        print "It needs 'contact_format.xml' 'schema.xml'"
        exit()
        
    fileName=args[1]
    dom = parse(fileName)
    regions = dom.getElementsByTagName('Region')
    
    fields=dict()
    for r in regions:
        fields[r.getAttribute("field")]=r.getAttribute("type")
        
    dom = parse(args[2])
    exists = dom.getElementsByTagName('field')
    existDict = dict()
    
    for  r in exists:
        existDict[r.getAttribute('name')]=r.getAttribute('type')
    
    for fn in existDict.viewkeys():
        if (fields.has_key(fn)):
            continue
        
        fields[fn]=existDict[fn]
    
    for f in sorted(fields.iterkeys()):
        print '<field name="%s" type="%s" indexed="true" store="true" />' %( f,  fields[f])

    
if __name__ == '__main__':
    main(sys.argv)
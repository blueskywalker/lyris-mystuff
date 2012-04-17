
#import easy to use xml parser called minidom:
from xml.dom.minidom import parse
import sys

if(len(sys.argv)<3):
    print "It needs 'contact_format.xml' 'schema.xml'"
    exit()
    
fileName=sys.argv[1]
dom = parse(fileName)
regions = dom.getElementsByTagName('Region')

fields=dict()
for r in regions:
    fields[r.getAttribute("field")]=r.getAttribute("type")
    
dom = parse(sys.argv[2])
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
    

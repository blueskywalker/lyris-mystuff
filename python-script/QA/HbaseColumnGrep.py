#!/usr/bin/env python

import sys
#sys.path.append('/home/jerry/Software/gen-py')

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 
import ConfigParser

 
hbaseHost = '10.3.203.146'
#hbaseHost = '10.3.213.149'
#hbaseHost = '10.3.9.18'


def getConfiguration(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    global hbaseHost
    
    hbaseHost = config.get('hosts','hbase')
    
    
def columnGrep(table_name,column,pattern):
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    #print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])

    ret = []
    
    counter=0    
    try:
        while True:
            result=client.scannerGet(scanner)
            
            row=result[0].columns
            for col,val in row.iteritems():
                
                if(col == "%s%s"%(desc_name,column)):
                        
                    if(val.value.find(pattern)!=-1):
                        ret.append(result[0].row)

            counter = counter + 1
            if((counter%1000)==0):
                print "scanning....%d" %(counter)
    except:
        pass
    
    print "total counter is %d"%(counter)
    return ret
    
def printStdout(rows,outputfile):
    
    OUTPUT=sys.stdout
    
    if(outputfile != ""):
        OUTPUT=open(outputfile,"w")
        
    for row in rows:
        print >>OUTPUT, row
    
    
def main(args):
    if(len(args) < 4):
        print "%s tablename column pattern output[option]"%(args[0])
        sys.exit(1)

    tablename=args[1]
    column = args[2]
    pattern = args[3]

    outputfile = ""
    if(len(args)>4):
        outputfile=args[4]
    
    getConfiguration('host.properties')
    
    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    global client
    client = Hbase.Client(protocol)

#    tablename = "%s_%s_master_%s"%(orgId,subOrgId,orgId)

    rowlist = columnGrep(tablename,column,pattern)
    
    print len(rowlist)
    printStdout(rowlist,outputfile)
    
if __name__ == "__main__":
    main(sys.argv)    
    


        


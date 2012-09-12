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
    
    
def rowPrint(table_name):

    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    #print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])

    ret = []
    
    try:
        while True:
            result=client.scannerGet(scanner)
            
            print result[0].row
    except:
        pass
    
    
def printStdout(rows,outputfile):
    
    OUTPUT=sys.stdout
    
    if(outputfile != ""):
        OUTPUT=open(outputfile,"w")
        
    for row in rows:
        print >>OUTPUT, row
    
    
def main(args):
    if(len(args) < 2):
        print "%s tablename" %(args[0])
        sys.exit(1)

    tablename=args[1]

    getConfiguration('host.properties')
    
    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    global client
    client = Hbase.Client(protocol)

#    tablename = "%s_%s_master_%s"%(orgId,subOrgId,orgId)

    rowPrint(tablename)
    
if __name__ == "__main__":
    main(sys.argv)    
    


        


#!/usr/bin/env python

import sys
import solr
import commands
import ConfigParser
import os

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 

#hbaseHost = '10.3.203.146' 
#hbaseHost = '10.3.213.149'

#solrHost = '10.3.202.165'
#solrHost = '10.3.212.141'


def getConfiguration(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    global hbaseHost
    
    hbaseHost = config.get('hosts','hbase')
    
    global solrHost
    solrHost = config.get('hosts','solr')
    

def printRow(row):
    
    for k,v in row[0].columns.iteritems():
        print "%s:%s"%(k,v)


def main(args):
    
    if(len(args) < 2):
        print "%s <verified file> -all"%(args[0])
        sys.exit(1)
    
    filename = args[1]
    opt_all = True if len(args)>2 and args[2] == "-all" else False

    filenamearray = filename.split("_")
    orgId = filenamearray[0]
    subOrgId = filenamearray[1]
    
    getConfiguration('host.properties')

    
    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    global client
    client = Hbase.Client(protocol)
        
    
    tablename = "%s_%s_master_%s"%(orgId,subOrgId,orgId);
    

    for line in open(filename,"r"):
        input=line.strip()
        row=client.getRow(tablename,input)
        print input 
        printRow(row)
        print ""
        if (not opt_all): break

    
    transport.close()

if __name__ == "__main__":
    main(sys.argv)    
    


        


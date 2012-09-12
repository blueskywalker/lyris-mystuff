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
    

    
    
def main(args):
    
    if(len(args)!=2):
        print "%s tableName"%(args[0])
        sys.exit(1)
    
    tablename = args[1]
    
    getConfiguration('host.properties')

    
    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    global client
    client = Hbase.Client(protocol)
        
    
#    tablename = "%s_%s_master_%s"%(orgId,subOrgId,orgId);
    client.disableTable(tablename)
    client.deleteTable(tablename)

    transport.close()

if __name__ == "__main__":
    main(sys.argv)    
    


        


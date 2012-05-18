#!/usr/bin/env python

import sys
#sys.path.append('/home/jerry/Software/gen-py')

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 

 
#hbaseHost = '10.3.203.146'
#hbaseHost = '10.3.9.18'
            
        
def getMasterTables(hbaseHost):
    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Hbase.Client(protocol)

    for table in client.getTableNames():
        if 'master' in table:
            print table

    transport.close()
    
def main(args):
    if(len(args)<2):
        print "%s hbasehost"%(args[0])
        sys.exit(-1)

    getMasterTables(args[1]);

if __name__ == "__main__":
    main(sys.argv)    
    


        


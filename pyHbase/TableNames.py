#!/usr/bin/env python

import sys
#sys.path.append('/home/jerry/Software/gen-py')

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 
import ConfigParser

 
hbaseHost=""

def getConfiguration(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    global hbaseHost
    
    hbaseHost = config.get('hosts','hbase')

def getColumnInfo(table_name):
    
    #coldesc = client.getTableRegions(table_name)

    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])
    #print client.scannerGetList(scanner,1)

    columnInfo=dict()

    
    try:
        while True:
            result=client.scannerGet(scanner)
            row=result[0].columns
            for col,val in row.iteritems():
                if(columnInfo.has_key(col)):
                    columnInfo[col] = columnInfo[col] + 1
                else:
                    columnInfo[col] = 1            
    except:
         pass


    for col in columnInfo.items():
        print col


def getUniqRow(table_name):
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])

    rows=dict()

    counter=0    
    try:
        while True:
            result=client.scannerGet(scanner)
            if rows.has_key(result[0].row):
                rows[result[0].row] = rows[result[0].row] + 1
            else:
                rows[result[0].row] = 1
            
            counter = counter + 1
            if((counter%1000)==0):
                print "scanning....%d" %(counter)
    except:
        pass
    

    return rows;   

    
def getRowsLimit(table_name,no_row):
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    print desc_name
    
    scanner = client.scannerOpen(table_name,'',[desc_name])
    
    return client.scannerGetList(scanner,no_row)
    
    
     
    
def printRowsResult(rows):
    
    for row in rows:
        print "row-id:%s" %(row.row)
        for k,v in sorted(row.columns.items()):
            print "%s:%s"%(k,v.value)
            

        
def getMasterTables():
    for table in client.getTableNames():
        if 'master' in table:
            print table

    
def getTableNames():
    for table in client.getTableNames():
            print table

def main(args):

    getConfiguration('host.properties')

    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    global client
    client = Hbase.Client(protocol)

    getTableNames()

if __name__ == "__main__":
    main(sys.argv)    
    


        


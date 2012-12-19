#!/usr/bin/env python

import sys

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 
import ConfigParser



def getConfiguration(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    global hbaseHost
    
    hbaseHost = config.get('hosts','hbase')
    
    
def getMasterTables():
    ret=[]
    for table in client.getTableNames():
        if 'master' in table:
            ret.append(table);

    return ret


 

def columnProcess(table_name):
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    #print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])
    
    try:
        while True:
            result=client.scannerGet(scanner)
            
            row=result[0].columns
            row_key=result[0].row
            
            email=""
            emailDomain=""
            
            for col,val in row.iteritems():
                if (col=="master_info_cf:email"):
                    email=val.value
                elif (col == "master_info_cf:emailDomain"):
                    emailDomain=val.value
            
            
            if len(emailDomain)==0:
                if len(email)==0:
                    print "There are risky row exist"
                else:
                    two=email.split('@')
                    if len(two)==2:
                        print row_key
                        try:
                            column="%semailDomain"%(desc_name)
                            client.mutateRow(table_name,row_key,[Hbase.Mutation(column=column,value=two[1])])
                        except:
                            print "Error Mutation: %s" %(row_key)
                            
        client.scannerClose(scanner)
    except:
        pass
    

def main(args):

    getConfiguration('host.properties')

    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    global client
    client = Hbase.Client(protocol)

    
    tableList=getMasterTables()

    # For test
    #table = 'lyris_uptiilt6_master_lyris'
    #columnProcess(table)
    
    for table in tableList:
        columnProcess(table)
        



if __name__ == "__main__":
    main(sys.argv)   

#!/usr/bin/env python

import sys
import time
from rfc3339 import rfc3339

#sys.path.append('/home/jerry/Software/gen-py')

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 

 


def updateColumn(table_name):
    
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])

    counter=0
    try:
        while True:
            result=client.scannerGet(scanner)
            
            fields=dict()
            
            valid = False
            
            for k,v in result[0].columns.items():
                fields[k]= v.value
                if(k=="master_info_cf:optIn" and v.value != 1):
                    fields[k]=1;
                    valid = True
            
            if(valid):
                mutatelist = list()
                
                #for k,v in fields.iteritems():                    
                #    mutatelist.append(Hbase.Mutation(column=k,value=v))
                
                mutatelist.append(Hbase.Mutation(column="master_info_cf:optIn",value="1"))
                print result[0].row    
                client.mutateRow(table_name,result[0].row,mutatelist)

            counter = counter + 1
            if((counter%1000)==0):
                print "scanning....%d" %(counter)
                
    except:
        pass
    
    client.scannerClose(scanner)
    
    

    
    
def printRowsResult(rows):
    
    for row in rows:
        print "row-id:%s" %(row.row)
        for col in row.columns.iteritems():
            print "%s:%s"%(col[0],col[1].value)
            


    
def main(args):
    
    if (len(args)<3):
        print "%s hbasehost tablename " % args[0]
        sys.exit(1)


    hbaseHost = args[1]

    table_name= args[2]

    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    global client
    client = Hbase.Client(protocol)
    
    updateColumn(table_name)
    
    transport.close()
    
if __name__ == "__main__":
    main(sys.argv)    
    


        


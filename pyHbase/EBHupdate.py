#!/usr/bin/env python

import sys
import time
from rfc3339 import rfc3339

#sys.path.append('/home/jerry/Software/gen-py')

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 

 
hbaseHost = '10.3.203.146'
#hbaseHost = '10.3.9.18'
transport = TBufferedTransport(TSocket(hbaseHost, 9090))
transport.open()
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Hbase.Client(protocol)

uuids = []


def getRowsLimit(table_name,no_row):
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])

    return client.scannerGetList(scanner,no_row)


def updateUUID(table_name):
    
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])

    counter=0
    indexOfUUID=0
    try:
        while True:
            result=client.scannerGet(scanner)
            #print result[0].row
            fields=dict()
            
            valid = False
            
            for k,v in result[0].columns.items():
                fields[k]= v.value
                if(k == "email_info_family:visit_open_count"):
                    print result[0].row
                    valid = True
            
            if(valid):
                fields["email_info_family:lyrisUUID"] = uuids[indexOfUUID];
                indexOfUUID= indexOfUUID + 1
                
                
                mutatelist = list()
                
                for k,v in fields.iteritems():                    
                    mutatelist.append(Hbase.Mutation(column=k,value=v))
                
                print mutatelist        
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
            

def updateRowsForDebugging(table_name,rows):
    
    for row in rows:
        newrowid= '|'.join(['jerry@lyris.com',row.row.split('|')[1]])
        print newrowid
        mutatelist=list()    
        
        for col in row.columns.iteritems():
            if('master_info_cf:updateDate'== col[0]):
                mutatelist.append(Hbase.Mutation(column=col[0],value=rfc3339(time.time())))
#                print col[1].value
#                print rfc3339(time.time())
            else:
                mutatelist.append(Hbase.Mutation(column=col[0],value=col[1].value))

        print mutatelist
        client.mutateRow(table_name,newrowid,mutatelist)
        break
        

    
def main(args):
    
 
    rows = getRowsLimit('lyris_uptilt_master_lyris',100)
    
    for row in rows:
        keys = row.row.split('|')
        #print keys[1]
        uuids.append(keys[1])
        
    table_name='email_by_hour'
    
#    updateUUID(table_name)
    
#    client.mutateRow(table_name,'jerry@lyris.com|079678-13795157-000',
#                     [Hbase.Mutation(column='master_info_cf:webSiteType',value='Commercial')])


if __name__ == "__main__":
    main(sys.argv)    
    
transport.close()

        


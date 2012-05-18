#!/usr/bin/env python

import sys
import time
from rfc3339 import rfc3339

#sys.path.append('/home/jerry/Software/gen-py')

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase 

 
#hbaseHost = '10.3.203.146'
hbaseHost = '10.3.9.18'
transport = TBufferedTransport(TSocket(hbaseHost, 9090))
transport.open()
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Hbase.Client(protocol)

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


    client.scannerClose(scanner)
    
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
    
    client.scannerClose(scanner)
    
    return rows;   

    
def getRowsLimit(table_name,no_row):
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    print desc_name
    
    scanner = client.scannerOpen(table_name,'',[desc_name])
    
    rows = client.scannerGetList(scanner,no_row)
    
    client.scannerClose(scanner)
    
    return rows
     
    
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
        
def getMasterTables():
    for table in client.getTableNames():
        if 'master' in table:
            print table

    
def main(args):
#    getColumnInfo('visitor_by_hour')
#    getColumnInfo('email_by_hour')
 
#    getColumnInfo('lyris_uptilt_master_lyris')            
    table_name='lyris_uptiltallin1002_master_lyris'
#    table_name='lyris_fulcrumtech_master_lyris'
#    table_name='visitor_by_hour'

#    rows=getUniqRow(table_name)
#    print(len(rows.items())) 

#    ret=getRowsLimit(table_name,3)
#   printRowsResult(ret)
#    updateRowsForDebugging(table_name,ret)

    client.mutateRow(table_name,'jerry@lyris.com|079678-13795157-000',
                     [Hbase.Mutation(column='master_info_cf:webSiteType',value='Commercial')])


if __name__ == "__main__":
    main(sys.argv)    
    
transport.close()

        


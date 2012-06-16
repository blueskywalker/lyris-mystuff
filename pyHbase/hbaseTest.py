#!/usr/bin/env python

import sys

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


def getUniqRow(table_name,echo):
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
    

    if (echo):
		for row in rows.items():
			print row
    else:
		print len(rows); 

    return rows


def getMasterTables():
    for table in client.getTableNames():
        if 'master' in table:
            print table

    

def getRowList(tablename,limit):
	coldesc = client.getColumnDescriptors(tablename)
	desc_name,desc = coldesc.items()[0]
	print desc_name
	
	scanner = client.scannerOpen(tablename,'',[desc_name])

	return client.scannerGetList(scanner,limit)

def printRowInfo(rows):
	for row in rows:
		print row.row
		for cell in row.columns.items():
			print cell
		print ""
	
	
def main(args):
   # getColumnInfo('visitor_by_hour')
    #getColumnInfo('email_by_hour')
 
#    getUniqRow(table_name)
    getColumnInfo('lyris_uptilt_master_lyris')            
#   getColumnInfo('web_behavior_lyris_uptilt')            
#	getUniqRow('email_by_hour',False)

#	getUniqRow('visitor_by_hour',False)

#	rows = getRowList("email_by_hour",10)
#	rows = getRowList("visitor_by_hour",10)

#	rows = getRowList("lyris_uptilt_master_lyris",10)
#	printRowInfo(rows)
	
if __name__ == "__main__":
    main(sys.argv)    
    

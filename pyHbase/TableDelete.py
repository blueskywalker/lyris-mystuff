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


def getUpdateColumn(table_name,column):

	coldesc = client.getColumnDescriptors(table_name)

	desc_name,desc = coldesc.items()[0]

	print desc_name

	scanner = client.scannerOpen(table_name,'',[desc_name])

	counter=0

	try:
		while True:
			mutatelist=list()
			result=client.scannerGet(scanner)
			#print result[0]
			#print result[0].row
		
			for col,value in result[0].columns.items():
				
				if(col == "email_info_family:lyris_uuid"):
					continue
				
				mutatelist.append(Hbase.Mutation(column=col,value=value.value))
			
			client.mutateRow(table_name,result[0].row,mutatelist)
			client.d
			counter = counter + 1
			if((counter%1000)==0):
				print "scanning....%d" %(counter)
			
			

	except:
		pass

	return True;   

	

def getDeleteColumn(table_name,column):

	coldesc = client.getColumnDescriptors(table_name)

	desc_name,desc = coldesc.items()[0]

	print desc_name

	scanner = client.scannerOpen(table_name,'',[desc_name])

	counter=0

	try:
		while True:
			
			result=client.scannerGet(scanner)
			#print result[0]
			#print result[0].row
		
			client.deleteAll(table_name,result[0].row,column)
				
			counter = counter + 1
			if((counter%1000)==0):
				print "scanning....%d" %(counter)
			
			

	except:
		pass

	return True;   

	
def main(args):
	#table_name='web_behavior_lyris_uptilt'
	table_name='email_by_hour'

	getDeleteColumn(table_name,'email_info_family:lyris_uuid')


if __name__ == "__main__":
	main(sys.argv)    
	transport.close()	


		


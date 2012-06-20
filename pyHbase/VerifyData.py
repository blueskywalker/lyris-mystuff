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
    

def verifyData(table_name):
    coldesc = client.getColumnDescriptors(table_name)

    desc_name,desc = coldesc.items()[0]

    #print desc_name

    scanner = client.scannerOpen(table_name,'',[desc_name])

    outputfile = "%s_verify.txt"%(table_name)

    try:
        os.remove(outputfile)
    except:
        pass
    
    OUTPUT = open(outputfile,"w")
    
    counter=0    
    try:
        while True:
            result=client.scannerGet(scanner)
            #print result[0].row
            uuid = result[0].columns['master_info_cf:lyrisUUID'].value
            if( not getRowFromSolr(uuid)):
                print >> OUTPUT, result[0].row
            
            counter = counter + 1
            if((counter%1000)==0):
                print "scanning....%d" %(counter)
            
    except:
        pass
    
    print "total count is %d" %(counter)
    OUTPUT.close()
    


def connectSolrServer(orgId,subOrgId):
    global solrServer
    coreNo = commands.getoutput("./getCore.sh %s %s"%(orgId,subOrgId))
    hostUrl = "http://%s:8983/solr/%s"%(solrHost,coreNo)
    solrServer = solr.SolrConnection(hostUrl)

def getRowFromSolr(uuid):
    #print uuid
    res=solrServer.query("id:%s"%(uuid))
    
    if(len(res.results)>0):
#        print res.results[0]
        return True
    else:
        return False

def getCoreNo(orgId,subOrgId):
    result = commands.getoutput("./getCore.sh %s %s"%(orgId,subOrgId))
    return result
    
    
def main(args):
    
    if(len(args)!=3):
        print "%s orgId subOrgId"%(args[0])
        sys.exit(1)
    
    orgId = args[1]
    subOrgId = args[2]
    
    getConfiguration('host.properties')

    
    transport = TBufferedTransport(TSocket(hbaseHost, 9090))
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    global client
    client = Hbase.Client(protocol)
        
    
    tablename = "%s_%s_master_%s"%(orgId,subOrgId,orgId);
        
    connectSolrServer(orgId,subOrgId)
    verifyData(tablename)

    transport.close()

if __name__ == "__main__":
    main(sys.argv)    
    


        


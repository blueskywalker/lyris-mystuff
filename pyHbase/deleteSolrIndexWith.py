#!/usr/bin/env python

import sys
import solr
import commands
import ConfigParser

def getConfiguration(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    
    global solrHosts
    hosts = config.get('hosts','solr')
    solrHosts = hosts.split(',')
    print solrHosts
    

def connectSolrServer(host,orgId,subOrgId):
    global solrServer
    coreNo = commands.getoutput("./getCore.sh %s %s"%(orgId,subOrgId))
    hostUrl = "http://%s:8983/solr/%s"%(host,coreNo)
    solrServer = solr.SolrConnection(hostUrl)
    
def main(args):
    
    if(len(args) < 3):
        print "%s orgid subOrgId"%(args[0])
        sys.exit(-1)
    
    getConfiguration('host.properties')
    
    for host in solrHosts:
    	connectSolrServer(host,args[1],args[2])
    	solrServer.delete_query("orgId:%s AND subOrgId:%s"%(args[1],args[2]))
    	solrServer.commit()
    	solrServer.close()
    
    
if __name__ == '__main__':
    main(sys.argv)

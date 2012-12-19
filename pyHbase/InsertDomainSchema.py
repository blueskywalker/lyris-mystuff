#!/usr/bin/env python

import sys
import ConfigParser
import MySQLdb as mdb

def getConfiguration(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    global mySqlHost
    
    mySqlHost = config.get('hosts','mysql')


def insertSchema(database):
    try:
        cur = con.cursor()
        queryString = "INSERT INTO %s.list_schema" % database
        queryString += "(uuid,contactFormatType,externalTblNameSuffix,field,name,type,category,mergeTag,multiSelect,autoComplete,bucketed) "
        queryString += "VALUES ('CTFR-081640-01187882-444','Region','_master_lyris_stg','emailDomain','EmailDomain','string','DEMOGRAPHIC',b'0',b'0',b'0',b'0')"
        print queryString
        cur.execute(queryString)
        
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        
def connectDB(mysql):
    
    global con
    con = None
    
    try:
    
        con = mdb.connect(mysql, 'root','g0lyr1s')
        
        cur = con.cursor()
        cur.execute("show databases")
        
        response = cur.fetchall()
        
        # for Test
        insertSchema('lyris_uptiltnew')
        
#        for database in response:
#            insertSchema(database[0])
    
        cur.execute("commit")
        
    except mdb.Error, e:
    
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    finally:    
        
        if con:
            
            con.close()



def main(args):
    getConfiguration('host.properties')
    connectDB(mySqlHost)
    
    
if __name__ == "__main__":
    main(sys.argv)  

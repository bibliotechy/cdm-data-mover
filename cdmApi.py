#!/usr/bin/python2.7

import httplib
import json



def cdmToJson():
    #gets 150,000 basic records from contentDM
    req = '/dmwebservices/?q=dmQuery/all/subjec^^all^and/all/title/150000/1/0/0/0/0/json'
    
    conn = httplib.HTTPConnection('lenny.gsu.edu',port=80,timeout=20)
    conn.request('GET', req)
    response  = conn.getresponse()
    
    #add error catching here
    
    #full list of records in cdm6
    data = json.loads(response.read())

def jsonToObjectHierarchy(data):
    #build a dictionary of cdm records, either single file records, or compound objects with 
    #child records as an entry  
    dataDict = {}
     
    for record in data['records']:
        uniqueID = record['collection'].strip('/') + u'/' + unicode(record['pointer'])
        if record['parentobject'] == -1:
            dataDict[uniqueID] = record
            if record['filetype'] == 'cpd':
                dataDict[uniqueID][u'children'] = {}
        else:
            try:
                parentuniqueID = record['collection'].strip('/') + u'/' + unicode(record['parentobject'])
                dataDict[parentuniqueID]['children'][record['pointer']] = record
            except KeyError:
                print "Key error"
                pass
            
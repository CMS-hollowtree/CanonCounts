#!/usr/bin/env python

import datetime
from pysnmp.entity.rfc3413.oneliner import cmdgen
from mailer import Mailer
from prettytable import PrettyTable

cmdGen = cmdgen.CommandGenerator()

pageCountMIBColor = 'iso.3.6.1.2.1.43.10.2.1.4.1.1'
pageCountMIBBlack = 'iso.3.6.1.4.1.1602.1.11.1.3.1.4.108'
today = datetime.date.today()

def snmp(community, host, mib):
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    	cmdgen.CommunityData(community, mpModel=0),
		cmdgen.UdpTransportTarget((host, 161)),
		cmdgen.MibVariable(mib)
    )
	
    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % 
                (errorStatus.prettyPrint(), 
                errorIndex and 
                varBinds[(errorIndex)-1] or '?'))
        else:
            for name, val in varBinds:
                return((val))

CRCountC = snmp('public', 'CanonReception', pageCountMIBColor)
CFOCountC = snmp('public', 'CanonFrontOffice', pageCountMIBColor)
CEJCountC = snmp('public', 'CanonEJ', pageCountMIBColor)
CSHPCountC = snmp('public', '192.168.4.163', pageCountMIBColor)

CRCountB = snmp('public', 'CanonReception', pageCountMIBBlack)
CFOCountB = snmp('public', 'CanonFrontOffice', pageCountMIBBlack)
CEJCountB = snmp('public', 'CanonEJ', pageCountMIBBlack)
CSHPCountB = snmp('public', '192.168.4.163', pageCountMIBBlack)
# SUBJECT, TODAY, PRINTER - COUNT, PRINTER - COUNT, PRINTER - COUNT
# message = 'Subject: %s\n\n Lake Business,\n\nBelow are the pagecounts, as of today (%s).\n\n%s : %d\n%s : %d\n%s : %d\n%s : %d\n\n Thank you,\n\nConor Sullivan\nHose Master\n1233 East 222nd St.\nCleveland, OH 44117\n216-481-2020' % ('HoseMaster: Printer Page Counts', today, 'CanonReception (A4568)', CRCount, 'CanonFrontOffice (A2021)', CFOCount, 'CanonEJ (A3803)', CEJCount, 'CanonShipping (ASHP)', CSHPCount)
counts = [
	{
		'name': 'CanonReception',
		'id': 'A4568',
		'pageCounts': {
			'ColorPageCount': CRCountC,
			'BlackWhitePageCount': CRCountB
		}
	},
	{
		'name': 'CanonFrontOffice',
		'id': 'A2021',
		'pageCounts': {
			'ColorPageCount': CFOCountC,
			'BlackWhitePageCount': CFOCountB
		}
	},
	{
		'name': 'CanonEJ',
		'id': 'A3803',
		'pageCounts': {
			'ColorPageCount': CEJCountC,
			'BlackWhitePageCount': CEJCountB
		}
	},
	{
		'name': 'CanonShipping',
		'id': 'ASHP',
		'pageCounts': {
			'ColorPageCount': CSHPCountC,
			'BlackWhitePageCount': 'NONE'
		}
	}
]
#Mailer(message)
t = PrettyTable(['ID', 'Name', 'Color Pages', 'Black Pages'])

for printer in counts:
	t.add_row([printer['id'], printer['name'], printer['pageCounts']['ColorPageCount'], printer['pageCounts']['BlackWhitePageCount']])
print(t.get_string())
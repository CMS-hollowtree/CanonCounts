#!/usr/bin/env python
from flask import render_template, request, Flask, flash, redirect
from pysnmp.entity.rfc3413.oneliner import cmdgen
from app import app
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests, time, json, os
import datetime

cmdGen = cmdgen.CommandGenerator()

pageCountMIBColor = 'iso.3.6.1.2.1.43.10.2.1.4.1.1'
pageCountMIBBlack = 'iso.3.6.1.4.1.1602.1.11.1.3.1.4.108'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

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
def getCounts():   
    CRCountC = snmp('public', 'CanonReception.homant.ds', pageCountMIBColor)
    CFOCountC = snmp('public', 'CanonFrontOffice.homant.ds', pageCountMIBColor)
    CEJCountC = snmp('public', 'CanonEJ.homant.ds', pageCountMIBColor)
    CSHPCountC = snmp('public', '192.168.4.163', pageCountMIBColor)

    CRCountB = snmp('public', 'CanonReception.homant.ds', pageCountMIBBlack)
    CFOCountB = snmp('public', 'CanonFrontOffice.homant.ds', pageCountMIBBlack)
    CEJCountB = snmp('public', 'CanonEJ.homant.ds', pageCountMIBBlack)
    CSHPCountB = snmp('public', '192.168.4.163', pageCountMIBBlack)

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
                'BlackWhitePageCount': 'None'
            }
        }
    ]
    return counts

@app.route('/', methods=['GET','POST'])
@app.route('/index')

def index():
    if request.method == 'GET':
        form = ReusableForm(request.form)
        print(form.errors)
        counts = getCounts()

    return render_template('index.html',
            form=form,
            title='Hose Master',
            subtitle='Canon page counts',
            counts = counts
            )
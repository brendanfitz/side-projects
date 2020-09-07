# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 19:52:11 2020

@author: Brendan Non-Admin
"""

import requests
import pandas as pd
import feedparser
from lxml import etree
import io

##############################################################################
# RSS
##############################################################################

url = 'https://www.sec.gov/cgi-bin/browse-edgar'
cik = '0000094845' # levi strauss
params = {
    'action': 'getcompany', 
    'CIK': cik,
    'type': '10-K',
    'start': 0,
    'count': 40,
    'output': 'atom',
}
response = requests.get(url, params)
rawdata = response.content

d = feedparser.parse(rawdata)


entry = d.entries[-5]
sorted(entry.keys())
entry

accension_number = entry['accession-number'].replace('-', '')
filing_url_base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accension_number}"

##############################################################################
# Filing Summary
##############################################################################
filing_summary_url = filing_url_base + 'FilingSummary.xml'
response = requests.get('https://www.sec.gov/Archives/edgar/data/94845/000119312505031592/d10k.htm')

response.content
with io.BytesIO(response.content) as f:
    tree = etree.parse(f)
    
root = tree.getroot()
root

##############################################################################
# tables
##############################################################################
response = requests.get(url + '/R2.htm')
pd.read_html(response.content)[0]
    
##############################################################################
# Use FilingSummary.xml summary to pull document numbers e.g. R1.htm, R2.htm
##############################################################################
url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accension_number}/FilingSummary.xml"


##############################################################################
# Pull tables from R1.htm, R2.htm, etc
##############################################################################


##############################################################################
# 10-K
##############################################################################

url = 'https://www.sec.gov/Archives/edgar/data/1318605/000156459020004475/tsla-10k_20191231_htm.xml'
response = requests.get(url)

with io.BytesIO(response.content) as f:
    tree = etree.parse(f)
    
root = tree.getroot()

namespaces = root.nsmap

def get_value(node, namespace, element):
    if node.find(f'{{{namespace}}}{element}') is not None:
        return node.find(f'{{{namespace}}}{element}').text
    return None

def get_child_node(node, namespace, element, _id=None):
    return node.find(f'{{{namespace}}}{element}')

def get_context_node(node, context_ref):
    xpath = ".//*[@id='{}']".format(context_ref)
    return root.xpath(xpath)[0]

context_ref = "C_0001318605_us-C_0001318605_us-gaapStatementBusinessSegmentsAxis_tslaAutomotiveSegmentMember_20190101_20191231"
context = get_context_node(root, context_ref)

def get_custom_dimension(context):
    if context[0] is not None:
        segment = get_child_node(context[0], namespaces[None], "segment")
        if segment is not None:
            explicitMember = segment[0]
            if explicitMember is not None:
                return explicitMember.get('dimension'), explicitMember.text
    return None

get_custom_dimension(context)

def get_data(element):
    data = list()
    
    gaap_namespace = namespaces['us-gaap']
    
    for node in root.findall(f'{{{gaap_namespace}}}{element}'):
        context_ref = node.get('contextRef')
        context = get_context_node(root, context_ref)
        
        dimensions = get_custom_dimension(context)
        if dimensions is not None:
            dimension = dimensions[0]
            dimension_type = dimensions[1]
        else:
            dimension = None
            dimension_type = None
        
        period = get_child_node(context, namespaces[None], 'period')
        data.append({
            'context_ref': context_ref,
            'element': element,
            'value': node.text,
            'instant': get_value(period, namespaces[None], "instant"),
            'startDate': get_value(period, namespaces[None], "startDate"),
            'endDate': get_value(period, namespaces[None], "endDate"),
            'dimension': dimension,
            'dimension_type': dimension_type,
        })
    return pd.DataFrame(data)   

get_data('Revenues')




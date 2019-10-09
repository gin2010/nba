# -*- coding: utf-8 -*-
# File  : xml_demo.py
# Author: water
# Date  : 2019/8/23

BASIC = """
<note>
<to>George</to>
<from>John</from>
<heading>Reminder</heading>
{}
<body>Don't forget the meeting!</body>
</note>
"""
nodes = ['test','fphm','fpdm']
values = ['abc','134534','20190101']

#<test>abc</test>
def generateXml(nodes,values):
    xml = ""
    for node,value in zip(nodes,values):

        xml+=("<{0}>{1}</{0}>\n").format(node,value)
    return BASIC.format(xml)

if __name__ == "__main__":
    case = generateXml(nodes,values)
    print(case)

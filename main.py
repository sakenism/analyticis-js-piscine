import os
from datetime import datetime

import plotly.express as px
import numpy as np
import plotly.graph_objects as go


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from docxtpl import DocxTemplate
from hasura import Hasura

z01 = Hasura(os.getenv("HASURA_ADDR"), os.getenv("HASURA_SCRT"))

js = "3402"

children_of_js_Query = """
{
  object_child(where: {parentId: {_in: [%s]}}, order_by: {index: asc}) {
    child {
      id
      name
    }
  }
}
"""

count_status = """
{
  obj1: progress_aggregate(where: {objectId: {_eq: %s},
  		bestResult: {grade: {_gte: 1}}}) {
    aggregate {
      count
    }
  }
  
  obj0: progress_aggregate(where: {objectId: {_eq: %s},
  		bestResult: {grade: {_lt: 1}}}) {
    aggregate {
      count
    }
  }
}
"""


children_of_js = z01.query(children_of_js_Query % js)
children_of_js = children_of_js['data']['object_child']

tmp = []

for child in children_of_js:
	tmp.append(child['child'])


children_of_js = tmp

children_of_child = {}

str_children_of_js = ""

for child in children_of_js:
	str_children_of_js = str_children_of_js + str(child['id']) + ','


if len(str_children_of_js) > 0:
	str_children_of_js = str_children_of_js[:-1]

grandchildren_of_js = z01.query(children_of_js_Query % str_children_of_js)
grandchildren_of_js = grandchildren_of_js['data']['object_child']

tmp = []

for grandchild in grandchildren_of_js:
	tmp.append(grandchild['child'])

grandchildren_of_js = tmp

str_grandchildren_of_js = ""

for grandchild in grandchildren_of_js:
	str_grandchildren_of_js = str_grandchildren_of_js + str(grandchild['id']) + ','

if len(str_grandchildren_of_js) > 0:
	str_grandchildren_of_js = str_grandchildren_of_js[:-1]

map_ans = {}

for grandchild in grandchildren_of_js:
	map_ans[grandchild['id']] = []
	res = z01.query(count_status % (grandchild['id'], grandchild['id']))
	positive = res['data']['obj1']['aggregate']['count']
	negative = res['data']['obj0']['aggregate']['count']
	# print(positive, negative)

	map_ans[grandchild['id']].append({
		"name": grandchild['name'],
		"success": positive,
		"fail": negative
	})

for child in children_of_js:
	map_ans[child['id']] = []
	res = z01.query(children_of_js_Query % str(child['id']))
	res = res['data']['object_child']
	children_of_child[child['id']] = res
		
	positive = 0
	negative = 0

	for tmp in res:
		positive = positive + map_ans[tmp['child']['id']][0]['success']
		negative = negative + map_ans[tmp['child']['id']][0]['fail']
	map_ans[child['id']].append({
		"name": child['name'],
		"success": positive,
		"fail": negative	
	})	

bin_children_id = []
bin_children_name = []
bin_children_success = []
bin_children_fail = []

bin_grandchildren_id = []
bin_grandchildren_name = []
bin_grandchildren_success = []
bin_grandchildren_fail = []

for child in children_of_js:
	bin_children_id.append(child['id'])
	bin_children_name.append(map_ans[child['id']][0]['name'])
	bin_children_success.append(map_ans[child['id']][0]['success'])
	bin_children_fail.append(map_ans[child['id']][0]['fail'])

	for grand in children_of_child[child['id']]:
		bin_grandchildren_id.append(grand['child']['id'])
		bin_grandchildren_name.append(map_ans[grand['child']['id']][0]['name'])
		bin_grandchildren_success.append(map_ans[grand['child']['id']][0]['success'])
		bin_grandchildren_fail.append(map_ans[grand['child']['id']][0]['fail'])
figchildren = go.Figure(data=go.Bar(x=bin_children_name, y=bin_children_success))
figchildren.show()

figgrandchildren = go.Figure(data=go.Bar(x=bin_grandchildren_name, y=bin_grandchildren_success))
figgrandchildren.show()

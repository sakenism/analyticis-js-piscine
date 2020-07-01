# -*- coding: utf-8 -*-
# @Author: atlekbai
# @Date:   2019-10-22 17:40:16
# @Last Modified by:   Tlekbai Ali
# @Last Modified time: 2020-02-27 13:14:46

import os
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from docxtpl import DocxTemplate
from hasura import Hasura



# 01 hasura database
z01 = Hasura(os.getenv("HASURA_ADDR"), os.getenv("HASURA_SCRT"))

# Скачиваем данные с таблицы
# result хранит массив объектов с полями каждой строки
# client = connect()
# sheet = getSheet(client)
# result = sheet.get_all_records()

# из result храним в passed только github логины тех кто прошел
# passed = [row['login'] for row in result if row['passed'] == 'yes']
# totalScore = [row['score'] for row in result if row['passed'] == 'yes']
# hours = [row['average_hours'] for row in result if row['passed'] == 'yes']

# value = ",".join([f"\\\"{pas}\\\"" for pas in passed])

# делаем запросы в базу чтобы получить данные тех кто прошел

children_of_js_Query = """
{
  object_child(where: {parentId: {_in: [3402]}}, order_by: {index: asc}) {
    child {
      id
      name
    }
  }
}

"""


grandchildren_of_js_Query = """
{
  object_child(where: {parentId: {_in: [%s]}}, order_by: {index: asc}) {
    child {
      id
      name
    }
  }
}

"""

exercise_status = """
{
  progress(where: {objectId: {_in: %s}}) {
    objectId
    results(where: {grade: {_gte: 1}}){
      grade
    }
  }
}
"""

name_Query = """
{
  object(where: {id: {_eq: %s}}) {
    name
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


children_of_js = z01.query(children_of_js_Query)
children_of_js = children_of_js['data']['object_child']

# print(children_of_js)

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

# print(str_children_of_js)

grandchildren_of_js = z01.query(grandchildren_of_js_Query % str_children_of_js)
grandchildren_of_js = grandchildren_of_js['data']['object_child']

tmp = []

for grandchild in grandchildren_of_js:
	tmp.append(grandchild['child'])

grandchildren_of_js = tmp

# print(grandchildren_of_js)

str_grandchildren_of_js = ""

for grandchild in grandchildren_of_js:
	str_grandchildren_of_js = str_grandchildren_of_js + str(grandchild['id']) + ','

if len(str_grandchildren_of_js) > 0:
	str_grandchildren_of_js = str_grandchildren_of_js[:-1]


# print(str_grandchildren_of_js)

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
	res = z01.query(grandchildren_of_js_Query % str(child['id']))
	res = res['data']['object_child']
	children_of_child[child['id']] = res
		
	# print(res, '\n\n')
	positive = 0
	negative = 0

	for tmp in res:
		# print(map_ans[tmp['child']['id']][0])
		# print(tmp['child'])
		positive = positive + map_ans[tmp['child']['id']][0]['success']
		negative = negative + map_ans[tmp['child']['id']][0]['fail']
		# print(tmp['child']['id'], '\n')
	map_ans[child['id']].append({
		"name": child['name'],
		"success": positive,
		"fail": negative	
	})	
	# print(map_ans)




# dict_items = map_ans.items()
# dict_items = sorted(dict_items)

# map_ans = dict_items

# print(map_ans)

for child in children_of_js:
	print(child['id'], map_ans[child['id']])
	for grand in children_of_child[child['id']]:
		print('\t', grand['child']['id'], map_ans[grand['child']['id']])
	print()

# print(children_of_child)

# for child in children_of_child:
# 	print(child, children_of_child[child])

# print(dict_keys)


# for child in children_of_js:
# 	map_ans[child] = []
# 	children_of_child = z01.query(grandchildren_of_js_Query % str(child))
# 	children_of_child = children_of_child['data']['object_child']
# 	tmp = []
# 	for ch in children_of_child:
# 		tmp.append(ch['childId'])
# 	children_of_child = tmp
# 	success = 0
# 	fail = 0
# 	for ch in children_of_child:
# 		map_ans[ch]['success']

# 	print(children_of_child)
	# map_ans[child].append({
	# 	"name": z01.query(name_Query % str(child)),

	# })


# print(map_ans)











# print(grandchildren_of_js_Query % str_children_of_js)
# map_of_children_of_js = {}
# arr_of_children_of_js = []
# map_ans = {}

# for child in children_of_js:
# 	id = child['childId']
# 	# print(id)
# 	map_of_children_of_js[id] = z01.query(grandchildren_of_js_Query % str(id))
# 	map_of_children_of_js[id] = map_of_children_of_js[id]['data']['object_child']

# 	print(child['childId'], map_of_children_of_js[id], '\n\n\n')

# 	nm = z01.query(name_Query % str(id))
# 	nm = nm['data']['object'][0]['name']
# 	map_ans[id] = []
# 	map_ans[id].append({
# 		"name": nm,
# 		"success": 0,
# 		"fail": 0
# 	})
# 	# print(map_of_children_of_js[id], '\n\n')
# 	str_tmp = "["
# 	for tmp in map_of_children_of_js[id]:
# 		str_tmp = str_tmp + str(tmp['childId']) + ","
# 		cid = tmp['childId']
# 		nm = z01.query(name_Query % str(cid))
# 		nm = nm['data']['object'][0]['name']
# 		map_ans[cid] = []
# 		map_ans[cid].append({
# 			"name": nm,
# 			"success": 0,
# 			"fail": 0
# 		})
# 	if len(str_tmp) > 1:
# 		str_tmp = str_tmp[:-1]
# 	str_tmp = str_tmp + "]"
# 	arr_of_children_of_js.append(str_tmp)

# for tmp in map_ans:
# 	print(tmp, map_ans[tmp])

# print(arr_of_children_of_js)



# name_Query = """
# {
#   object(where: {id: {_eq: %s}}) {
#     name
#   }
# }
# """



# for days in arr_of_children_of_js:
# 	print("\nDay is being downloaded\n")
# 	res = z01.query(exercise_status % days)
# 	res = res['data']['progress']
# 	print("\nDay is downloaded\n")
# 	for rs in res: 
# 		if len(rs['results']) >= 1:
# 			map_ans[rs['objectId']][0]['success'] = map_ans[rs['objectId']][0]['success'] + 1
# 		else:
# 			map_ans[rs['objectId']][0]['fail'] = map_ans[rs['objectId']][0]['fail'] + 1
# 	print("\nDay is analyzed\n")
	

# print("\nExercises are being merged to days\n")

# for child in children_of_js:
# 	id = child['childId']
# 	for tmp in map_of_children_of_js[id]:
# 		map_ans[id][0]['success'] = map_ans[id][0]['success'] + map_ans[tmp['childId']][0]['success']
# 		map_ans[id][0]['fail'] = map_ans[id][0]['fail'] + map_ans[tmp['childId']][0]['fail'] 

# print("\nExercises are merged to days\n")

# for tmp in map_ans:
# 	print(tmp, map_ans[tmp])
	# if (map_ans[0]['success'] >= 150):
	# 	print('\n')

# arr_positive = []
# arr_negative = []

# for tmp in res:
# 	print(tmp)

# print(res)



	# for exercise in map_of_children_of_js[days]:
	# 	cnt_positive = 0
	# 	cnt_negative = 0
	# 	exercise = exercise['childId']
	# 	this_day = children_of_js = z01.query(exercise_status % exercise)
	# 	this_day = this_day['data']['progress']
	# 	for user in this_day:
	# 		if len(user['results']) >= 1:
	# 			cnt_positive = cnt_positive + 1
	# 			day_positive = day_positive + 1
	# 		else:
	# 			cnt_negative = cnt_negative + 1
	# 			day_negative = day_negative + 1
	# 	ex = z01.query(name_Query % exercise)
	# 	ex = ex['data']['object'][0]['name']
	# 	map_ans['results'].append({
	# 		'name': ex,
	# 		'success': cnt_positive,
	# 		'fail': cnt_negative
	# 	})
	# 	# map_ans[ex]['success'] = cnt_positive
	# 	# map_ans[ex]['fail'] = cnt_negative
	# 	# print("Exercise -", ex)
	# 	# print(cnt_positive, cnt_negative)
	# map_ans['results'].append({
	# 	'name': day,
	# 	'succes': day_positive,
	# 	'fail': day_negative 
	# })
	# # map_ans[day]['success'] = day_positive
	# # map_ans[day]['fail'] = day_negative

	# 	# print(this_day)


	# print(map_ans)

# print(map_of_children_of_js)















# grandchildren_of_js = z01.query(grandchildren_of_js_Query % str_children_of_js)

# grandchildren_of_js = grandchildren_of_js['data']['object_child']

# str_grandchildren_of_js = ""
# for child in grandchildren_of_js:
# 	str_grandchildren_of_js = str_grandchildren_of_js + str(child['childId']) + ','
# str_grandchildren_of_js = str_grandchildren_of_js[:-1]



# print(children_of_js)

# print('\n\n\n')

# print(grandchildren_of_js)


# passedUsers = result['data']['user']
# passedUsers = sorted(passedUsers, key=lambda x: x['attrs']['lastNameLat'])

# итерируемся по прошедшим
# constantNumber = "04/2020/"
# cnt = 0
# for user in passedUsers:
# 	cnt = cnt + 1
# 	# if cnt == 2 :
# 	# 	break
# 	attrs = user['attrs']
	
# 	surcyr = attrs["lastNameCyr"].strip()
# 	namecyr = attrs["firstNameCyr"].strip()
# 	surlat = attrs["lastNameLat"].strip()
# 	namelat = attrs["firstNameLat"].strip()
# 	iin = attrs["iin"]
# 	docnum = attrs["passNum"]
# 	borndate = formatDate(attrs["dateOfBirth"])
# 	issueddate = formatDate(attrs["dateOfIss"])
# 	expiredate = formatDate(attrs["dateOfExp"])
# 	email = attrs["email"]
# 	tel = attrs["tel"]
# 	num = constantNumber + str(cnt)
# 	context = {
# 		"fioCyr": f"{surcyr} {namecyr}",
# 		"fioLat": f"{surlat} {namelat}",
# 		"borndate": borndate,
# 		"iin": f"{iin}",
# 		"docnum": f"{docnum}",
# 		"issueddate": f"{issueddate}",
# 		"expiredate": f"{expiredate}",
# 		"email": email,
# 		"num" : num,
# 	}
# 	# print(context['email'])
# 	# for i in range (len(passed)):
# 	# 	if user['githubLogin'] == passed[i]:
# 	# 		print((hours[i]))

# 	# Сгенерировать документ
# 	generateDoc(context)

	
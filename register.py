import os
# from util import send
from hasura import Hasura

usersQuery = """
{
	progress(where:{attrs:{_contains: {acceptedAtEvent157: true}}}) {
		user {
			id
		}
	}
}
"""


z01 = Hasura(os.getenv("HASURA_ADDR"), os.getenv("HASURA_SCRT"))

result = z01.query(usersQuery)
passedUsers = result['data']['progress']
login = [user["user"]["id"] for user in passedUsers]

Quer = """
mutation registeredUsersToDiv01 {
	insert_event_user(objects: ["""
for i in range (len(login)) :
	Quer = Quer + "\n" + "\t{eventId: 132, userId: " + str(login[i]) + "},"
  
Quer = Quer + """
	]) {
		affected_rows
	}
}
"""
for i in range (len(login)) :
	a = int(input())
	# print(a)
	ok = 0
	for j in range (len(login)) :
		if login[j] == a :
			ok = 1
	if ok == 1 :
		print("YES")
	else :
		print("NO")

# print(login, "\n", len(login), Quer)
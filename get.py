# import requests
# with open('idPhoto/' + name, 'wb') as handle:
#         response = requests.get("https://01.alem.school/api/storage/download?fileId=4_z0f4bb835a30c3d6e6fa20f1c_f1101a630c39277e0_d20200203_m044823_c002_v0001132_t0000&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxOCIsImlhdCI6MTU4NTQ4MTIyNiwiaXAiOiI5MC4xNDMuMTkwLjIwOCIsImV4cCI6MTU4NTU2NzYyNiwiaHR0cHM6Ly9oYXN1cmEuaW8vand0L2NsYWltcyI6eyJ4LWhhc3VyYS1hbGxvd2VkLXJvbGVzIjpbImFkbWluIiwidXNlciJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJhZG1pbiIsIngtaGFzdXJhLXVzZXItaWQiOiIxOCIsIngtaGFzdXJhLXRva2VuLWlkIjoiNWZmNWFjNTQtNzQxYS00NmIzLWJiNWItM2M0MTY1ZDg4MjhkIiwieC1oYXN1cmEtdG9hZC1pZCI6IjE5OCJ9fQ.2whfxRROP4-QNZGTsomn2SY3l-8-zLq8AYyW5HkB3BQ", stream=True)

#         if not response.ok:
#             print (response)

#         for block in response.iter_content(1024):
#             if not block:
#                 break

#             handle.write(block)

import requests

file1 = open('name.txt', 'r') 
Names = file1.readlines() 
file1.close() 

file2 = open('doc.txt', 'r') 
Id = file2.readlines() 
file2.close()   

  
count = 0
# for i in range (len(Names)): 
#     # print(Names[i].strip())
#     print(Id[i])
        
# for i in range (len(Names)):
# 	if i == 2:
# 		break 
name = Names[0]
print(type('Names[0]'))
with open("idPhoto/" + name, 'wb') as handle:
        response = requests.get("https://01.alem.school/api/storage/download?fileId=" + Id[0] + "&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxOCIsImlhdCI6MTU4NTQ4MTIyNiwiaXAiOiI5MC4xNDMuMTkwLjIwOCIsImV4cCI6MTU4NTU2NzYyNiwiaHR0cHM6Ly9oYXN1cmEuaW8vand0L2NsYWltcyI6eyJ4LWhhc3VyYS1hbGxvd2VkLXJvbGVzIjpbImFkbWluIiwidXNlciJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJhZG1pbiIsIngtaGFzdXJhLXVzZXItaWQiOiIxOCIsIngtaGFzdXJhLXRva2VuLWlkIjoiNWZmNWFjNTQtNzQxYS00NmIzLWJiNWItM2M0MTY1ZDg4MjhkIiwieC1oYXN1cmEtdG9hZC1pZCI6IjE5OCJ9fQ.2whfxRROP4-QNZGTsomn2SY3l-8-zLq8AYyW5HkB3BQ", stream=True)

        if not response.ok:
            print (response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
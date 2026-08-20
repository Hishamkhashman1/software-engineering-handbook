from json import loads

json_data = '''
{
  "id": 42,
  "name": "Alice",
  "email": "alice@example.com",
  "active": true
}
'''

json_input = loads(json_data)

# print (json_input)

def solution(json_input):
  result = {}
  

  result["user_id"] = json_input["id"]
  result["username"] = json_input["name"]
  if json_input.get("active"):
    if json_input.get("active") == True:
      result["status"] = "Active"
    else:
      result["status"] = "Inactive"
  else:
    result["status"] = "check json"

  return result



print (solution(json_input))


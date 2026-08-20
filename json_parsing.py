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

print (json_input)

def solution(json_input):
  result = {}
  
  if json_input.get("active") == True:
    result["user_id"] = json_input["id"]
    result["username"] = json_input["name"]
    result["status"] = json_input["active"]

  return result



print (solution(json_input))


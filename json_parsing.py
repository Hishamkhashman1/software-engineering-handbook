from json import loads
from flatten_dict import flatten

json_data = '''
{
  "id": 42,
  "name": "Alice",
  "email": "alice@example.com",
  "active": true
}
'''

# json_input = loads(json_data)

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



# print (solution(json_input))

json_data_nested = '''
{
  "user": {"id": 101,"name": "Bob","location": {"city": "Tokyo","country": "Japan"}},"account": {"plan": "premium","balance": 125.50}
}
'''

json_input_nested = loads(json_data_nested)

def solution_nested(json_input_nested):
  flat_dict = flatten(json_input_nested)
  result = flat_dict.get("user")
  return result

print (solution_nested(json_input_nested))



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



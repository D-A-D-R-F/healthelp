import os

map_api_key = os.environ.get('MAP_API')
print(map_api_key)

test = 'hi we you .'
if test.find(' ') != None:
    print(test.replace(' ' , '+'))

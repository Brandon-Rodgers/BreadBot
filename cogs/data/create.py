import yaml

def read(file_name):
  with open(f'{file_name}.yaml', 'r') as file:
    return yaml.safe_load(file)

def write(file_name, item):
  with open(f'{file_name}.yaml', 'w') as file:
    return yaml.dump(item, file)

def add(file_name, item, key):
  file = read(file_name)
  file[key] = item
  write(file_name, file)


item = {'legion': {
          'leader': 'avz', 
          'members': {'test': 1234, 'test2': 5678}
          }
        }

new_item = {'leader': 'zar',
            'members': ['test', 'test3']
}

#write('guild', item)
#print(read('guild'))
add('guild', new_item, 'legion3')
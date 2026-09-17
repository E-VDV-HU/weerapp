# Source - https://stackoverflow.com/a/17341041
# Posted by Klaus Byskov Pedersen
# Retrieved 2026-09-07, License - CC BY-SA 3.0

#Just an example how the dictionary may look like
myDict = {'age': ['12'], 'address': ['34 Main Street, 212 First Avenue'],
      'firstName': ['Alan', 'Mary-Ann'], 'lastName': ['Stone', 'Lee']}

def search(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor in v:
                return k
    return None

#Checking if string 'Mary' exists in dictionary value
print(search(myDict, 'Mary')) #prints firstName

import os

print os.getcwd()

f = open('temp.txt', 'w')
f.write(os.getcwd())
import os

app = 'firefox.exe'
loc = None
posLocs = []

for root, dirs, files in os.walk(r'C:\\'):
    if app in files:
        posLocs.append(os.path.abspath(os.path.join(root, app)))
    
loc = sorted(posLocs, key=len)[0]
print(loc)
from functools import reduce
import os, json

def fileMap(rootDir = r'C:\\'):
    map = {}

    for root, dirs, files in os.walk(rootDir):
        # print(root, dirs, files)
        map[root] = {
            "folders": dirs,
            "files": files
        }

    with open('tests\\fileMap.json', 'w') as fp:
        json.dump(map, fp)

    return map

def fileMap2(rootDir = r'C:\\'):
    map = {}

    for root, dirs, files in os.walk(rootDir):
        # print(root, dirs, files)
        temp = {d: {} for d in dirs}
        temp['files'] = files
        # print(map[root])

        # print(os.path.basename(root))
        found = False
        for x in map:
            if os.path.basename(root) in map[x]:
                map[x][os.path.basename(root)] = temp
                found = True

        if not found:
            map[root] = temp
        
        print("T", map)

    with open('tests\\fileMap.json', 'w') as fp:
        json.dump(map, fp)

    return map

def get_directory_structure(rootdir = r'C:\\'):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    found at https://stackoverflow.com/questions/21455021/python-map-a-filesystem-to-a-directory-structure-works-but-how
    """
    dir_ = {}
    # rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        path_as_list = path[start:].split(os.sep)
        files_in_dir = dict.fromkeys(files)
        fullDir = reduce(dict.get, path_as_list[:-1], dir_)
        fullDir[path_as_list[-1]] = files_in_dir
        print(fullDir)

    with open('tests\\fileMap.json', 'w') as fp:
        json.dump(dir_, fp)

    return dir_

if __name__ == '__main__':
    # fileMap()

    # fileMap2()

    get_directory_structure()
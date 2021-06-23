import os

root_path = os.getcwd()
ignore_list = ['.git', 'images','html','.idea', '企业权限管理系统', 'pictures']
dir_set = set()

def in_ignore_list(dir_name):
    for ignore_dir in ignore_list:
        if ignore_dir in dir_name:
            return True
    return False


def list():
    files = os.walk(root_path)
    for path, dir_list, file_list in files:
        if in_ignore_list(path):
            continue
        for dir_name in dir_list:
            if in_ignore_list(dir_name):
                continue
            print(os.path.join(path, dir_name))

if __name__ == "__main__":
    list()

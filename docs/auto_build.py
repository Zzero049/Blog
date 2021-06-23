import os
import codecs

root_path = os.getcwd()
ignore_list = ['.git', 'images', 'html', '.idea', '企业权限管理系统', 'pictures', '黑马旅游网']
top_file_list = {'backend': '后端', 'front': '前端', 'practice': '算法记录', 'AI': '人工智能',
                 'others': '其他', 'service': '业务'}
dir_set = set()
project_root_name = 'blog'


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
            dir_set.add(os.path.join(path, dir_name))


"""
:return 0 不需要 _sidebar.md
:return 1 已经有 _sidebar.md
:return 2 需要 _sidebar.md
"""


def need_build_sidebar(file_list):
    if "hide.md" in file_list:
        return 0

    if "_sidebar.md" in file_list:
        return 1

    for file in file_list:
        if file.endswith(".md"):
            return 2

    return 0


def update_sidebar():
    for dir in dir_set:
        files = os.walk(dir)
        for path, dir_list, file_list in files:
            if in_ignore_list(path):
                continue
            if need_build_sidebar(file_list) == 1 or need_build_sidebar(file_list) == 2:
                with open(os.path.join(path, "_sidebar.md"), "w+", encoding='utf-8') as f:
                    f.truncate()
                    write_sidebar(path, file_list, f)


def write_sidebar(path, file_list, f):
    write_return_sidebar(path, f)
    idx = path.index(project_root_name)
    file_path = path[idx + len(project_root_name) + 1:]
    file_path_block = file_path.split("\\")

    f.write("- " + file_path_block[-1] + "\n")
    for file in file_list:
        # 子目录形式的笔记
        if count_md(file_list) == 1:
            child_files = os.listdir(path)
            for child_dir in child_files:
                child_path = os.path.join(path, child_dir)
                if os.path.isdir(child_path):
                    newDir = os.listdir(child_path)
                    if "_sidebar.md" in newDir:
                        child_dir_path = child_path[idx + len(project_root_name) + 1:]
                        child_file_path_block = child_path.split("\\")
                        res = os.path.join(child_dir_path,"_sidebar.md")
                        res = res.replace('\\', '/')
                        f.write("\t - [" + child_file_path_block[-1] + "]" + "(" + res + ")\n")
        elif file.endswith(".md") and file != "_sidebar.md":
            res = os.path.join(file_path, file)
            res = res.replace('\\', '/')
            f.write("\t - [" + file + "]" + "(" + res + ")\n")


def update_top_sidebar():
    with open(os.path.join("./_sidebar.md"), "w+", encoding='utf-8') as f:
        files = os.listdir(root_path)
        idx = root_path.index(project_root_name)
        for child_dir in files:
            child_path = os.path.join(root_path, child_dir)
            if os.path.isdir(child_path) and child_dir in top_file_list:
                f.write("- " + top_file_list[child_dir] + "\n")
                c_files = os.listdir(child_path)
                for newDir in c_files:

                    c_path = os.path.join(child_path, newDir)
                    if os.path.isdir(c_path):
                        child_dir_path = c_path[idx + len(project_root_name) + 1:]
                        child_file_path_block = c_path.split("\\")
                        res = os.path.join(child_dir_path,"_sidebar.md")
                        res = res.replace('\\', '/')
                        f.write("\t - [" + child_file_path_block[-1] + "]" + "(" + res + ")\n")


def count_md(file_list):
    sum = 0
    for file in file_list:
        if file.endswith(".md"):
            sum += 1
    return sum


def write_return_sidebar(path, f):
    f.write("---\n" +
            "- [返回上一级](_sidebar.md) \n" +
            "---\n")


if __name__ == "__main__":
    list()
    update_sidebar()
    update_top_sidebar()

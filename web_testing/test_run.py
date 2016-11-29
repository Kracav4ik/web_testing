import os
import shutil
import subprocess
import tempfile

import requests
import sys


def equal_files(path1, path2):
    file1 = open(path1)
    file2 = open(path2)
    return file1.read().strip() == file2.read().strip()


def run_tests(program, path):
    files = os.listdir(path)
    names = []
    for fname in files:
        if fname.endswith(".a"):
            names.append(os.path.splitext(fname)[0])
    for name in names:
        tdy = tempfile.TemporaryDirectory()
        dir_name = tdy.name
        shutil.copyfile(program, os.path.join(dir_name, "run.py"))
        shutil.copyfile(os.path.join(path, name), os.path.join(dir_name, "mark.in"))
        subprocess.run([sys.executable, "run.py"], cwd=dir_name, timeout=2)
        if not equal_files(os.path.join(dir_name, "mark.out"), os.path.join(path, "%s.a" % name)):
            return "Failed on test %s" % name
    return "Passed"


if __name__ == '__main__':
    tests_path = r'c:\git_guest\web_testing\olympiads\beasts'
    submit_id, program_path, task_name = sys.argv[1:]
    # noinspection PyBroadException
    try:
        result = run_tests(program_path, os.path.join(tests_path, task_name))
    except:
        result = "Exception"

    url = 'http://localhost:6543/answer'
    requests.get(url, params={
        "result": result,
        "submit_id": submit_id,
    })

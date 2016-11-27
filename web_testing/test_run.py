import os
import shutil
import subprocess
import tempfile

import requests
import sys

import time


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
            return "Failed on test %s (dir %s)" % (name, dir_name)
    return "Passed"


if __name__ == '__main__':
    tests_path = r'c:\git_guest\web_testing\olympiads\beasts\f'
    run_id, program_path = sys.argv[1:]
    result = run_tests(program_path, tests_path)

    url = 'http://localhost:6543/answer'
    requests.get(url, params={
        "result": result,
        "run_id": run_id,
    })
    time.sleep(2000)

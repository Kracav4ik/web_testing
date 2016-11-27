import os
import shutil
import subprocess
import tempfile

import sys


def equal_files(path1, path2):
    file1 = open(path1, "br")
    file2 = open(path2, "br")
    return file1.read() == file2.read()


def f(text_program, path):
    files = os.listdir(path)
    names = []
    for fname in files:
        if fname.endswith(".in"):
            names.append(os.path.splitext(fname)[0])
    for name in names:
        tdy = tempfile.TemporaryDirectory()
        with open(os.path.join(tdy.name, "run.py"), "w") as file:
            file.write(text_program)
        shutil.copyfile(os.path.join(path, "%s.in" % name), os.path.join(tdy.name, "input.txt"))
        subprocess.run([sys.executable, "run.py"], cwd=tdy.name, timeout=2)
        print("True" if equal_files(os.path.join(tdy.name, "output.txt"),
                                    os.path.join(path, "%s.out" % name)) else "False")


if __name__ == "__main__":
    f("""
file_inp = open("./input.txt")
file_out = open("./output.txt", "w")
s = file_inp.read()
file_out.write(s[::-1])
    """, "./demo_tests")

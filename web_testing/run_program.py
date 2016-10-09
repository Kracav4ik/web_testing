import os
import shutil
import subprocess
import tempfile


def equal_files(path1, path2):
    file1 = open(path1, "br")
    file2 = open(path2, "br")
    return file1.read() == file2.read()


def f(text_program, path):
    tdy = tempfile.TemporaryDirectory()
    file = open(tdy.name + "/run.py", "w")
    file.write(text_program)
    file.close()
    shutil.copyfile(os.path.join(path, "1.in"), os.path.join(tdy.name, "input.txt"))
    subprocess.run(["python.exe", "run.py"], cwd=tdy.name, timeout=2)
    print("True" if equal_files(os.path.join(tdy.name, "output.txt"), os.path.join(path, "1.out")) else "False")

if __name__ == "__main__":
    f("""
file_inp = open("./input.txt")
file_out = open("./output.txt", "w")
s = file_inp.read()
file_out.write(s[::-1])
    """, "./demo_tests")

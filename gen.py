import pathlib
import sys


problemPath = str(pathlib.Path().resolve()) + f'/{sys.argv[1]}'
from os import system, chdir

chdir(problemPath)
print("Generating problem", pathlib.Path().resolve())

lines = [line.strip() for line in open(f"genTemplate.txt")]
curIdx = int(lines[0].split('=')[1])


totalInputs = len(lines)-1+curIdx - 1
for i in range(1, len(lines)):
	cmd = f"python gen.py {curIdx} {lines[i]}"
	system(cmd)
	print(f"Generated input {curIdx} / {totalInputs}")
	curIdx+=1
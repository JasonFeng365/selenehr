import pathlib
import os
import json

def listFiles(directory, extension=""):
	def cond(f):
		if not os.path.isfile(os.path.join(directory, f)): return False
		if extension and not (len(f)>=len(extension) and f[-len(extension):]==extension): return False
		return True

	files = [f for f in os.listdir(directory) if cond(f)]
	return files

def pidExists(path):
	problemPath = f'{str(pathlib.Path().resolve())}/{path}/hr_info'
	files = listFiles(problemPath)
	return "hr_pid.txt" in files

def readPID(path):
	if not pidExists(path): return -1
	pidFilepath = f'{str(pathlib.Path().resolve())}/{path}/hr_info/hr_pid.txt'

	with open(pidFilepath, 'r') as file:
		return int(file.readline().strip())
	return -1

def setPID(path, pid):
	pidFilepath = f'{str(pathlib.Path().resolve())}/{path}/hr_info/hr_pid.txt'

	with open(pidFilepath, 'w') as file:
		file.write(str(pid))
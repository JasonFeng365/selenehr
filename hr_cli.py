import argparse
from selene_hr import SeleneHR, bcolors
import pathlib
import sys

import json

def log(string):
	print(f"[{bcolors.OKGREEN}HR{bcolors.OKBLUE}CLI{bcolors.ENDC}] {string}")

def getJson(path):
	with open(path, 'r') as file:
		return json.load(file)
	return {}

def absPath(path):
	return f'{str(pathlib.Path().resolve())}/{path}'

from compileStatement import compile
import problemid

import dotenv
import os
dotenv.load_dotenv()
session = os.getenv("SESSION")

def gentests(path, args):
	log("Generating testcases...")
	cmd = f'gen "{path}"'
	os.system(cmd)

def ziptests(path, args):
	log("Zipping testcases...")
	cmd = f'zip_tests "{path}"'
	os.system(cmd)

def buildtests(path, args):
	gentests(path, args)
	ziptests(path, args)

def addEmptyTests(path, args):
	count = int(args[0])
	log(f"Adding {count} blank testcases...")

	for i in range(count):
		inputPath = f"{path}/testcases/input/input{i:02d}.txt"
		outputPath = f"{path}/testcases/output/output{i:02d}.txt"
		with open(inputPath, 'w') as f: pass
		with open(outputPath, 'w') as f: pass


def compileStatement(path, args):
	log("Compiling statement...")
	compile(path)

def uploadTests(path, args):
	log("Uploading testcases...")
	if not problemid.pidExists(path):
		log("Problem does not exist!")
		return
	id = problemid.readPID(path)
	abs = absPath(path)

	extrainfo = getJson(path+"/hr_info/hr_extra_info.json")
	samples = extrainfo["samples"]
	sampleDataMap = extrainfo["sampleDataMap"]
	sampleDataMap = {int(key):val for key, val in sampleDataMap.items()}


	hr = SeleneHR(session)	
	hr.uploadTestcases(id, abs+"/testcases.zip",
					samples=samples,
					sampleDataMap=sampleDataMap)
	hr.close()

# If problem exists, update. Otherwise, make new problem and set hr_pid file.
def upload(path, args):
	statement = getJson(path+"/hr_info/statement.json")
	extrainfo = getJson(path+"/hr_info/hr_extra_info.json")

	params = statement | extrainfo
	del params["samples"]
	del params["sampleDataMap"]

	abs = absPath(path)

	hr = SeleneHR(session)	
	if not problemid.pidExists(path):
		log("Creating problem...")
		id = hr.createNewProblem(**params)
		problemid.setPID(path, id)
	else:
		id = problemid.readPID(path)
		log("Updating existing problem...")
		hr.editProblemDetails(id, **params)
	
	hr.close()

def push(path, args):
	buildtests(path, args)
	compileStatement(path, args)
	upload(path, args)
	uploadTests(path, args)


FUNCTION_MAP = {'tgen' : gentests,
				'tg' : gentests,
				'tzip' : ziptests,
				'tz' : ziptests,
				'tbuild' : buildtests,
				'tb' : buildtests,
				'tempty': addEmptyTests,
				'te': addEmptyTests,
				'tupload': uploadTests,
				'tu': uploadTests,

				'mdparse' : compileStatement,
				'md' : compileStatement,
				'upload' : upload,
				'push' : push,
				}

# Not sure how to use argparse :pensive:
def main():
	parser = argparse.ArgumentParser(prog='hr', description="HackerRank CLI")
	parser.add_argument('command', choices=FUNCTION_MAP.keys())
	parser.add_argument('path')
	parser.add_argument('params', nargs='*')
	
	args = parser.parse_args()
	
	path = args.path
	log(path)
	FUNCTION_MAP[args.command](path, args.params)
	
	

if __name__ == "__main__":
	main()
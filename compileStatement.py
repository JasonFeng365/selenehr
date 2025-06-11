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

def compile(path):
	problemPath = f'{str(pathlib.Path().resolve())}/{path}'
	statement = listFiles(problemPath, extension=".md")[0]

	def findLine(lines, phrase):
		for i, line in enumerate(lines):
			if phrase in line: return i
		return -1
	
	res = {}

	with open(f'{problemPath}/{statement}', 'r') as file:
		def cond(line: str):
			if len(line.strip())==0: return False
			if line.startswith("<!--"): return False
			if line.startswith("### Objective"): return False
			if "page-break-after" in line: return False
			return True
		
		lines = [line.strip() for line in file.readlines() if cond(line)]
		jasonLine = findLine(lines, "Jason Feng")
		inputLine = findLine(lines, "### Input Specification")
		constraintsLine = findLine(lines, "### Constraints")
		outputLine = findLine(lines, "### Output Specification")
		tableLine = findLine(lines, "<table><tr>")

		def joinLines(arr: list[str]):
			res = []
			for i in range(len(arr)-1):
				if arr[i].startswith("* ") and arr[i+1].startswith("* "): res += [arr[i], '\n']
				else: res += [arr[i], '\n\n']
			res+=[arr[-1]]
			return "".join(res)

		res["statement"] = joinLines(lines[jasonLine+1:inputLine])
		res["inputFormat"] = joinLines(lines[inputLine+1:constraintsLine])
		res["constraints"] = joinLines(lines[constraintsLine+1:outputLine])
		res["outputFormat"] = joinLines(lines[outputLine+1:tableLine])
		
	with open(f'{problemPath}/hr_info/statement.json', 'w') as file:
		json.dump(res, file, indent='\t')

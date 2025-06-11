from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class difficulties:
	EASY = 0
	MEDIUM = 1
	HARD = 2
	ADVANCED = 3
	EXPERT = 4

	__lookup = ["Easy", "Medium", "Hard", "Advanced", "Expert"]
	def toName(n):
		return difficulties.__lookup[n]


class SeleneHR:
	LOADING = '⌛'
	COMPLETE = '✅'
	WARNING = '⚠️'
	ERROR = '❌'
	__LOG_HEADER = "".join([bcolors.HEADER, '[', bcolors.OKCYAN, 'Selene', bcolors.OKGREEN, 'HR', bcolors.HEADER, ']', bcolors.ENDC])

	def __init__(self, session, logging = True):
		self.session = session
		self.logging = logging

		options = webdriver.ChromeOptions()
		options.add_argument("--log-level=2")

		self.driver = webdriver.Chrome(options=options)
		self.driver.minimize_window()
	
	def close(self):
		self.driver.close()

	def __log(self, data, mode=""):
		if not self.logging: return
		if mode: print(self.__LOG_HEADER, mode, data)
		else: print(self.__LOG_HEADER, data)

	def __openWithCookie(self, url):
		self.__log("Setting cookie", mode=self.LOADING)
		self.driver.get(url)
		self.driver.add_cookie({"name": "_hrank_session", "value": self.session})

		self.__log("Opening page", mode=self.LOADING)
		self.driver.refresh()
	
	def __waitUntilElementExists(self, by, xName, delay=.1, doScroll=False):
		sleep(delay)
		while True:
			try:
				res = self.driver.find_element(by, xName)
				sleep(delay)
				if doScroll: self.__scrollTo(res)
				return res
			except:
				# print("Delaying on", xName)
				sleep(delay)

	def __waitUntilElementsExist(self, by, xName, delay=.1, minElements=1):
		while True:
			try:
				res = self.driver.find_elements(by, xName)
				if len(res)<minElements:
					sleep(delay)
					continue
				sleep(delay)
				return res
			except:
				# print("Delaying on", xName)
				sleep(delay)
	
	def __waitUntilGone(self, by, xName, delay=.1):
		while True:
			try:
				self.driver.find_element(by, xName)
				sleep(delay)
			except:
				return
	
	def __scrollTo(self, element):
		self.driver.execute_script("arguments[0].scrollIntoView();", element)
	
	def __setSampleTestcaseExplanation(self, text):
		l = self.__waitUntilElementsExist(By.CSS_SELECTOR, "div[class='CodeMirror cm-s-default CodeMirror-wrap']", minElements=3)
		self.driver.execute_script("arguments[0].CodeMirror.setValue(`"+text+"`);", l[2])

		l = self.__waitUntilElementExists(By.XPATH, "//button[text()='Update']")
		self.__scrollTo(l)
		l.click()
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Updating...']")
		self.__waitUntilGone(By.CSS_SELECTOR, "div[class='CodeMirror cm-s-default CodeMirror-wrap']")
	
	
	def uploadTestcases(self, problemId, filepath, samples=1, sampleDataMap={}):
		self.__openWithCookie(f"https://www.hackerrank.com/administration/challenges/edit/{problemId}/testcases")

		self.__waitUntilElementExists(By.CLASS_NAME, "btn.btn-text.upload-zip.msR")
		numTestcases = len(self.__waitUntilElementsExist(By.CSS_SELECTOR, "[data-id]", minElements=0))//8

		self.__log(f"{numTestcases} existing testcases found", mode=self.LOADING)
		l = self.__waitUntilElementExists(By.CLASS_NAME, "btn.btn-text.upload-zip.msR")
		l.click()

		if numTestcases>0:
			l = self.__waitUntilElementExists(By.CLASS_NAME, "btn.btn-large.continue-delete-and-upload")
			l.click()

		self.__log("Uploading zip file", mode=self.LOADING)
		l = self.__waitUntilElementExists(By.CSS_SELECTOR, "input[type='file']")
		l.send_keys(filepath)
		sleep(1)

		l = self.__waitUntilElementExists(By.XPATH, "//button[text()='Upload']")
		l.click()


		l = self.__waitUntilGone(By.XPATH, "//button[text()='Uploading...']")
		self.__log("Finished uploading testcases", mode=self.COMPLETE)

		self.driver.refresh()

		self.__log("Setting sample testcases", mode=self.LOADING)
		testcaseData = self.__waitUntilElementsExist(By.CSS_SELECTOR, "[data-id]")
		numTestcases = len(testcaseData)//8

		for i in range(samples):
			testcaseIdx = 8*i+1
			self.__scrollTo(testcaseData[testcaseIdx])
			testcaseData[testcaseIdx].click()

		self.__log("Saving changes", mode=self.LOADING)
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Save Changes']").click()
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Saving...']")
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Save Changes']")

		self.__log("Finished setting sample testcases", mode=self.COMPLETE)

		if sampleDataMap:
			for i, text in sampleDataMap.items():
				self.__log(f"Adding explanation for testcase {i}", mode=self.LOADING)
				testcaseIdx = 8*i+6
				testcaseData = self.__waitUntilElementsExist(By.CSS_SELECTOR, "[data-id]", minElements=8*numTestcases)
				self.__scrollTo(testcaseData[testcaseIdx])
				testcaseData[testcaseIdx].click()
				self.__setSampleTestcaseExplanation(text)
			self.__log(f"Finished adding sample testcase descriptions", mode=self.COMPLETE)
	
	__formatPipeline = [
		("\\", "\\\\"),
		("`", "\\`"),
	]
	def __strf(self, s: str):
		for a, b in self.__formatPipeline:
			s = s.replace(a, b)
		return s
	# Preview limit of 140 characters
	# Statement limit of 1000 characters
	def editProblemDetails(self, problemId: int, name="", difficulty=-1, preview="", statement="", inputFormat="", constraints="", outputFormat="", tags: list[str]=None):
		if len(preview)>140:
			self.__log(f"Error: preview must be 140 characters or less, currently at {len(preview)}", mode=self.ERROR)
			return
		if tags != None and len(tags)==0:
			self.__log(f"Error: tags must be nonempty", mode=self.ERROR)
			return
		if len(statement)>1000:
			self.__log(f"Warning: statement should be 1000 characters or less, currently at {len(statement)}", mode=self.WARNING)

		self.__openWithCookie(f"https://www.hackerrank.com/administration/challenges/edit/{problemId}/details")

		if difficulty != -1:
			self.__log("Setting difficulty", mode=self.LOADING)
			difficultyName = difficulties.toName(difficulty)
			self.__waitUntilElementExists(By.ID, "s2id_challenge_difficulty", doScroll=True).click()
			self.__waitUntilElementsExist(By.XPATH, f"//*[contains(text(), '{difficultyName}')]", minElements=1)[-1].click()
		
		def setTextIfFieldExists(fieldName, text):
			if text:
				self.__log(f"Setting {fieldName}", mode=self.LOADING)
				l = self.__waitUntilElementExists(By.ID, fieldName, doScroll=True)
				l.clear()
				l.send_keys(text)
		
		setTextIfFieldExists("name", self.__strf(name))
		setTextIfFieldExists("preview", self.__strf(preview))

		def setCodeMirrorIfFieldExists(fieldName, text, codemirror):
			if text:
				self.__log(f"Setting {fieldName}", mode=self.LOADING)
				self.__scrollTo(codemirror)
				self.driver.execute_script("arguments[0].CodeMirror.setValue(`"+text+"`);", codemirror)

		codemirrors = self.__waitUntilElementsExist(By.CSS_SELECTOR, "div[class='CodeMirror cm-s-default CodeMirror-wrap']", minElements=4)
		
		setCodeMirrorIfFieldExists("statement", self.__strf(statement), codemirrors[0])
		setCodeMirrorIfFieldExists("input format", self.__strf(inputFormat), codemirrors[1])
		setCodeMirrorIfFieldExists("constraints", self.__strf(constraints), codemirrors[2])
		setCodeMirrorIfFieldExists("output format", self.__strf(outputFormat), codemirrors[3])

		if tags != None:
			self.__log(f"Removing old tags", mode=self.LOADING)
			prevTags = self.__waitUntilElementsExist(By.CSS_SELECTOR, "span[class='tag']", minElements=1)
			tagInput = self.__waitUntilElementExists(By.ID, "tags_tag", doScroll=True)
			tagInput.send_keys(Keys.BACK_SPACE * len(prevTags))

			self.__log(f"Settings new tags", mode=self.LOADING)
			tagInput.send_keys("\n".join(tags) + '\n')
		
		self.__log("Saving changes", mode=self.LOADING)
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Save Changes']").click()
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Save Changes']")
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Save Changes']")

		self.__log(f"Edit your problem at {bcolors.OKCYAN}{bcolors.UNDERLINE}https://www.hackerrank.com/administration/challenges/edit/{problemId}/details{bcolors.ENDC}", mode=self.COMPLETE)
		self.__log("Finished editing problem details", mode=self.COMPLETE)

	def createNewProblem(self, name="", difficulty=1, preview="", statement="", inputFormat="", constraints="", outputFormat="", tags: list[str]=[]):
		if not name:
			self.__log(f"Error: name must be nonempty", mode=self.ERROR)
			return
		if not preview:
			self.__log(f"Error: preview must be nonempty", mode=self.ERROR)
			return
		if len(preview)>140:
			self.__log(f"Error: preview must be 140 characters or less, currently at {len(preview)}", mode=self.ERROR)
			return
		if not statement:
			self.__log(f"Error: statement must be nonempty", mode=self.ERROR)
			return
		if not inputFormat:
			self.__log(f"Error: input format must be nonempty", mode=self.ERROR)
			return
		if not constraints:
			self.__log(f"Error: constraints must be nonempty", mode=self.ERROR)
			return
		if not outputFormat:
			self.__log(f"Error: output format must be nonempty", mode=self.ERROR)
			return
		if len(tags)==0:
			self.__log(f"Error: tags must be nonempty", mode=self.ERROR)
			return
		if len(statement)>1000:
			self.__log(f"Warning: statement should be 1000 characters or less, currently at {len(statement)}", mode=self.WARNING)

		self.__openWithCookie(f"https://www.hackerrank.com/administration/challenges/create")
		
		def setTextIfFieldExists(fieldName, text):
			if text:
				self.__log(f"Setting {fieldName}", mode=self.LOADING)
				l = self.__waitUntilElementExists(By.ID, fieldName, doScroll=True)
				l.clear()
				l.send_keys(text)
		
		setTextIfFieldExists("name", self.__strf(name))
		setTextIfFieldExists("preview", self.__strf(preview))

		def setCodeMirrorIfFieldExists(fieldName, text, codemirror):
			if text:
				self.__log(f"Setting {fieldName}", mode=self.LOADING)
				self.__scrollTo(codemirror)
				self.driver.execute_script("arguments[0].CodeMirror.setValue(`"+text+"`);", codemirror)

		codemirrors = self.__waitUntilElementsExist(By.CSS_SELECTOR, "div[class='CodeMirror cm-s-default CodeMirror-wrap']", minElements=4)
		
		setCodeMirrorIfFieldExists("statement", self.__strf(statement), codemirrors[0])
		setCodeMirrorIfFieldExists("input format", self.__strf(inputFormat), codemirrors[1])
		setCodeMirrorIfFieldExists("constraints", self.__strf(constraints), codemirrors[2])
		setCodeMirrorIfFieldExists("output format", self.__strf(outputFormat), codemirrors[3])

		tagInput = self.__waitUntilElementExists(By.ID, "tags_tag", doScroll=True)

		self.__log(f"Settings new tags", mode=self.LOADING)
		tagInput.send_keys("\n".join(tags) + '\n')
		
		self.__log("Saving changes", mode=self.LOADING)
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Save Changes']").click()
		self.__waitUntilGone(By.XPATH, "//button[text()='Save Changes']")
		self.__waitUntilElementExists(By.XPATH, "//button[text()='Save Changes']")

		sleep(3)

		problemId = int(self.driver.current_url.split("/")[-2])
		self.__log(f"Problem ID: {problemId}", mode=self.COMPLETE)

		self.editProblemDetails(problemId, difficulty=difficulty)

		self.__log("Finished editing problem details", mode=self.COMPLETE)

		return problemId
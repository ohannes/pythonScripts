import os

class FileSystem:
	def __init__(self):
		self.fileName = ""
		self.changeToRootDirectory()

	def changeToRootDirectory(self):
		for i in range(len(os.getcwd().split("/")) - 1):
			os.chdir("..")

	def searchForFile(self, fileList):
		for fileName in fileList:
			if self.fileName == fileName:
				print os.getcwd() + fileName
				return
			if self.fileName in fileName:
				print os.getcwd() + fileName
			if os.path.isdir(fileName):
				fileList = os.listdir(fileName)
				os.chdir(fileName)
				self.searchForFile(fileList)
				os.chdir('..')

	def search(self, fileName):
		self.fileName = fileName
		self.searchForFile(os.listdir(os.getcwd()))

fileSystem = FileSystem()
fileName = raw_input("what are you looking for? ")
fileSystem.search(fileName)

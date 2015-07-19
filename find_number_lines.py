import os,sys

### Configuration ###
REGULATED_LENGTH_FOR_FILE_NAME = 25
REGULATE_CHARACTER_FOR_FILE_NAME = " "
REGULATED_LENGTH_FOR_NUMBER_OF_LINES = 7
REGULATE_CHARACTER_FOR_NUMBER_OF_LINES = REGULATE_CHARACTER_FOR_FILE_NAME
FILE_INFO_SEPERATOR = "\t"
FILE_EXTENSION_SPLITTER = "."
REGULATED_LENGTH_FOR_FOLDER_NAME = REGULATED_LENGTH_FOR_FILE_NAME
REGULATE_CHARACTER_FOR_FOLDER_NAME = REGULATE_CHARACTER_FOR_FILE_NAME
PATH_SEPERATOR = "/"
FOLDER_INFO_SEPERATOR = FILE_INFO_SEPERATOR
LINE_SINGULAR = "line"
LINE_PLURAL_SUFFIX = "s"
FILE_DOES_NOT_EXIST = "File does not exist"
FOLDER_DOES_NOT_EXIST = "Folder does not exist"
INFO_DIMENSION_SEPERATOR = " "
DEFAULT_NUMBER_OF_LINES = 0
LIMIT_FOR_PLURAL = 1
ALLOWED_EXTENSIONS = ["py"]
### Configuration END ###

class SourceObject:
    def __init__(self):
        pass
    def regulateStringUpToLengthWithCharacter(self, string, length, character):
        if len(string) > length:
            return string
        while len(string) < length:
            string += character
        return string
    def regulateStringForPlural(self, string, counter, plural_suffix):
        if counter > LIMIT_FOR_PLURAL:
            string += plural_suffix
        return string
    def setNumberOfLines(self):
        pass
    def getInfo(self):
        pass
    def setInfo(self):
        pass

class SourceFile(SourceObject):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_extension = ""
        self.regulated_file_name = self.regulateStringUpToLengthWithCharacter(self.file_name, REGULATED_LENGTH_FOR_FILE_NAME, REGULATE_CHARACTER_FOR_FILE_NAME)
        self.number_of_lines = DEFAULT_NUMBER_OF_LINES
        self.setFileExtension()
        self.setNumberOfLines()
        self.number_of_lines_string = self.regulateStringUpToLengthWithCharacter(str(self.number_of_lines), REGULATED_LENGTH_FOR_NUMBER_OF_LINES, REGULATE_CHARACTER_FOR_NUMBER_OF_LINES)

    def setFileExtension(self):
        file_name_split = self.file_name.split(FILE_EXTENSION_SPLITTER)
        if len(file_name_split) == 1:
            self.file_extension = ""
        else:
            self.file_extension = file_name_split[-1]

    def setNumberOfLines(self):
        if not self.file_extension in ALLOWED_EXTENSIONS:
            self.number_of_lines = 0
            return

        if os.path.exists(self.file_name):
            ftr = open(self.file_name)
            lines = ftr.readlines()
            ftr.close()
            self.number_of_lines = len(lines)
        else:
            print FILE_DOES_NOT_EXIST, self.file_name

    def getInfo(self):
        info_string = self.regulated_file_name + FILE_INFO_SEPERATOR + self.number_of_lines_string + INFO_DIMENSION_SEPERATOR + LINE_SINGULAR
        info_string = self.regulateStringForPlural(info_string, self.number_of_lines, LINE_PLURAL_SUFFIX)
        return info_string

    def printInfo(self):
        if self.file_extension in ALLOWED_EXTENSIONS:
            print self.getInfo()

class SourceFolder(SourceObject):
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.regulated_folder_name = self.regulateStringUpToLengthWithCharacter(self.folder_name, REGULATED_LENGTH_FOR_FOLDER_NAME, REGULATE_CHARACTER_FOR_FOLDER_NAME)
        self.file_list = []
        self.number_of_lines = DEFAULT_NUMBER_OF_LINES
        self.setNumberOfLines()
        self.number_of_lines_string = self.regulateStringUpToLengthWithCharacter(str(self.number_of_lines), REGULATED_LENGTH_FOR_NUMBER_OF_LINES, REGULATE_CHARACTER_FOR_NUMBER_OF_LINES)

    def setNumberOfLines(self):
        if os.path.exists(self.folder_name):
            file_list = os.listdir(self.folder_name)
            for file_name in file_list:
                source_file = None
                path = self.folder_name + PATH_SEPERATOR + file_name
                if os.path.isdir(path):
                    source_file = SourceFolder(path)
                else:
                    source_file = SourceFile(path)
                self.number_of_lines += source_file.number_of_lines
                self.file_list.append(source_file)
                
        else:
            print FOLDER_DOES_NOT_EXIST, self.folder_name

    def getInfo(self):
        info_string = self.regulated_folder_name + FOLDER_INFO_SEPERATOR + self.number_of_lines_string + INFO_DIMENSION_SEPERATOR + LINE_SINGULAR
        info_string = self.regulateStringForPlural(info_string, self.number_of_lines, LINE_PLURAL_SUFFIX)
        return info_string

    def printInfo(self):
        for source_file in self.file_list:
            source_file.printInfo()
        print self.getInfo()

class Application:
    def __init__(self):
        self.target_folder = self.getTargetFolder()
        SourceFolder(self.target_folder).printInfo()

    def getTargetFolder(self):
        if len(sys.argv) == 1:
            return "."
        return sys.argv[1]

Application()

import os

class ConfigFileParser:
    def __init__(self, file_name, splitter):
        self.file_name = file_name
        self.splitter = splitter
        self.table = {}
        self.parseFile()

    def parseFile(self):
        if not os.path.exists(self.file_name):
            #print "file does not exists", self.file_name
            return
        ftr = open(self.file_name)
        while True:
            line = ftr.readline()
            if not line:
                break
            s = line.split(self.splitter)
            if len(s) < 2:
                #print "invalid line:", line
                continue
            label = self.removeSpaces(s[0])
            value = self.removeSpaces(s[1])
            if len(label) < 1:
                #print "invalid label:", line
                continue
            if len(value) < 1:
                #print "invalid value:", line
                continue
            self.table[label] = value
        ftr.close()

    def getStrValue(self, label):
        return self.table[label]

    def getIntValue(self, label):
        value_str = self.table[label]
        try:
            int_value = int(value_str, 10)
            return int_value
        except:
            #print "label does not exist or value is invalid", label
            return 0

    def getBoolValue(self, label):
        value_str = self.table[label]
        if value_str.upper() == "TRUE":
            return True
        return False

    def getFloatValue(self, label):
        value_str = self.table[label]
        try:
            float_value = float(value_str)
            return float_value
        except:
            #print "label does not exist or value is invalid", label
            return 0.0

    def getStrArrayValue(self, label, splitter):
        value_str = self.table[label]
        return value_str.split(splitter)

    def getIntArrayValue(self, label, splitter):
        value_str = self.table[label]
        array_str = value_str.split(splitter)
        array_int = []
        for e in array:
            try:
                i = int(e, 10)
                array_int.append(i)
            except:
                #print "label does not exist or value is invalid", label
                array_int.append(0)
        return array_int

    def getBoolArrayValue(self, label, splitter):
        value_str = self.table[label]
        array_str = value_str.split(splitter)
        array_bool = []
        for e in array:
            if e.upper() == "TRUE":
                array_bool.append(True)
            else:
                array_bool.append(False)
        return array_bool

    def getFloatArrayValue(self, label, splitter):
        value_str = self.table[label]
        array_str = value_str.split(splitter)
        array_float = []
        for e in array:
            try:
                f = float(e)
                array_float.append(f)
            except:
                #print "label does not exist or value is invalid", label
                array_float.append(0.0)
        return array_float

    def removeSpaces(self, text):
        x = ""
        for char in text:
            if char != " " and char != "\t" and char != "\n":
                x += char
        return x

conf_file = ConfigFileParser("categories.txt", ":")
print conf_file.getStrValue("Category2")

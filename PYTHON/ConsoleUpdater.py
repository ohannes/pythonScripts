import os, sys, time

class ConsoleUpdater:
    def __init__(self):
        self.message = ""

    def cleanConsole(self):
        for char in self.message:
            sys.stdout.write("\b")
        sys.stdout.flush()

    def writeMessage(self, message, cleanConsole = True):
        if cleanConsole:
            self.cleanConsole()
        self.message = message
        sys.stdout.write(self.message)
        sys.stdout.flush()

def test():
    consoleUpdater = ConsoleUpdater()
    for i in range(101):
        consoleUpdater.writeMessage(str(i) + "% completed")
        time.sleep(0.1)
    print ""

test()

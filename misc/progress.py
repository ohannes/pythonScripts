import os, sys, time, threading

class ConsoleUpdater:
    def __init__(self):
        self.message = ""

    def writeToConsole(self, message):
        sys.stdout.write(message)
        sys.stdout.flush()

    def clearConsole(self):
        clear_message = "\b" * len(self.message)
        self.writeToConsole(clear_message)
        clean_message = " " * len(self.message)
        self.writeToConsole(clean_message)
        self.writeToConsole(clear_message)

    def writeMessage(self, message):
        self.clearConsole()
        self.message = message
        self.writeToConsole(self.message)

class ProgressViewer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.progress = 0
        self.message = ""
        self.console_updater = ConsoleUpdater()

        self.updateMessage()
        self.start()

    def updateProgress(self, progress):
        self.progress = int(round(progress))
        self.updateMessage()

    def updateMessage(self):
        self.message = str(self.progress) + "%"
        while len(self.message) < 5:
            self.message += " "

    def run(self):
        self.startActivity()

    def startActivity(self):
        number_of_dots = 0
        while True:
            message = self.message + "." * number_of_dots
            self.console_updater.writeMessage(message)
            number_of_dots += 1
            time.sleep(0.5)
            if number_of_dots >= 4:
                number_of_dots = 0

    def simulate(self):
        while self.progress < 100:
            self.updateProgress(self.progress+1)
            time.sleep(1)
        print ""

ProgressViewer().simulate()
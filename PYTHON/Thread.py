import threading, time, mutex

class ThreadX(threading.Thread):
    def __init__(self, callerMethod):
        threading.Thread.__init__(self)
        self.callerMethod = callerMethod
        self.cancelMutex = mutex.mutex()
        self.shouldCancel = False

    def run(self):
        while True:
            self.cancelMutex.lock()
            shouldCancel = self.shouldCancel
            self.cancelMutex.unlock()
            if(shouldCancel):
                break
            self.callerMethod()
            self.cancelMutex.unlock()
        print "END OF THREAD"
        
    def stop(self):
        self.cancelMutex.lock()
        self.shouldCancel = True
        self.cancelMutex.unlock()

class ClassX:
    def __init__(self, message, duration):
        self.message = message
        self.duration = duration
        self.timer = 0
        self.thread = ThreadX(self.threadMethod)
        self.thread.start()
        self.timerThread = ThreadX(self.timerMethod)
        self.timerThread.start()

    def threadMethod(self):
        print self.message
        time.sleep(1)

    def timerMethod(self):
        time.sleep(1)
        self.timer += 1
        if self.timer == self.duration:
            self.thread.stop()

    def join(self):
        self.thread.join()

    def cancel(self):
        try:
            self.thread._Thread__stop()
        except:
            print "Thread could not be killed"

class KillerX:
    def __init__(self, classToKill, timeForKill):
        self.classToKill = classToKill
        self.timeForKill = timeForKill
        self.timer = 0
        self.thread = ThreadX(self.threadMethod)
        self.thread.start()

    def threadMethod(self):
        while True:
            if self.timer == self.timeForKill:
                break
            self.timer += 1
            time.sleep(1)
        self.kill()

    def kill(self):
        self.classToKill.cancel()

def test():
    x = ClassX("Hello", 5)
    x.join()

test()

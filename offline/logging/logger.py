import os.path as path
from datetime import datetime

getSeverityString = {
    0: "INFO",
    1: "WARN",
    2: "ERROR"
}

class Logger:
    def __init__(self, pathToLogs, printSeverity=0):
        if not path.isdir(path.normpath(pathToLogs)):
            import pathlib
            raise ValueError(f"[ERROR] The logging path \"{path.normpath(pathToLogs)}\" was not a valid directory.")
        self.logPath = path.join(pathToLogs, datetime.now().strftime("log%d-%m-%y-T%H%M%S.log"))
        with open(self.logPath, "a") as f:
            f.write(f"Log for run at {datetime.now().strftime('%d-%m-%y-T%H:%M:%S')}\n")
        self.printSeverity = printSeverity # Messages with severity >= this will get printed
        self.defaultSeverity = 0 # The default severity for a message if none is provided

    def log(self, message, messageSeverity=-1):
        # If you pass in an invalid severity, or no severity then default to the logger default
        if not messageSeverity in {0, 1, 2}:
            messageSeverity = self.defaultSeverity
        loggingMessage = f"[{getSeverityString[messageSeverity]}]: {message}" # Magic f string formatting, could also include a timestamp?
        if messageSeverity >= self.printSeverity:
            print(loggingMessage) 
        with open(self.logPath, "a") as f:
            f.write(loggingMessage+"\n")

def testLogging():
    from tempfile import TemporaryDirectory
    import os
    with TemporaryDirectory() as tempDir:
        logger = Logger(tempDir, 1)
        logger.log("hello", 0)
        logger.log("another message", 1)
        logger.log("an error!", 2)
        numFiles = len(os.listdir(path.normpath(tempDir)))
        assert numFiles == 1, f"Wrong number of files: {numFiles}, expected 1"

if __name__ == "__main__":
    testLogging()
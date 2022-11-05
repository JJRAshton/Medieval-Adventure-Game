from enum import Enum
import os.path
from datetime import datetime

class Severity(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

class Logger:
    def __init__(self, pathToLogs, printSeverity=Severity.INFO):
        if not os.path.isDir(pathToLogs):
            raise ValueError("[ERROR] The logging path was not a valid directory.")
        self.logPath = os.path(pathToLogs, datetime.now().strftime("log%d-%m-%y-T%H:%M:%S"))
        self.printSeverity = printSeverity # Messages with severity >= this will get printed
        self.defaultSeverity = Severity.INFO # The default severity for a message if none is provided

    def log(self, message, severity=None):
        # If you pass in an invalid severity, or no severity then default to the logger default
        if not isinstance(severity, Severity):
            messageSeverity = self.defaultSeverity
        loggingMessage = f"[{messageSeverity}]: {message}" # Magic f string formatting, could also include a timestamp?
        if messageSeverity >= self.printSeverity:
            print(loggingMessage) 
        with open(self.logPath, "a") as f:
            f.write(loggingMessage)

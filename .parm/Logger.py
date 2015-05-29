import time
import sys
import os.path as path


class Logger:
    """Logger class used to remember log paths and verbosity"""

    @staticmethod
    def timestamp():
        """Return the time in the format [yy-mm-dd hh:mm:ss]"""
        form = '[%y-%m-%d %H:%M:%S]'
        timestamp = time.strftime(form)
        return timestamp

    def __init__(self, parameters):
        self.parameters = parameters
        self.verbose = parameters["verbose"]
        log_path = self.get_log_path()
        self.log_file = open(log_path, 'a')
        self.log("Logger initialized.")

    def __del__(self):
        """Make sure to close the log file!"""
        self.log_file.close()

    def log(self, message):
        """Write the message to the log file, print if verbose."""
        message = self.prepare_message(message)
        self.log_file.write(message)
        if self.verbose:
            print(message)

    def log_error(self):
        """Log the three pieces of an exception"""
        error = sys.exc_info()
        for i in error:
            self.log(str(i))

    def get_log_path(self):
        """Determines the path to the current logfile"""
        log_path = path.join(self.parameters["parm_path"], "logs")
        log_timestamp = time.strftime('%y-%m-%d')
        log_path = path.join(log_path, "log-" + log_timestamp + ".txt")
        return log_path

    def prepare_message(self, message):
        """Adds timestamp and strips whitespace from message"""
        return self.timestamp() + ' ' + message.strip('\n')

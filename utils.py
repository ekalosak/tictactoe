import logging
import logging.handlers
from os.path import exists, curdir, join
from os import makedirs
import time

class StdoutFormatter(logging.Formatter):
    # https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level
    err_fmt  = "ERROR: %(msg)s"
    dbg_fmt  = "DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "%(msg)s"
    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')  
    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt
        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = StdoutFormatter.dbg_fmt
        elif record.levelno == logging.INFO:
            self._style._fmt = StdoutFormatter.info_fmt
        elif record.levelno == logging.ERROR:
            self._style._fmt = StdoutFormatter.err_fmt
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)
        # Restore the original format configured by the user
        self._style._fmt = format_orig
        return result

def new_logger():
    """Create a new logger object using python's logging module"""
    appname = 'tictactoe'
    # TODO join source root, not curdir
    logdir = join(curdir, 'log')
    if not exists(logdir): makedirs(logdir)
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    logfn = join(logdir, appname + "_" + date + '.log')
    logger = logging.getLogger(appname)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler(logfn, 'a', 8*1024, 8)
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    fhfmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    chfmt = StdoutFormatter()
    fh.setFormatter(fhfmt)
    ch.setFormatter(chfmt)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return(logger)

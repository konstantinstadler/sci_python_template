""" template for python scripts following Pauliuk et al 2015 - Fig 1 


    In the file there is only one place to define/specify folders - the function 
    file_folder_specs().

    Notes
    ------
    The docstrings follow roughly the guidelines for numpy docstrings: http://sphinx-doc.org/latest/ext/example_numpy.html
        
    AUTHOR timestamp
    KST 20150625

    """

# general
import sys
import os
import logging
import collections
import subprocess
import pickle

# scientific
#import numpy as np
#import scipy.stats as ss
#import scipy.optimize as so
#import pandas as pd

# graphics
#import matplotlib.pyplot as plt
#import seaborn as sns

# testing - if tests should run with each script
#import pytest

def file_folder_specs():
    """ Get file and folder structure - the place to change folder information.

    Returns
    -------
    dict 
        File and folder specs

    """

    root = 'D:\KST\proj\template\template'
    files_folders = {
        'root' : root,
        #'data' : os.path.abspath(
                #os.path.join(root, 'data')
                #)
        }

    # we can also check for existence here to put everything in place
    #if not os.path.exists(files_folders[data]): os.makedirs(files_folders[data])

    return files_folders

def _start_logger(logfile = 'log.txt', filemode = 'w', detail = False):
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    loghandler = logging.FileHandler(logfile,filemode)
    loghandler.setLevel(logging.DEBUG)

    if detail:
        format = logging.Formatter("%(asctime)s %(msecs)d - %(levelname)s - %(module)s.%(funcName)s(%(lineno)d) - %(message)s [%(processName)s(%(process)d) %(threadName)s(%(thread)d)]" , datefmt='%Y%m%d %H%M%S')
    else:
        format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s" , datefmt='%Y%m%d %H%M%S')
    loghandler.setFormatter(format)
    log.addHandler(loghandler)   

    return loghandler

def _stop_logger(handler):
    handler.flush()
    handler.close()
    log = logging.getLogger()
    log.removeHandler(handler)

def main():
    # The programm code comes here

    # SETTINGS 
    ff = file_folder_specs()

    # READ DATA


    # ORGANIZE/CLEAN DATA
    

    # CALCULATIONS


    # FORMAT RESULTS


    # VISUALIZE


    # STORE


    return locals()


if __name__ == "__main__":
    # The main routine gets only started if the script is run directly. 
    # It only includes the logging boilerplate and a top level try-except for catching and logging all exceptions.

    # START LOGGING
    if not os.path.exists('./log'): os.makedirs('./log')
    log_summary = _start_logger(logfile = './log/process.log')
    #log_detail = _start_logger(logfile = './log/process_details.log', detail = True)
    logging.info('Start logging of {}'.format(__file__))

    # remove/change this try-excep depending on the version control used
    try: 
        logging.info("Current git commit: %s", 
                    subprocess.check_output(["git", "log", "--pretty=format:%H", "-n1"]).decode("utf-8"))
    except:
        logging.warn('Running without version control')

    # If you have quick test you can run them within the script, otherwise use py.test from the command line and delete these lines
    #if pytest.main() == 0:
        #logging.info("All tests passed")
    #else:
        #logging.error("Some tests not passed!")

    # MAIN PROGRAMM
    # remove the try-except if exception should just stop the programm, but remember to end the program with the _stop_logger functions.
    try:
        # The following update your local namespace with the variables from main()
        locals().update(main())
        # if you don't want the script to pollute your namespace use 
        # which gives you all varibales from main in a dict called 'results'
        #results = main()
    except Exception as exc:
        logging.exception(exc)
        raise
    finally:
        # STOP LOGGER - clean
        _stop_logger(log_summary)
        #_stop_logger(log_detail)






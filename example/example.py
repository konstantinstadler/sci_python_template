""" Example of using the template for an analysis


    Notes
    ------
    This script requires a internet connection (data is downloaded from the World Bank server) and
    the pandas and seaborn module.
        
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
import itertools

# scientific
#import numpy as np
#import scipy.stats as ss
#import scipy.optimize as so
import pandas as pd
import pandas.io.wb

# graphics
import matplotlib.pyplot as plt
import seaborn as sns

# testing - if tests should run with each script
import pytest

def file_folder_specs():
    """ Get file and folder structure - the place to change folder information.

    Returns
    -------
    dict 
        File and folder specs

    """

    root = os.path.dirname(os.path.abspath(__file__))
    # folder structure
    files_folders = {
        'root' : root,
        'data' : os.path.abspath(
                os.path.join(root, 'data')
                ),
        'fig' : os.path.abspath(
                os.path.join(root, 'fig')
                )
        }
    
    # update the specific files used
    files_folders.update({'result_file' : os.path.join(
                                            files_folders['data'],
                                            'research_outcome.csv'
                                            )})

    folders_to_check = ['data', 'fig']
    # we can also check for existence here to put everything in place
    for folder in folders_to_check:
        if not os.path.exists(files_folders[folder]): os.makedirs(files_folders[folder])

    return files_folders

def get_wb_data(indi, year = 2007):
    """ Get world bank data for the indicators specified

    Parameters
    ----------

    indi : dict
        Dictionary with 
            wbcode : name
        The name is used a column header for the return dataframe

    year : int, optional
        Year of the analysis (default: 2007)

    Returns
    -------
    pandas DataFrame
        With countries as index and name from indi as columns

    """
    logging.info('Reading data for {} for {}'.format(indi, year))
    wbres = pd.io.wb.download(indicator = list(indi.keys()), 
                            start = year, end = year, 
                            country = "all")
    wbres.columns = [indi[nn] for nn in wbres.columns]
    return wbres


def fig_correlations(data, aly_title, fig_save = True):
    """ Plot correlations

    Parameters
    ----------
    data : pd.DataFrame
    aly_title : str
    fig_save : bool, optional
        False if data should not be saved
        

    """
    ff = file_folder_specs()

    plt.figure()
    sns.corrplot(data, diag_names = False)
    plt.title(aly_title)
    if fig_save:
        _save_fig(aly_title, ff['fig'])
    plt.show()
    plt.close()

def fig_linplot(data, x , y, aly_title, fig_save = True):
    """ Plot correlations

    Parameters
    ----------
    data : pd.DataFrame
    x,y : str
        X and Y axis for the plot, valid column names of data
    aly_title : str
    fig_save : bool, optional
        False if data should not be saved
        

    """
    ff = file_folder_specs()

    title = aly_title + 'for {} vs {}'.format(x, y)
    sns.regplot(x ,y , data = data)
    plt.title(title)
    plt.xlim(0)
    plt.ylim(0)
    if fig_save:
        _save_fig(title, ff['fig'])
    plt.show()
    plt.close()


def fig_all_linplot(data, aly_title, fig_save = True):
    """ Plot correlations

    Parameters
    ----------
    data : pd.DataFrame
    aly_title : str
    fig_save : bool, optional
        False if data should not be saved
        

    """
    ff = file_folder_specs()

    for pairs in itertools.combinations(data.columns,2):
        title = aly_title + 'for {} vs {}'.format(pairs[0], pairs[1])
        sns.regplot(pairs[0], pairs[1], data = data)
        plt.title(title)
        plt.xlim(0)
        plt.ylim(0)
        if fig_save:
            _save_fig(title, ff['fig'])
        plt.show()
        plt.close()

def _save_fig(name, path): 
    """ Routine for saving figure

    Parameters
    ----------

    Returns
    -------
    TYPE

    """
    path = os.path.abspath(path)
    file_format = 'png'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    file_name = "".join(letter for letter in name.replace(' ','_') 
                if letter.isalnum() or letter is '_') + '.' + file_format
    while(file_name.find('__') > 0): 
        file_name=file_name.replace('__','_')
    plt.savefig(os.path.join(path,file_name),dpi=600,bbox_inches='tight')



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
    fig_save = True  # save figures?
    logging.info('Saving figures: {}'.format(fig_save))

    sci_indicators = {
        "NY.GDP.MKTP.CD"    : "GDP",
        "SP.POP.TOTL"       : "population",
        "IP.JRN.ARTC.SC"    : "scientific_articles",
        "GB.XPD.RSDV.GD.ZS" : "rd_expend_per_gdp",
    }

    # READ DATA
    research_outcome = get_wb_data(sci_indicators)

    # ORGANIZE/CLEAN DATA
    research_outcome.dropna(inplace = True)

    # CALCULATIONS
    logging.info('Calculate results...')
    research_outcome['rd_expend_per_pop'] = research_outcome['rd_expend_per_gdp'] * research_outcome['GDP'] / research_outcome['population']
    research_outcome['scientific_articles_per_pop'] = research_outcome['scientific_articles'] / research_outcome['population']
    research_outcome['scientific_articles_per_gdp'] = research_outcome['scientific_articles'] / research_outcome['GDP']

    # VISUALIZE
    logging.info('Visualizing results...')
    sns.set_context('poster')
    fig_correlations(research_outcome, aly_title = 'Pairwise correlations of scientific outcome', fig_save = fig_save)
    fig_linplot(research_outcome, 
                x = 'rd_expend_per_gdp',
                y = 'scientific_articles_per_gdp', 
                aly_title = 'Linear relation', 
                fig_save = fig_save) 
    #fig_all_linplot(research_outcome, aly_title = 'Linear relation', fig_save = fig_save)  # all linear relatioships - a lot of figures

    # STORE
    logging.info('Saving...')
    research_outcome.to_csv(ff['result_file'])

    logging.info('Analysis completed')
    return locals()


if __name__ == "__main__":
    # The main routine gets only started if the script is run directly. 
    # It only includes the logging boilerplate and a top level try-except for catching and logging all exceptions.

    # START LOGGING
    if not os.path.exists('./log'): os.makedirs('./log')
    log_summary = _start_logger(logfile = './log/process.log')
    log_detail = _start_logger(logfile = './log/process_details.log', detail = True)
    logging.info('Start logging of {}'.format(__file__))

    # remove/change this try-excep depending on the version control used
    try: 
        logging.info("Current git commit: %s", 
                    subprocess.check_output(["git", "log", "--pretty=format:%H", "-n1"]).decode("utf-8"))
    except:
        logging.warn('Running without version control')

    # If you have quick test you can run them within the script, otherwise use py.test from the command line and delete these lines
    if pytest.main() == 0:
        logging.info("All tests passed")
    else:
        logging.error("Some tests not passed!")

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
        _stop_logger(log_detail)






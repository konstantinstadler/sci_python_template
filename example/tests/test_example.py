""" Example testing file for the template based on py.test

http://pytest.org

"""

# modules needed for the testing
import os
import sys

# The following puts the path below in the testing path register to make the top-level
# script importable
_scriptpath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _scriptpath + '/../')

# the module/script to be tested
import example as extt

def test_file_folder_specs():
    assert type(extt.file_folder_specs()) is dict


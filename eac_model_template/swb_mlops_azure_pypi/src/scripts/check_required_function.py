"""
The function aims to verify the existence of training.py, scoring.py and the existence of the function themselves.
Locate the model_src or model_modules
assert the existence of scoring.py
    assert the existence of score() and evaluate()
assert the existence of training.py if supervised
    assert the existence of train()

"""

import ast
import os
import fnmatch


def find_file(directory='.', file_to_find='training.py') -> bool:
    """
    The glob function will look in the current directory, to fall back we need to use ../.

    """
    print("looking for notebooks")
    result = []
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, file_to_find):
            result.append(file)
    if len(result) == 0:
        print('No file found with the format specified')
        return False
    print("found files : {}".format(result))
    return True


def find_training(directory='.'):
    if find_file(directory=directory, file_to_find='training.py'):
        print("Training was found")
        return True
    else:
        print("Could not find the training.py")
        return False


def find_scoring(directory='.'):
    if find_file(directory=directory, file_to_find='scoring.py'):
        print("scoring was found")
        return True
    else:
        print("Could not find the scoring.py")
        return False


def search_function(file_to_search: str,
                    function_to_search: str):
    with open(file_to_search, 'rb') as f:
        tree = ast.parse(f.read(-1))
    print("looking for function {}".format(function_to_search))
    for each in function_to_search:
        tab = [x.name for x in ast.walk(tree) if isinstance(x, ast.FunctionDef) and x.name == each]
        # the search returns a list
        # if the function is found then the list is not empty
        if len(tab) >= 1:
            print("function : {} in file {} was found".format(function_to_search, file_to_search))
            return True
        else:
            print("Error : function {} in file {} was not found".format(function_to_search, file_to_search))
            raise LookupError


def validate(directory: str,
             model_type: str):
    """
    This is the general function that validate the whole structure.
    If this passes then the pipeline can move further
    """
    if model_type == 'supervised':
        if find_training(directory=directory) and find_scoring(directory=directory):
            print("Found files for supervised model")
        else:
            print("Some files are missing")
        print("verifying functions")
        if search_function(directory + 'scoring.py', ['evaluate']) and \
                search_function(directory + 'scoring.py', ['score']) and \
                search_function(directory + 'training.py', ['train']):
            print("All functions found")
        else:
            print("the file is missing some function")

    if model_type == 'rulebased':
        if find_scoring(directory=directory):
            print("Found files for rule based model")
        else:
            print("Some files are missing")
        print("verifying functions")
        if search_function(directory + 'scoring.py', ['evaluate']) and \
                search_function(directory + 'scoring.py', ['score']):
            print("All functions found")
        else:
            print("the file is missing some function")

# Databricks notebook source
import os

import pandas as pd
q = spark.sql("select * from top95")


# COMMAND ----------

# MAGIC %sh ls

# COMMAND ----------


from z3 import * # z3 is a theorem prover by Microsoft research. In our case we will use it as a constaint solver.

def solver(data):
    '''
    Here we are going to implement the solver itself.
    The input will be an array of soduku lines.
    
    Here is an example of a line:
    4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
    where :
    . are unknown
    # are fixed values ie constrains
    

    The rules :
    values are comprise in range 1 to 9
    a soduku is 9x9 square
    each line must have distinct value
    each column must have distinct value
    each sub 3x3 square must have a distinct value
    optional: the diagonal values can also be distinct

    from the example above, the square will be :
    4.....8.5
    .3.......
    ...7.....
    .2.....6.
    ....8.4..
    ....1....
    ...6.3.7.
    5..2.....
    1.4......
    
    '''
    # Here are the constraints
    # 9x9 matrix of integer variables
    X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(9) ]
        for i in range(9) ]

    # each cell contains a value in {1, ..., 9}
    cells_c  = [ And(1 <= X[i][j], X[i][j] <= 9)
                for i in range(9) for j in range(9) ]

    # each row contains a digit at most once
    rows_c   = [ Distinct(X[i]) for i in range(9) ]

    # each column contains a digit at most once
    cols_c   = [ Distinct([ X[i][j] for i in range(9) ])
                for j in range(9) ]

    # each 3x3 square contains a digit at most once
    sq_c     = [ Distinct([ X[3*i0 + i][3*j0 + j]
                            for i in range(3) for j in range(3) ])
                for i0 in range(3) for j0 in range(3) ]

    sudoku_c = cells_c + rows_c + cols_c + sq_c
    print("original table : {}".format(data))
    # Here is the instance
    instance_c = [ If(data[i][j] == 0,
                  True,
                  X[i][j] == data[i][j])
               for i in range(9) for j in range(9) ]
    s = Solver() # This is an Z3 instance solver
    s.add(sudoku_c + instance_c) # Adding all the contraints together
    if s.check() == sat: # Z3 will evaluate if there is a solution that satifies all constraints
        m = s.model()
        r = [ [ m.evaluate(X[i][j]) for j in range(9) ]
            for i in range(9) ]
        print("solved soduku :")
        print(r)
        return r
    else:
        print("failed to solve")
        return False




# COMMAND ----------

import urllib.request


def read_dataset_from_url(spark, url):
    # for this demo we're downloading the dataset locally and then reading it. This is obviously not production setting
    # https://raw.githubusercontent.com/apache/spark/branch-2.4/data/mllib/sample_libsvm_data.txt
    urllib.request.urlretrieve(url, "/tmp/data.txt")
    return spark.read.format("libsvm").load("/tmp/data.txt")


def read_from_line(line):
    '''
    The function converts are string into a list of list to look like a matrix.
    : param line : a line of 81 characters where unknowns are '.'
    '''

    # We just convert the line of data into a matrix of int
    # the string needs to be 81 characters
    if len(line) < 81:
        print("problem submitted is less that 81 characters : {}".format(len(line)))
        exit()
    numbers = [int(c) if c != '.' else 0 for c in line]
    output = []
    for i in range(0,len(line),9):
            output.append(numbers[i:i+9])

    return output

# COMMAND ----------

import logging
import joblib
import json
from pyspark import SparkConf
from pyspark.sql import SparkSession
#from .solver import solver  # import your own module containing function
#from .util import read_from_line

logging.getLogger("py4j").setLevel(logging.INFO)

# spark name and other properties are set by the framework launcher in spark-submit. don't override
spark = SparkSession.builder \
    .config(conf=SparkConf()) \
    .enableHiveSupport() \
    .getOrCreate()


def train(data_conf, model_conf, **kwargs):
    '''
    Even if this is a rule based model we still need to have a function.
    This function can still help you to verify that your rules are correct against specific dataset.
    '''
    
    
    #  Model_conf contains hyperparmater but in this case it can be setup parameter for this instance
    # we need to query the data base :
    hive_sql = "select {} from {}".format(data_conf["column"],
                                            data_conf["table"])
    df_raw = spark.sql(hive_sql)
    #df_raw.show()
    #  Since we do not need a pyspark dataframe we will convert it to pandas and then send it to our functions
    pdd=df_raw.toPandas()
    # from this function we are sending the dataset line by lines
    solved = 0
    unsolved = 0
    for i in range(0,pdd["problems"].size-1):
        print("here is a line : {}".format(pdd["problems"][i]))
        problem_array = read_from_line(pdd["problems"][i])
        if solver(problem_array) == False:
            unsolved = unsolved + 1 
        else :
            solved = solved +  1

    results={}
    results["solved"]=solved
    # We need to create a dummy model file because the framwork is expecting a model
    with open("models/results.json", "w+") as f:
        json.dump(results, f)
    logging.info("solved {} soduku".format(solved))
    logging.info("unsolved {} soduku".format(unsolved))
    return solved


# COMMAND ----------

data_conf={}
data_conf["column"] = "problems"
data_conf["table"] = "top95"
model_conf={}
train(data_conf,model_conf)


# COMMAND ----------



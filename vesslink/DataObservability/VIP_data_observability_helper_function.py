import pandas as pd
import requests 
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
from time import time, sleep
from itertools import repeat
import json
from jsondiff import diff
import random
import os
import sys
import boto3
import botocore
import concurrent.futures
import plotly.express as px
import gzip

def initAWSClient(aws_access_key_id, aws_secret_access_key, bucket, proxy):
    '''
    Initialize a connection to AWS S3
    '''
    try:
        session = boto3.session.Session(aws_access_key_id, aws_secret_access_key)
        botoconfig = botocore.config.Config(proxies=proxy)
        s3 = session.resource('s3', config=botoconfig)
        client = boto3.client(
            's3',
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key,
            config=botoconfig
        )
        bucket=bucket
        BUCKET = s3.Bucket(bucket)
        if client !=None:
            print('AWS S3 client created')
            return (s3,client,BUCKET)
    except Exception as e:
        print('\n initAWSClient function: \n', e)
        return None

def prepare_folder(name,clear=False):
    '''
    Create a folder to store analysis csv files, optional: clear files in folder
    '''
    try:
        current_directory = os.getcwd()
        directory = os.path.join(current_directory, name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if clear:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath) or os.path.islink(filepath):
                    os.unlink(filepath)
        print(f'folder "{name}" created')
        return directory
    except Exception as e:
        print('\n prepare_folder function: \n', e)
        return None

def getTimeSeries(tStart,tEnd, security):
    '''
    Get a time series in between 2 dates. Security (in minutes) limits the inclusion of a timeslot only if the current numbers of          minutes of the current time is bigger than the security. Example: if the current datetime is 2022/05/16 08:31 and the security
    is 30, the timeslot '2022051608' will not be included.
    '''
    try:
        if tStart < tEnd:
            dtFormat = '%Y%m%d%H'
            tSeries = [tStart.strftime(dtFormat)]
            date_time = tStart
            to_date_time = tEnd+timedelta(hours=-1)
            while date_time < to_date_time:
                date_time += timedelta(hours=1)
                tSeries.append(date_time.strftime(dtFormat))
            if tEnd.minute < 30:
                tSeries = tSeries[:-1] 
            return tSeries
        else:
            return None
    except Exception as e:
        print('\n getTimeSeries function: \n', e)
        return None

def getMissingTimeSlots(csv_directory,file, security):
    '''
    Check missing records from the historical data. Generated a lst of timestamps from the gap between the latest extracts on S3
    and the current time.
    '''
    try:
        path = f"{csv_directory}/{file}"
        df=pd.read_csv(path)
        lastDate=datetime.strptime(df['date'].iloc[-1],'%Y%m%d-%H')
        missingTimeSlots=getTimeSeries(lastDate+timedelta(hours=1),datetime.utcnow(), security)
        return missingTimeSlots
    except Exception as e:
        print('\n getMissingTimeSlots function: \n', e)
        return None

def getListFilesDay(BUCKET, t):
    '''
    Get the list of files for a specific day
    parameter t is the date as string with the format '%Y%m%d%H'
    '''
    try:
        day=t[:-2]
        hour=t[-2:]
        Prefix=f'IMOSDL/Hourly/{day}' if hour is None else f'IMOSDL/Hourly/{day}/{hour}'
        listFiles=[s3_file.key for s3_file in BUCKET.objects.filter(Prefix=Prefix)]
        file=[s3_file.split('/')[4] for s3_file in listFiles]
        return file
    except Exception as e:
        print('\n getListFilesDay function: \n', e)
        return None

def getAllJobsbMetrics(BUCKET, ts, csv, csv_directory, filename):
    '''
    Function to generate the historical tables metrics dataframe of extracted data on S3.
    A csv file can be saved optionally.
    Parameters: 
    - BUCKET (S3 config)
    - ts: Time series: list of timestamps
    - csv: boolean
    - csv_directory, filename: String
    '''
    try:
        def getJobMetrics(BUCKET, ts):
            day=ts[:-2]
            hour=ts[-2:]
            date=day +'-'+ hour
            delivery=1 if len(getListFilesDay(BUCKET, ts))>0 else 0
            expectation=1
            df=pd.DataFrame({'date': [date],
                            'jobDelivered' : [delivery],
                            'JobExpected' : [expectation]})
            return df
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                res = list(executor.map(getJobMetrics, repeat(BUCKET),ts))
        if res!= []:
            dfMerge=pd.concat(res, ignore_index = True, axis = 0)
            if csv:
                path=f"{csv_directory}/{filename}"
                dfMerge.to_csv(path,index=False)
            return dfMerge
        else:
            return None
    except Exception as e:
        print('\n getAllJobsbMetrics function: \n', e)
        return None


def getDeltaJobsbMetrics(BUCKET, csv_directory, missingTimeSlots, historical_job_metrics_file_name, security, csv = False):
    '''
    Function to update the historical tables metrics dataframe of extracted data on S3. Requires a list of timestamp.
    '''
    try:
        path = f"{csv_directory}/{historical_job_metrics_file_name}"
        df=pd.read_csv(path)
        lastDate=datetime.strptime(df['date'].iloc[-1],'%Y%m%d-%H')
        missingTimeSlots=getTimeSeries(lastDate+timedelta(hours=1),datetime.utcnow(),security)
        if missingTimeSlots!=None:
            df2=getAllJobsbMetrics(BUCKET, missingTimeSlots, csv, csv_directory, historical_job_metrics_file_name)
            dfMerge=pd.concat([df, df2], ignore_index = True, axis = 0)
            dfMerge.to_csv(path,index=False)
            print('Saved')
        else:
            dfMerge=df
        return dfMerge
    except Exception as e:
        print('\n getDeltaJobsbMetrics function: \n', e)
        return None

def getAllTablesbMetrics(client, BUCKET, bucket, tablesOutOfScopeVeson, ts, csv, csv_directory, filename):
    '''
    Function to generate an historical tables metrics dataframe of extracted data on S3. Requires a list of timestamp.
    A csv file can be saved optionally.
    Parameters: 
    - client, BUCKET, bucket (S3 config)
    - ts: Time series: list of timestamps
    - csv: boolean
    - csv_directory, filename: String
    '''
    try:
        def getTableMetrics(client, BUCKET, bucket, tablesOutOfScopeVeson, ts):
            try:
                day=ts[:-2]
                hour=ts[-2:]
                date=day +'-'+ hour
                uniqueTablesSchema=getListTablesCurrentSchema(client, bucket, ts)
                if uniqueTablesSchema!=None:
                    uniqueTablesSchemaAdjusted=sorted(list(set(uniqueTablesSchema).difference(tablesOutOfScopeVeson)))
                    uniqueTablesJob=getListTablesCurrentJob(BUCKET, ts)
                    missingTables=sorted(list(set(uniqueTablesSchemaAdjusted).difference(uniqueTablesJob)))
                    tablesDelivered=len(uniqueTablesSchemaAdjusted)-len(missingTables)
                    tablesExpected=len(uniqueTablesSchemaAdjusted)
                    completenessRatio=1-(len(missingTables)/len(uniqueTablesSchema))
                    df=pd.DataFrame({
                        'date': [date],
                        'tablesDelivered' : [tablesDelivered],
                        'tablesExpected' : [tablesExpected],
                        'missingTables': [len(missingTables)],
                        'missingTablesList':[missingTables],
                        'completenessRatio': [round(tablesDelivered/tablesExpected,4)]
                        })
                    return df
                else: 
                    return None     
            except Exception as e:
                print('\n getTableMetrics function: \n', e)
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            res = list(executor.map(getTableMetrics, repeat(client), repeat(BUCKET), repeat(bucket), repeat(tablesOutOfScopeVeson), ts))
        if set(res)!={None}:
            dfMerge=pd.concat(res, ignore_index = True, axis = 0)
            if csv:
                path=f"{csv_directory}/{filename}"
                dfMerge.to_csv(path,index=False)
        else:
            dfMerge= None
        
        return dfMerge
    except Exception as e:
        print('\n getAllTablesbMetrics function: \n', e)
        return None

def getDeltaTablesbMetrics(client, BUCKET, bucket, tablesOutOfScopeVeson, ts, csv, csv_directory, filename, security):
    try:
        path = f"{csv_directory}/{filename}"
        df=pd.read_csv(path)
        lastDate=datetime.strptime(df['date'].iloc[-1],'%Y%m%d-%H')
        missingTimeSlots_table=getTimeSeries(lastDate+timedelta(hours=1),datetime.utcnow(), security)
        if len(missingTimeSlots_table)>0 and missingTimeSlots_table!=None:
            df2=getAllTablesbMetrics(client, BUCKET, bucket, tablesOutOfScopeVeson, ts, csv, csv_directory, filename)
            dfMerge=pd.concat([df, df2], ignore_index = True, axis = 0)
            dfMerge.to_csv(path,index=False)
        else:
            dfMerge=df
        return dfMerge
    except Exception as e:
        print('\n getDeltaTablesbMetrics function: \n', e)
        return None

def getAllJobsSizeMetrics(BUCKET, ts, csv,csv_directory, filename):
    try:
        def getJobSize(BUCKET, t):
            try:
                day=t[:-2]
                hour=t[-2:]
                date=day +'-'+ hour
                prefix=f'IMOSDL/Hourly/{day}/{hour}'
                size = int(sum([obj.size for obj in BUCKET.objects.filter(Prefix=prefix)])/1000)
                files = int(sum([1 for obj in BUCKET.objects.filter(Prefix=prefix)]))
                df=pd.DataFrame({'date': [date],
                                'size' : [size],
                                'files' : [files]})
                return df
            except Exception as e:
                print('\n getJobSize function: \n', e)
                return None
        if ts !=None:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                res = list(executor.map(getJobSize, repeat(BUCKET),ts))
            dfMerge=pd.concat(res, ignore_index = True, axis = 0)

            if csv:
                path=f"{csv_directory}/{filename}"
                dfMerge.to_csv(path,index=False)
                return dfMerge
            else:
                return dfMerge
        else:
            return None
    except Exception as e:
        print('\n getAllJobsSizeMetrics function: \n', e)
        return None

def getDeltaJobsSizeMetrics(BUCKET,security, ts, csv, csv_directory, filename):
    try:
        path = f"{csv_directory}/{filename}"
        df=pd.read_csv(path)
        lastDate=datetime.strptime(df['date'].iloc[-1],'%Y%m%d-%H')
        missingTimeSlots_jobSize=getTimeSeries(lastDate+timedelta(hours=1),datetime.utcnow(), security)
        print()
        if missingTimeSlots_jobSize!=[]:
            df2=getAllJobsSizeMetrics(BUCKET, ts, csv, csv_directory, filename)
            dfMerge=pd.concat([df, df2], ignore_index = True, axis = 0)
            dfMerge.to_csv(path,index=False)
            return dfMerge
        else:
            dfMerge=df
            return dfMerge
    except Exception as e:
        print('\n getDeltaJobsSizeMetrics function: \n', e)
        return None

def getListTablesCurrentSchema(client, bucket, t):
    '''
    Function to get the list of all tables from the current schema
    '''
    try:
        if loadSchema(client, bucket, t) != None:
            ListTablesCurrentSchema=sorted([i['DataObjectName'] for i in loadSchema(client, bucket, t)])
            return(ListTablesCurrentSchema)
        else:
            return None
    except Exception as e:
        print('\n getListTablesCurrentSchema function: \n', e)
        return None

def loadSchema(client,bucket,t):
    '''
    Function to load and unzip a specific table (zipped json) form from an S3 Bucket
    '''
    day=t[:8]
    hour=t[8:]
    Key=f'IMOSDL/Hourly/{day}/{hour}/_MasterTableSchema.json'
    try:
        result = client.list_objects_v2(Bucket=bucket, Prefix=Key)
        if 'Contents' in result:
            obj = client.get_object(
                Bucket = bucket,
                Key = Key
            )
            filedata = json.loads(obj['Body'].read())
            return filedata
        else:
            return None
    except Exception as e:
        print('\n loadSchema function: \n', e)
        return None


def getListTablesCurrentJob(BUCKET, t):
    try:
        ListTablesCurrentJob=sorted(list(set([i.split('_')[0] for i in getListFilesDay(BUCKET, t)])))
        return(ListTablesCurrentJob)
    except Exception as e:
        print('\n getListTablesCurrentJob function: \n', e)
        return None

def aggregateJobMetrics(dt): 
    dt['day'] = dt.apply(lambda x: x['date'][:8],axis=1)
    dt=dt.groupby('day').sum()
    dt['successRatio']=dt.apply(lambda x: x['jobDelivered']/x['JobExpected'],axis=1)
    return dt

def aggregateTableMetrics(dt): 
    dt['day'] = dt.apply(lambda x: x['date'][:8],axis=1)
    dt=dt.groupby('day').mean()
    return dt

def drawScatterSingleLine(go,  x, y, track, title, xaxis, yaxis, w, h, font):
    dt = go.Figure()
    dt = dt.add_trace(go.Scatter(x = x, y = y, name = track))
    dt.update_layout(title=title,xaxis_title=xaxis,yaxis_title=yaxis,width=w,height=h,font=font)
    dt.show()

def drawScatterDoubleLine(go, x, y1, y2, track1, track2, title, xaxis, yaxis, w, h, font):
    dt= go.Figure()
    dt = dt.add_trace(go.Scatter(x = x, y = y1, name = track1))
    dt = dt.add_trace(go.Scatter(x = x, y = y2, name = track2))
    dt.update_layout(title=title,xaxis_title=xaxis,yaxis_title=yaxis,width=w,height=h,font=font)
    dt.show()

def drawScatterTripleLine(go, x, y1, y2, y3, track1, track2, track3, title, xaxis, yaxis, w, h, font):
    dt= go.Figure()
    dt = dt.add_trace(go.Scatter(x = x, y = y1, name = track1))
    dt = dt.add_trace(go.Scatter(x = x, y = y2, name = track2))
    dt = dt.add_trace(go.Scatter(x = x, y = y3, name = track3))
    dt.update_layout(title=title,xaxis_title=xaxis,yaxis_title=yaxis,width=w,height=h,font=font)
    dt.show()

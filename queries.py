#!/usr/bin/python
# encoding: utf-8

"""
Defines queries and execution functions for calling the Bear sqlite DB.
"""

import sqlite3
import os

DB_LOCATION = "⁨/⁨Library⁩/⁨Application Support⁩/⁨info.eurocomp.Timing2⁩/SQLite.db"
DB_KEY = "db_path"

RECENT_TASKS =  "SELECT DISTINCT TaskActivity.title, Project.title FROM TaskActivity INNER JOIN Project ON TaskActivity.projectID=Project.id WHERE TaskActivity.isDeleted=0 ORDER BY TaskActivity.endDate DESC LIMIT 10"
  
TASKS_BY_TITLE = "SELECT DISTINCT TaskActivity.title, Project.title FROM TaskActivity INNER JOIN Project ON TaskActivity.projectID=Project.id WHERE TaskActivity.isDeleted=0 AND lower(TaskActivity.title) LIKE lower('%{0}%')"

def list_recent_tasks(workflow, log, query):
    """
    List recent tasks
    """
    sql_query = RECENT_TASKS
    return run_query(workflow, log, sql_query)
    
def search_tasks_by_title(workflow, log, query):
    """
    Searches for tasks by the title of the task.
    """
    sql_query = TASKS_BY_TITLE.format(query)
    return run_query(workflow, log, sql_query)
    
def run_query(workflow, log, sql):
    """
    Takes a SQL command, executes it, and returns the results.
    """
    db_path = workflow.stored_data(DB_KEY)
    if not db_path:
        db_path = find_bear_db(log)
        workflow.store_data(DB_KEY, db_path)
    else:
        log.debug(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    log.debug(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    log.debug("Found {0} results".format(len(results)))
    cursor.close()
    return results

def find_timingdb(log):
    """
    Finds the Timing sqlite3 DB.
    """
    home = os.path.expanduser("~")
    db_file = "{0}{1}".format(home, DB_LOCATION)

    if not os.path.isfile(db_file):
        log.debug(
            "Timing db not found at {0}".format(db_file))

    log.debug(db_file)
    return db_file

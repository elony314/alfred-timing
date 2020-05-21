#!/usr/bin/python
# encoding: utf-8

"""
Main search script for alfred-bear workflow.
"""

import sys
import argparse
import queries
import json
from workflow import Workflow, ICON_SYNC

SINGLE_QUOTE = "'"
ESC_SINGLE_QUOTE = "''"

# Update workflow from GitHub repo
UPDATE_SETTINGS = {'github_slug': 'elony314/alfred-timing'}
SHOW_UPDATES = True

WORKFLOW = Workflow(update_settings=UPDATE_SETTINGS)
LOGGER = WORKFLOW.logger

def main(workflow):
    if SHOW_UPDATES and workflow.update_available:
        workflow.add_item('A new version is available',
                          'Action this item to install the update',
                          autocomplete='workflow:update',
                          icon=ICON_SYNC)

    LOGGER.debug('Started workflow')
    args = parse_args()
    
    if args.pause:
        LOGGER.debug("Pause timing task")
        WORKFLOW.add_item(title="Pause current task", arg='pause', valid=True)
    elif args.query:
        query = args.query[0]
        query = query.encode('utf-8')
        LOGGER.debug("Searching tasks for %s", format(query))
        execute_search_query(query)
    else:
        raise Exception("Cannot parse")

    workflow.send_feedback()

def parse_args():
    """
    Parses out the arguments sent to the script in the Alfred workflow.
    """
    parser = argparse.ArgumentParser(description="Parse Tasks Argument")

    parser.add_argument('--pause', '-p', action='store_true', help="pause current task")
    parser.add_argument('query', type=unicode, nargs=argparse.REMAINDER, help='query to start a task')

    LOGGER.debug(WORKFLOW.args)
    args = parser.parse_args(WORKFLOW.args)
    return args


def execute_search_query(query):
    """
    Decides what search to run based on args that were passed in and executes the search.
    """
    if query: # user has input, search based on input
        LOGGER.debug('Searching tasks')
        
        # escape single quote
        query = query.replace(SINGLE_QUOTE, ESC_SINGLE_QUOTE)
        
        task_results =  queries.search_tasks_by_title(WORKFLOW, LOGGER, query)
    
    else: #  user has not input, List recent tasks
        LOGGER.debug('List recent tasks')
        task_results = queries.list_recent_tasks(WORKFLOW, LOGGER, query)
    
    if not task_results:
        WORKFLOW.add_item(title="No tasks found. Add it as a new task?", arg=json.dumps({"task_name": query}), valid=True)
    else:
        for task_result in task_results:
            LOGGER.debug(task_result)
            # since project name can be duplicated, the project id is required
            if task_result[1] != None:
                json_arg = json.dumps({"task_name": task_result[0], "proj_name":task_result[1], "proj_id":str(task_result[2])})
            else:
                json_arg = json.dumps({"task_name": task_result[0]})
            
            LOGGER.debug(json_arg)
            WORKFLOW.add_item(title=task_result[0], subtitle="Project: {}".format(task_result[1]), arg=json_arg, valid=True)


if __name__ == '__main__':
    sys.exit(WORKFLOW.run(main))

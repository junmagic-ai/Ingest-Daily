# This script is used to interact with Google Tasks API.
# It includes functions to authenticate the API, mark a task as completed, and fetch open tasks and mark them as completed.
# The 'authenticate_google_tasks_api' function checks if a token.pickle file exists, which stores the user's access and refresh tokens.
# If the file exists, it loads the credentials from the file.
# If the file does not exist or the credentials are not valid, it lets the user log in and saves the credentials in token.pickle for future use.
# The 'mark_task_as_completed' function marks a specific task as completed.
# The 'fetch_and_complete_tasks' function fetches open tasks and marks them as completed.


import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Authentication and Token Setup
def authenticate_google_tasks_api():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json',
                scopes=['https://www.googleapis.com/auth/tasks']  # Changed scope to allow modifications
            )
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Mark a task as completed
def mark_task_as_completed(service, tasklist_id, task_id):
    try:
        print(f"Marking task with ID {task_id} in list {tasklist_id} as completed.")
        task = {'id': task_id, 'status': 'completed'}
        response = service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
        print("Task marked as completed:", response)
    except Exception as e:
        print(f"Error marking task as completed: {e}")

# Fetch Open Tasks and Mark Them as Completed
def fetch_and_complete_tasks():
    creds = authenticate_google_tasks_api()
    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    tasklists = results.get('items', [])

    open_tasks = []  # List to store open tasks

    if not tasklists:
        print('No task lists found.')
        return open_tasks

    for tasklist in tasklists:
        tasks = service.tasks().list(tasklist=tasklist['id']).execute().get('items', [])
        for task in tasks:
            if task['status'] != 'completed':
                open_tasks.append(task)  # Add task to the list
                if 'id' in task:
                    mark_task_as_completed(service, tasklist['id'], task['id'])
    return open_tasks


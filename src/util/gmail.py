"""
Modified and cleaned up from

https://github.com/x4nth055/pythoncode-tutorials/tree/master/general/gmail-api

Thanks!
"""
import os
import pickle
import typing as T

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API utils
from googleapiclient.discovery import build

from util import log

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ["https://mail.google.com/"]


def gmail_authenticate(email: str, credentials_path: str) -> build:
    creds = None
    cookie_path = f"token_{email}.pickle"
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(cookie_path):
        with open(cookie_path, "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(cookie_path, "wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)


def search_messages(service: build, query: str) -> T.List[T.Any]:
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if "messages" in result:
        messages.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        result = (
            service.users().messages().list(userId="me", q=query, pageToken=page_token).execute()
        )
        if "messages" in result:
            messages.extend(result["messages"])
    return messages


def delete_messages(service: build, query: str) -> T.Any:
    messages_to_delete = search_messages(service, query)
    log.print_bold(f"Deleting {len(messages_to_delete)} emails.")
    # it's possible to delete a single message with the delete API, like this:
    # service.users().messages().delete(userId='me', id=msg['id'])
    # but it's also possible to delete all the selected messages with one query, batchDelete
    return (
        service.users()
        .messages()
        .batchDelete(userId="me", body={"ids": [msg["id"] for msg in messages_to_delete]})
        .execute()
    )


def mark_as_read(service: build, query: str) -> T.Any:
    messages_to_mark = search_messages(service, query)
    log.print_normal(f"Matched emails: {len(messages_to_mark)}")
    return (
        service.users()
        .messages()
        .batchModify(
            userId="me",
            body={"ids": [msg["id"] for msg in messages_to_mark], "removeLabelIds": ["UNREAD"]},
        )
        .execute()
    )


def mark_as_unread(service: build, query: str) -> T.Any:
    messages_to_mark = search_messages(service, query)
    log.print_normal(f"Matched emails: {len(messages_to_mark)}")
    return (
        service.users()
        .messages()
        .batchModify(
            userId="me",
            body={"ids": [msg["id"] for msg in messages_to_mark], "addLabelIds": ["UNREAD"]},
        )
        .execute()
    )

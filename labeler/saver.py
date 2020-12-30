import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

def init():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    CREDENTIAL_FILE = 'credentials.json'
    TOKEN_FILE = 'token.pickle'
    credentials = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_FILE, SCOPES)
            credentials = flow.run_local_server(port=10800)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    service = build('sheets', 'v4', credentials=credentials)

    return service.spreadsheets()

sheet = init()

def save(p_id, label):
    result = sheet.values().get(spreadsheetId="", range="position!A2:B").execute()
    rows = result.get('values', [])
    last_user = int(rows[len(rows)-1][0])
    
    row = [p_id, label]

    sheet.values().append(spreadsheetId='', valueInputOption="RAW", range="position", body={'values': [row]}).execute()

def saveSeveral(l):
    sheet.values().append(spreadsheetId='', valueInputOption="RAW", range="position", body={'values': l}).execute()

def getLast():
    result = sheet.values().get(spreadsheetId="", range="position!A2:B").execute()
    rows = result.get('values', [])
    return int(rows[len(rows)-1][0])


def classReport():
    subs = sheet.values().get(spreadsheetId="", range="position!A2:B").execute()
    rows = subs.get('values', [])

    red = 0
    pld = 0
    qtr = 0
    ukn = 0
    wrg = 0
    done = len(rows)

    for i in rows:
        if i[1] == "-":
            wrg = wrg + 1
        elif i[1] == "внутрикварт":
            qtr = qtr + 1
        elif i[1] == "плвд":
            pld = pld + 1
        elif i[1] == "красная":
            red = red + 1
        elif i[1] == "непонятно":
            ukn = ukn + 1
    
    return {"wrong": wrg, "unknown": ukn, "quater": qtr, "secondary": pld, "red": red, "done": done}

def findNotUsed():
    subs = sheet.values().get(spreadsheetId="", range="position!A2:B").execute()
    rows = subs.get('values', [])
    whole = [i for i in range(5000)]
    exist = [int(i[0]) for i in rows]
    print(list(set(whole) - set(exist)))
    return list(set(whole) - set(exist))[0]

def findAll(pic_id, label):
    d = pd.read_csv("final2.csv")
    rec = d.iloc[[pic_id]]
    records = d.loc[(d['Address_left'] == rec['Address_left'].values[0]) & (d["Долгота"] == rec["Долгота"].values[0]) & (d["Широта"] == rec["Широта"].values[0])]

    final = []
    for i in list(records["Unnamed: 0"]):
        if int(i) >= int(pic_id):
            final.append([i, label])

    saveSeveral(final)

    return findNotUsed()
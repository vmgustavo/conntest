import speedtest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# import pandas as pd
# import gspread_dataframe as gd

def main():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()

    # ['timestamp', 'download', 'upload', 'ping', 'latency', 'sponsor', 'id', 'host']
    data = [s.results.timestamp, s.results.download, s.results.upload,
            s.results.ping, s.results.server['latency'], s.results.server['sponsor'],
            s.results.server['id'], s.results.server['host']]

    # # Connecting with `gspread` here
    #
    # ws = gc.open("SheetName").worksheet("xyz")
    # existing = gd.get_as_dataframe(ws)
    # updated = existing.append(your_new_data)
    # gd.set_with_dataframe(ws, updated)

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('conntest-cred.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('conntest_results').sheet1
    sheet.append_row(values=data)


if __name__ == "__main__":
    main()

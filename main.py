import speedtest
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import re
from datetime import datetime
import pytz

MEGA_BYTES = pow(2, 20)
MEGA_BITS = pow(10, 6)


def main():
    timestamp = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%dT%H:%M:%S%Z')
    print('SERVICE START AT ' + timestamp)
    file_path = re.match(r'(/.+/)', os.path.abspath(__file__)).group(0)

    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()

    # ['timestamp', 'download', 'upload', 'ping', 'latency', 'sponsor', 'id', 'host']
    data = [timestamp,
            (s.results.download/MEGA_BITS), (s.results.upload/MEGA_BITS),
            (s.results.bytes_sent/MEGA_BYTES), (s.results.bytes_received/MEGA_BYTES),
            s.results.ping,
            s.results.server['sponsor'], s.results.server['name'],
            s.results.server['country'], s.results.server['id']]

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name((file_path + 'conntest-cred.json'), scope)
    client = gspread.authorize(creds)

    sheet = client.open('conntest_results').sheet1
    sheet.append_row(values=data)


if __name__ == "__main__":
    main()

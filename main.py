import logging
from datetime import datetime

import pytz
import gspread
import speedtest
from oauth2client.service_account import ServiceAccountCredentials

import LoggerClass

LoggerClass.Logger()
logger = logging.getLogger(__name__)
logger.info(f'_____ START EXECUTION {__file__}')

MEGA_BYTES = 2 ** 20
MEGA_BITS = 10 ** 6


def main():
    # SPEEDTEST PART
    timestamp = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).isoformat()
    logger.info('SERVICE START AT ' + timestamp)

    s = speedtest.Speedtest(
        config={
            # TODO: Customize to transfer less data
            'sizes': {
                'upload': [524_288, 1_048_576, 3_145_728],
                'download': [350, 500, 750, 1_000, 1_500, 2_000, 2_500, 3_000, 3_500, 4_000]
            },
            'counts': {'upload': 17, 'download': 4},
            'threads': {'upload': 2, 'download': 8},
            'length': {'upload': 10, 'download': 10},
            'upload_max': 51
        }
    )

    st = datetime.now()
    s.get_best_server()
    s.download()
    s.upload()

    exec_time = (datetime.now() - st).seconds

    res = s.results.dict()

    data = {
        'exec_time': exec_time,
        'date': timestamp,
        'ping': res['ping'],
        'download': res['download'] / MEGA_BITS,
        'bytes_received': res['bytes_received'] / MEGA_BYTES,
        'upload': res['upload'] / MEGA_BITS,
        'bytes_sent': res['bytes_sent'] / MEGA_BYTES,
        'server_loc': ' '.join([res['server']['name'], res['server']['cc']]),
        'server_host': res['server']['host'],
        'server_latency': res['server']['latency'],
        'client_ip': res['client']['ip']
    }

    logger.info(' | '.join([
        f'DOWN: {data["download"]:.02f}',
        f'UP: {data["upload"]:.02f}',
        f'PING: {data["ping"]:.02f}'
    ]))

    # GOOGLE DRIVE API PART
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('conntest-cred.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('conntest_results').sheet1
    sheet.append_row(values=list(data.values()))


if __name__ == "__main__":
    main()

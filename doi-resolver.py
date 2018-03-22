# coding: utf-8
import argparse
import datetime
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import requests
from requests_futures.sessions import FuturesSession
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Mass Construct URLs from DOIs and Resolve')
    parser.add_argument('input', help='Input CSV file')
    parser.add_argument('-w', '--workers', default=100, type=int,
                        help='Number of concurrent workers')
    parser.add_argument('-b', '--batchsize', default=100, type=int,
                        help='Batchsize (max memory consumption)')
    parser.add_argument('-t', '--timeout', default=5, type=int,
                        help='Timeout for requests')
    parser.add_argument('-c', '--column', default="doi",
                        help='Define target column')
    parser.add_argument('-f', '--format', default='https://doi.org/{}',
                        help='Format string for URL construction with ID.\
                              Example: \'https://doi.org/{}\'')
    parser.add_argument('-U', '--url', dest='url', action='store_true',
                        help='Disables URL construction')

    args = vars(parser.parse_args())

    # Options
    batchsize = args['batchsize']
    max_workers = args['workers']
    timeout = args['timeout']
    col = args['column']

    # Read input file
    df = pd.read_csv(args['input'])
    targets = df[col].tolist()

    resolved = pd.DataFrame({col: targets,
                             'resolved': None,
                             'ts': None,
                             'err': None,
                             'err_msg': None,
                             'status_code': None})
    resolved = resolved.set_index(col)

    # Split dois into batches
    batches = range(0, len(targets), batchsize)

    # FutureSession
    session = FuturesSession(max_workers=max_workers)
    for i in tqdm(batches, total=len(batches)):
        futures = []
        batch = targets[i:i + batchsize]

        # create futures in parallel
        for target in batch:
            now = datetime.datetime.now()
            if not args['url']:
                url = args['format'].format(target)
            else:
                url = target

            future = session.get(url, allow_redirects=True, timeout=timeout)

            futures.append({
                "target": target,
                "ts": str(now),
                "future": future
            })

        # collect future respones and populate df
        for response in futures:
            err = None
            err_msg = None
            status = None

            ix = response['target']

            try:
                resolved.loc[ix, 'resolved'] = response['future'].result().url
                resolved.loc[ix, 'status_code'] = response['future'].result().status_code
            except requests.exceptions.Timeout as ex:
                err_msg = str(ex)
                err = "Timeout"
            except requests.exceptions.TooManyRedirects as ex:
                err_msg = str(ex)
                err = "TooManyRedirects"
            except requests.exceptions.RequestException as ex:
                err_msg = str(ex)
                err = "RequestException"

            resolved.loc[ix, 'err'] = err
            resolved.loc[ix, 'err_msg'] = err_msg
            resolved.loc[ix, 'ts'] = response['ts']

    resolved.to_csv(args['input'].split(".csv")[0] + "_resolved.csv")

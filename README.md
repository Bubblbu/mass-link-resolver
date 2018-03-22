# Mass Link Resolver

Resolve DOIs (and other links) in parallel with nice update bars

- *Input*

    A list of IDs (e.g., DOI) or URLs

- *Output*

    Resolved URLs, resolve errors, response codes, timestamps

## Features

- Resolves a column of DOIs in parallel and creates an output file with metadata
- Define your own URL format if you're working with other IDs
- Resolve a column of URLs if you're not using IDs
- Uses [tqdm](https://github.com/noamraph/tqdm) to display a fancy progress bar & ETA

## Usage

```sh
usage: doi-resolver.py [-h] [-w WORKERS] [-b BATCHSIZE] [-t TIMEOUT]
                       [-c COLUMN] [-f FORMAT] [-U]
                       input

Mass Construct URLs from DOIs and Resolve

positional arguments:
  input                 Input CSV file

optional arguments:
  -h, --help            show this help message and exit
  -w WORKERS, --workers WORKERS
                        Number of concurrent workers
  -b BATCHSIZE, --batchsize BATCHSIZE
                        Batchsize (max memory consumption)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for requests
  -c COLUMN, --column COLUMN
                        Define target column
  -f FORMAT, --format FORMAT
                        Format string for URL construction with ID. Example:
                        'https://doi.org/{}'
  -U, --url             Disables URL construction
```

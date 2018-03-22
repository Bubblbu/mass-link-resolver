# Mass Link Resolver

Resolve DOIs (and other links) in parallel with a nice progress bar.

## Features

- Resolve a list of DOIs in parallel and create an output file with metadata
- Resolve a list of URLs if, e.g., resolve a list of shortened URLs
- Define your own URL format if you're not resolving DOIs
- Uses [tqdm](https://github.com/noamraph/tqdm) to display a fancy progress bar & ETA

## To-Do

- [ ] Properly set headers
- [ ] Add option to switch between HEAD and GET requests (HEAD as default)
- [ ] Add option to avoid hammering

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

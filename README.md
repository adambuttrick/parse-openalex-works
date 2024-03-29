## Overview

Processes a list of gzipped OpenAlex works data files and extracts the work and affiliation metadata.

## Data Fields

The following fields are extracted from each JSON entry and included in the CSV files:

- **DOI**: DOI for the work.
- **OpenAlex Work ID**: OpenAlex work ID.
- **Raw Affiliation String**: Affiliation string text.
- **Institution ID**: OpenAlex institution ID associated with the affiliation string.
- **ROR ID**: ROR ID for the associated with the affiliation string.

## Usage

```
python process_json_to_csv.py -i <path_to_input_file>
```

- **-i, --input**: Path to the input file containing the list of gzipped JSON files. (Required)

The script will automatically read each line of the input file as a path to a gzipped JSON file, parse the contents, and output CSV files in a directory named `csvs`. Each CSV file will be named after the corresponding ROR ID or OpenAlex institution ID, and will contain the data fields listed above.

### Error Logging

Errors encountered during the processing of each file are logged to `parsing_errors.csv`, with details about the file, the line number where the error occurred, the content of the line, and the error message.

### Example

```
python parse_works.py -i list_of_files.txt
```

In this example, `list_of_files.txt` should contain the file paths of the gzipped JSON files to be processed, one per line.

import argparse
import re
import ast
import gzip
import csv


def parse_arguments():
	parser = argparse.ArgumentParser(
		description="Process input file containing paths to gzipped JSON files.")
	parser.add_argument('-i', '--input', required=True,
						help="Path to the input file containing list of gzipped JSON files.")
	return parser.parse_args()


def log_error(file_name, line_num, line_content, error_message):
	with open('parsing_errors.csv', 'a') as f_out:
		writer = csv.writer(f_out)
		writer.writerow(
			[file_name, line_num, repr(line_content), error_message])


def write_to_csv(data, outfile):
	with open(outfile, 'a') as f_out:
		writer = csv.writer(f_out)
		writer.writerow(data)


def process_work_data(work, file_name, line_num, error_log):
	doi = work.get('ids', {}).get('doi', '')
	openalex_work_id = work.get('ids', {}).get('openalex', '')
	if 'authorships' in work:
		for author in work['authorships']:
			raw_affiliation = author.get('raw_affiliation_string', '')
			for institution in author.get('institutions', []):
				if 'ror' in institution:
					ror_id = institution['ror']
					outfile = f'csvs/{ror_id.replace("https://ror.org/", "")}.csv'
					csv_data = [doi, openalex_work_id, raw_affiliation,
								institution.get('id', ''), ror_id]
				elif 'id' in institution:
					institution_id = institution['id']
					outfile = f'csvs/{institution_id.replace("https://openalex.org/", "")}.csv'
					csv_data = [doi, openalex_work_id,
								raw_affiliation, institution_id]
				else:
					continue
				write_to_csv(csv_data, outfile)


def process_json_line(json_line, line_num, file_name, error_log):
	subs = {'null': 'None', 'true': 'True', 'false': 'False'}
	for k, v in subs.items():
		json_line = re.sub(k, v, json_line)
	work = ast.literal_eval(json_line) if json_line else None
	if work:
		process_work_data(work, file_name, line_num, error_log)


def process_file(input_file):
	error_log = 'parsing_errors.csv'
	with open(input_file) as f_in:
		all_files = [line.strip() for line in f_in]
	len_all_files = len(all_files)
	for i, file in enumerate(all_files):
		print(f'Parsing {i+1} of {len_all_files} - {file}')
		with gzip.open(file, 'rt', encoding='utf-8') as f_in:
			for line_num, line in enumerate(f_in):
				process_json_line(line, line_num, file, error_log)


if __name__ == '__main__':
	args = parse_arguments()
	process_file(args.input)

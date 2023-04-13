import re
import ast
import sys
import csv
import glob
import gzip
import json

def get_works_data(f):
	error_log = 'parsing_errors.csv'
	with open(f) as f_in:
		all_files = [line.strip() for line in f_in]
	len_all_files = str(len(all_files))
	for i, file in enumerate(all_files):
		print('Parsing', str(i), 'of', len_all_files, '-', file)
		with gzip.open(file, 'r+') as f_in:       
			for i, line in enumerate(f_in):
				try:                   
					str_data = line.decode('utf-8')
					subs = {'null':'None', 'true':'True', 'false':'False'}
					for k,v in subs.items(): str_data = re.sub(k,v, str_data)
					work = ast.literal_eval(str_data) if str_data != '' else None
					if work is not None:
						if 'ids' in work.keys() and 'ids' != [] and 'ids' != None:
							work_ids = work['ids']
							doi = work_ids['doi'] if 'doi' in work_ids.keys() else ''
							openalex_work_id = work_ids['openalex'] if 'openalex' in work_ids.keys() else ''
							if 'authorships' in work.keys() and work['authorships'] != []:
								authorships = work['authorships']
								for author in authorships:
									if 'raw_affiliation_string' in author.keys() and author['raw_affiliation_string'] != None:
										if 'institutions' in author.keys() and author['institutions'] != [] and author['institutions'] != None:
											for institution in author['institutions']:
												raw_affiliation = author['raw_affiliation_string']
												if 'ror' in institution.keys() and institution['ror'] != None:
													institution_id = institution['id']
													ror_id = institution['ror']
													outfile = 'csvs/' + re.sub('https://ror.org/', '', ror_id) + '.csv'
													with open(outfile, 'a') as f_out:
														writer = csv.writer(f_out)
														writer.writerow([doi, openalex_work_id, raw_affiliation, institution_id, ror_id])
												elif 'id' in institution.keys() and institution['id'] != None:
													institution_id = institution['id']
													outfile = 'csvs/' + re.sub('https://openalex.org/', '', institution_id) + '.csv'
													with open(outfile, 'a') as f_out:
														writer = csv.writer(f_out)
														writer.writerow([doi, openalex_work_id, raw_affiliation, institution_id])
				except Exception as e:
					with open(error_log, 'a') as f_out:
						writer = csv.writer(f_out)
						writer.writerow([file, i, line, str(e)])



if __name__ == '__main__':
	get_works_data(sys.argv[1])

import os
join = os.path.join


base_dir = '/gws/smf/j04/cp4cds1/c3s_34e/'

print('cmip5')
# how many failures, and what types of failure
# failure_dir = join(base_dir, 'logs/failure/c3s-cmip5')
write_error_dir = join(base_dir, 'logs/failure/write_error/c3s-cmip5')
no_files_dir = join(base_dir, 'logs/failure/no_files/c3s-cmip5')
extract_error_dir = join(base_dir, 'logs/failure/extract_error/c3s-cmip5')

# failures = sum(len(files) for _, _, files in os.walk(failure_dir))
write_errors = sum(len(files) for _, _, files in os.walk(write_error_dir))
no_file_errors = sum(len(files) for _, _, files in os.walk(no_files_dir))
extract_errors = sum(len(files) for _, _, files in os.walk(extract_error_dir))

print('total failures =', write_errors+no_file_errors+extract_errors)
print('write error failures =', write_errors)
print('no files error failures =', no_file_errors)
print('extract error failures =', extract_errors)


# how many succeeded
output_dir = join(base_dir, 'register/c3s-cmip5')
json_files = sum(len(files) for _, _, files in os.walk(output_dir))

print('total json files =', json_files)
print('Number of datasets successfully scanned =', (json_files-write_errors))


# how many datasets were attempted
print('Number of datasets attempted =', (json_files+no_file_errors+extract_errors))


# total volume of JSON files
json_count = 0
for root, dirs, files in os.walk(output_dir):
    for name in files:
        file_path = os.path.abspath(os.path.join(root, name))
        size = os.path.getsize(file_path)
        json_count += size

print('Total volume of JSON files (including those with write errors) =', json_count/1000, 'KB')

# average volume of a JSON file for this project
print('Average volume of a JSON file (including those with write errors) =', round((json_count/json_files)/1000, 2), 'KB')



#cordex

print('cordex')
# how many failures, and what types of failure
# failure_dir = join(base_dir, 'logs/failure/c3s-cmip5')
write_error_dir_cordex = join(base_dir, 'logs/failure/write_error/c3s-cordex')
no_files_dir_cordex = join(base_dir, 'logs/failure/no_files/c3s-cordex')
extract_error_dir_cordex = join(base_dir, 'logs/failure/extract_error/c3s-cordex')

# failures = sum(len(files) for _, _, files in os.walk(failure_dir))
write_errors_cordex = sum(len(files) for _, _, files in os.walk(write_error_dir_cordex))
no_file_errors_cordex = sum(len(files) for _, _, files in os.walk(no_files_dir_cordex))
extract_errors_cordex = sum(len(files) for _, _, files in os.walk(extract_error_dir_cordex))

print('total failures =', write_errors_cordex+no_file_errors_cordex+extract_errors_cordex)
print('write error failures =', write_errors_cordex)
print('no files error failures =', no_file_errors_cordex)
print('extract error failures =', extract_errors_cordex)


# how many succeeded
output_dir_cordex = join(base_dir, 'register/c3s-cordex')
json_files_cordex = sum(len(files) for _, _, files in os.walk(output_dir_cordex))

print('total json files =', json_files_cordex)
print('Number of datasets successfully scanned =', (json_files_cordex-write_errors_cordex))


# how many datasets were attempted
print('Number of datasets attempted =', (json_files_cordex+no_file_errors_cordex+extract_errors_cordex))


# total volume of JSON files
json = 0
for root, dirs, files in os.walk(output_dir_cordex):
    for name in files:
        file_path = os.path.abspath(os.path.join(root, name))
        size = os.path.getsize(file_path)
        json += size

print('Total volume of JSON files (including those with write errors) =', json/1000, 'KB')

# average volume of a JSON file for this project
print('Average volume of a JSON file (including those with write errors) =', round((json/json_files_cordex)/1000, 2), 'KB')
import os
join = os.path.join


base_dir = '/gws/smf/j04/cmip6_prep/c3s_34e/'


# how many failures, and what types of failure
failure_dir = join(base_dir, 'logs/failure/')
write_error_dir = join(base_dir, 'logs/failure/write_error/')
no_files_dir = join(base_dir, 'logs/failure/no_files/')
extract_error_dir = join(base_dir, 'logs/failure/extract_error')

failures = sum(len(files) for _, _, files in os.walk(failure_dir))
write_errors = sum(len(files) for _, _, files in os.walk(write_error_dir))
no_file_errors = sum(len(files) for _, _, files in os.walk(no_files_dir))
extract_errors = sum(len(files) for _, _, files in os.walk(extract_error_dir))

print('total failures =', failures)
print('write error failures =', write_errors)
print('no files error failures =', no_file_errors)
print('extract error failures =', extract_errors)


# how many succeeded
output_dir = join(base_dir, 'register/')
json_files = sum(len(files) for _, _, files in os.walk(output_dir))

print('total json files =', json_files)
print('Number of datasets succesfully scanned =', (json_files-write_errors))


# how many datasets were attempted
print('Number of datasets attempted =', (json_files+no_file_errors+extract_errors))


# total volume of JSON files
sum = 0
for root, dirs, files in os.walk(output_dir):
    for name in files:
        file_path = os.path.abspath(os.path.join(root, name))
        size = os.path.getsize(file_path)
        sum += size

print('Total volume of JSON files (including those with write errors) =', sum/1000, 'KB')

# average volume of a JSON file for this project
print('Average volume of a JSON file (including those with write errors) =', round((sum/json_files)/1000, 2), 'KB')


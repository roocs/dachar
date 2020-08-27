import os

join = os.path.join

QUEUE = "short-serial"
WALLCLOCK_LARGE = "23:59"
MEMORY_LARGE = 32000

WALLCLOCK_SMALL = "04:00"
MEMORY_SMALL = 4000

DIR_GROUPING_LEVEL = 4
CONCERN_THRESHOLD = 0.2

# _base_path = '/gws/smf/j04/cp4cds1/c3s_34e'
_base_path = "./outputs"

BASE_LOG_DIR = join(_base_path, "logs")
BATCH_OUTPUT_PATH = join(BASE_LOG_DIR, "batch-outputs/{grouped_ds_id}")
JSON_OUTPUT_PATH = join(_base_path, "register/{grouped_ds_id}.json")
SUCCESS_PATH = join(BASE_LOG_DIR, "success/{grouped_ds_id}.log")
NO_FILES_PATH = join(BASE_LOG_DIR, "failure/no_files/{grouped_ds_id}.log")
PRE_EXTRACT_ERROR_PATH = join(
    BASE_LOG_DIR, "failure/pre_extract_error/{grouped_ds_id}.log"
)
EXTRACT_ERROR_PATH = join(BASE_LOG_DIR, "failure/extract_error/{grouped_ds_id}.log")
WRITE_ERROR_PATH = join(BASE_LOG_DIR, "failure/write_error/{grouped_ds_id}.log")
FIX_PATH = join(_base_path, "fixes/{grouped_ds_id}.json")

ELASTIC_API_TOKEN = 'cdad90eaf6f889732fd691e38df2f6456e9f73029b3a49f0a871d5f64a553c44'
# ELASTIC_API_TOKEN = None

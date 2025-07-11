from pathlib import Path
from urllib.parse import urljoin


MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'
WHATS_NEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PRETTY_ARGUMENT_NAME = 'pretty'
FILE_ARGUMENT_NAME = 'file'
LOG_DIR_NAME = 'logs'
LOG_FILE_NAME = 'parser.log'
RESULTS_DIR_NAME = 'results'
DOWNLOADS_DIR_NAME = 'downloads'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

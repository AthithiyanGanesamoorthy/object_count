import os

from adapters.count_repo import CountMySQLRepo
from adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from domain.actions import CountDetectedObjects
import logging
handler = logging.FileHandler('logger_data.log', encoding='utf-8')

# configure the logger
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def dev_count_action() -> CountDetectedObjects:
    '''Returns a CountDetectedObjects instance with a FakeObjectDetector and CountMySQLRepo, using environment variables to set MySQL connection details.
    Modify the details as per your specific use case.'''
    mysql_host = os.environ.get(
        'MYSQL_HOST', 'localhost')  # change the details according the use
    mysql_port = os.environ.get('MYSQL_PORT', 3306)
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', 'password')
    mysql_db = os.environ.get('MYSQL_DB', 'DB')
    return CountDetectedObjects(FakeObjectDetector(),
                                CountMySQLRepo(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db))


def prod_count_action() -> CountDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', 3306)
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', 'password')
    mysql_db = os.environ.get('MYSQL_DB', 'DB')
    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                CountMySQLRepo(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db))


def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()

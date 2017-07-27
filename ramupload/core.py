import os
import os.path as osp
from glob import glob
import logging
from collections import defaultdict
import subprocess
import shlex

logger = logging.getLogger(__name__)


def _get_data_path(path=None):
    if path is None:
        output = subprocess.check_output(shlex.split('git worktree list'))
        root = output.split()[0]
        found_path = osp.join(root, 'data')
    else:
        found_path = osp.abspath(path)
    assert osp.exists(found_path)
    logger.debug("Data path: %s", found_path)
    return found_path


def _get_session_path(subject, experiment, session, path):
    return osp.join(path, experiment, subject, "session_{:d}".format(session))


def crawl_data_dir(path=None):
    """Crawl the data directory to find available data for uploading.

    :param str path: Path to look in.
    :returns: Dictionary of subjects. Keys are subjects, values are a list of
        experiments the subject has participated in.

    """
    path = _get_data_path(path)
    experiments = os.listdir(path)
    subjects = defaultdict(list)
    for exp in experiments:
        if exp.startswith('.'):
            continue
        for sdir in os.listdir(osp.join(path, exp)):
            subjects[sdir].append(exp)
            logger.info("Found experiment %s for subject %s", sdir, exp)
    return subjects


def get_sessions(subject, experiment, exclude_uploaded=True, path=None):
    """Get available sessions to upload.

    :param str subject:
    :param str experiment:
    :param bool exclude_uploaded: Exclude already uploaded data
        (not yet implemented).
    :param str path:

    """
    path = _get_data_path(path)
    sessions = []
    for session in range(20):
        subdir = _get_session_path(subject, experiment, session, path)
        pattern = osp.join(subdir, "*.*log")
        if len(glob(pattern)):
            sessions.append(session)
    return sessions

"""
libensemble helpers for launching subprocesses.
====================================================
"""

import os
import sys
import shlex
import signal
import time

from itertools import chain


# See: https://github.com/google/python-subprocess32
if os.name == 'posix' and sys.version_info[0] < 3:
    try:
        import subprocess32 as subprocess
        have_subprocess32 = True
    except ImportError:
        import subprocess
        have_subprocess32 = False
else:
    import subprocess
    have_subprocess32 = (sys.version_info[0] >= 3
                         and sys.version_info[1] >= 2)


def form_command(cmd_template, specs):
    "Fill command parts with dict entries from specs; drop any missing."
    specs = {k: v for k, v in specs.items() if v is not None}
    def fill(fmt):
        "Fill a template string and split with shlex; drop if missing specs"
        try:
            return shlex.split(fmt.format(**specs))
        except KeyError:
            return None
    return list(chain.from_iterable(filter(None, map(fill, cmd_template))))


def launch(cmd_template, specs=None, **kwargs):
    "Launch a new subprocess (with command templating and Python 3 help)."
    if not have_subprocess32 and kwargs.get('start_new_session'):
        del kwargs['start_new_session']
        kwargs['preexec_fn'] = os.setsid
    cmd = (form_command(cmd_template, specs) if specs is not None
           else cmd_template)
    return subprocess.Popen(cmd, **kwargs)


def killpg(process):
    "Kill the process (and group if it is group leader)."
    try:
        pid = process.pid
        pgid = os.getpgid(pid) if hasattr(os, 'killpg') else -1
        if pgid == pid:
            os.killpg(pgid, signal.SIGKILL)
        else:
            process.kill()
        return True
    except OSError:  # In Python 3: ProcessLookupError
        return False


def terminatepg(process):
    "Send termination signal to the process (and group if it is group leader)"
    try:
        pid = process.pid
        pgid = os.getpgid(pid) if hasattr(os, 'killpg') else -1
        if pgid == pid:
            # Claim in original controller was that we need a wait --
            # have not seen this anywhere else in my searching...
            time.sleep(0.1)
            os.killpg(pgid, signal.SIGTERM)
        elif hasattr(signal, 'CTRL_BREAK_EVENT'):
            # Supposedly does a group terminate for Windows...
            process.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            process.terminate()
        return True
    except OSError:  # In Python 3: ProcessLookupError
        return False


def process_is_stopped(process, timeout):
    "Wait for timeout to see if process is finished; True if done."
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(0.01)
        if process.poll() is not None:
            return True
    return process.poll() is not None


if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 3):

    # Python 3.3 added timeout arguments
    def wait(process, timeout=None):
        "Wait on a process with timeout."
        if timeout is None or process_is_stopped(process, timeout):
            return process.wait()
        return None

else:

    def wait(process, timeout=None):
        "Wait on a process with timeout (wait forever if None)."
        try:
            return process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            return None


def wait_and_kill(process, timeout):
    "Give a grace period for a process to terminate, then kill it."
    rc = wait(process, timeout)
    if rc is not None:
        return rc
    killpg(process)
    return process.wait()


def cancel(process, timeout=0):
    "Send a termination signal, give a grace period, then hard kill if needed."
    if timeout is not None and timeout > 0:
        terminatepg(process)
    return wait_and_kill(process, timeout)


# Note: cancel with timeout 0    -- just kill and then wait
#       cancel with timeout None -- just terminate and then wait
#       cancel with timeout > 0  -- try terminating, then hard kill if needed


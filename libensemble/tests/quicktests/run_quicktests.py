#!/usr/bin/env python3
"""Quick test suite for agent development checks.

Runs a curated subset of unit tests (via pytest) and functionality/regression
tests (as scripts) covering core libEnsemble paths including executor and APOSMM.

Requires the libe_agent conda environment. Expected runtime: ~60-90s.

Usage:
    conda run -n libe_agent python libensemble/tests/quicktests/run_quicktests.py
"""

import subprocess
import sys
import time
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = TESTS_DIR.parents[1]

CONDA_ENV = "libe_agent"

# --- Unit tests (pytest) ---------------------------------------------------

# Files to ignore entirely (collection errors or need special setup)
UNIT_TEST_IGNORES = [
    "test_ufunc_runners.py",
    "test_executor_gpus.py",
    "test_launcher.py",
]

# Individual tests to deselect
UNIT_TEST_DESELECT = [
    "libensemble/tests/unit_tests/test_ensemble.py::test_ensemble_prevent_comms_overwrite",
    "libensemble/tests/unit_tests/test_models.py::test_libe_specs",
]

# --- Script-based tests (functionality + regression) ------------------------
# Each entry: (subdir, filename, extra_args)
SCRIPT_TESTS = [
    # Core sampling
    ("functionality_tests", "test_1d_super_simple.py", ["--nworkers", "2", "--comms", "local"]),
    ("functionality_tests", "test_uniform_sampling.py", ["--nworkers", "2", "--comms", "local"]),
    ("functionality_tests", "test_persistent_uniform_sampling.py", ["--nworkers", "2", "--comms", "local"]),
    # Error handling
    ("functionality_tests", "test_worker_exceptions.py", ["--nworkers", "2", "--comms", "local"]),
    ("functionality_tests", "test_calc_exception.py", ["--nworkers", "2", "--comms", "local"]),
    ("functionality_tests", "test_elapsed_time_abort.py", ["--nworkers", "2", "--comms", "local"]),
    # Executor
    ("functionality_tests", "test_executor_hworld_pass_fail.py", ["--nworkers", "2", "--comms", "local"]),
    ("functionality_tests", "test_executor_simple.py", ["--nworkers", "2", "--comms", "local"]),
    # Regression - sampling
    ("regression_tests", "test_1d_sampling.py", ["--nworkers", "2", "--comms", "local"]),
    ("regression_tests", "test_2d_sampling.py", ["--nworkers", "2", "--comms", "local"]),
    # Regression - APOSMM
    ("regression_tests", "test_persistent_aposmm_nlopt.py", ["--nworkers", "3", "--comms", "local"]),
    ("regression_tests", "test_asktell_aposmm_nlopt.py", ["--nworkers", "3", "--comms", "local"]),
]

SIMDIR = TESTS_DIR / "unit_tests" / "simdir"
BUILD_TARGETS = [
    ("mpicc", "my_simtask.c", "my_simtask.x", ["-lm"]),
    ("gcc", "my_serialtask.c", "my_serialtask.x", ["-lm"]),
    ("gcc", "c_startup.c", "c_startup.x", ["-lm"]),
]


def build_sim_codes():
    """Build C test executables if not already present."""
    for compiler, src, out, flags in BUILD_TARGETS:
        outpath = SIMDIR / out
        srcpath = SIMDIR / src
        if outpath.exists():
            continue
        print(f"Building {out}...")
        result = subprocess.run([compiler, "-o", str(outpath), str(srcpath)] + flags, cwd=str(SIMDIR))
        if result.returncode != 0:
            print(f"WARNING: Failed to build {out} with {compiler}")


def run_unit_tests():
    """Run pytest unit tests."""
    print("=" * 60)
    print("UNIT TESTS (pytest)")
    print("=" * 60)
    rc = 0

    # Main unit tests (run from unit_tests dir for executor simdir paths)
    test_dir = str(TESTS_DIR / "unit_tests")
    cmd = [sys.executable, "-m", "pytest", test_dir, "-v", "--tb=short", "-q"]
    for ignore in UNIT_TEST_IGNORES:
        cmd.extend(["--ignore", str(TESTS_DIR / "unit_tests" / ignore)])
    for deselect in UNIT_TEST_DESELECT:
        cmd.extend(["--deselect", deselect])
    result = subprocess.run(cmd, cwd=str(TESTS_DIR / "unit_tests"))
    if result.returncode != 0:
        rc = result.returncode

    # Non-MPI unit tests
    nompi_dir = str(TESTS_DIR / "unit_tests_nompi")
    cmd = [sys.executable, "-m", "pytest", nompi_dir, "-v", "--tb=short", "-q"]
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if result.returncode != 0:
        rc = result.returncode

    return rc


def run_script_tests():
    """Run script-based functionality and regression tests."""
    print("\n" + "=" * 60)
    print("SCRIPT TESTS (functionality + regression)")
    print("=" * 60)
    failures = []
    for subdir, filename, args in SCRIPT_TESTS:
        test_path = TESTS_DIR / subdir / filename
        label = f"{subdir}/{filename}"
        print(f"\n--- {label} ---")
        t0 = time.time()
        result = subprocess.run([sys.executable, str(test_path)] + args, cwd=str(test_path.parent))
        elapsed = time.time() - t0
        if result.returncode != 0:
            failures.append(label)
            print(f"FAILED ({elapsed:.1f}s)")
        else:
            print(f"PASSED ({elapsed:.1f}s)")
    return failures


def main():
    t0 = time.time()
    build_sim_codes()
    unit_rc = run_unit_tests()
    script_failures = run_script_tests()
    elapsed = time.time() - t0

    print("\n" + "=" * 60)
    print(f"QUICK TESTS COMPLETE in {elapsed:.1f}s")
    print("=" * 60)

    if unit_rc != 0:
        print("Unit tests: SOME FAILURES")
    else:
        print("Unit tests: ALL PASSED")

    if script_failures:
        print(f"Script tests: {len(script_failures)} FAILED:")
        for f in script_failures:
            print(f"  - {f}")
    else:
        print("Script tests: ALL PASSED")

    if unit_rc != 0 or script_failures:
        sys.exit(1)


if __name__ == "__main__":
    main()

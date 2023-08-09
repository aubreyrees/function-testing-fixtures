#!/usr/bin/env bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd );
source "$SCRIPT_DIR/common.sh";


cd "$SCRIPT_DIR"
$SCRIPT_DIR/safe_bin.sh python -m code_gen > ../tests/function_fixtures.py

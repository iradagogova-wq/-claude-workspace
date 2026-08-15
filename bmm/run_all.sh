#!/bin/bash
set -e
cd /home/user/-claude-workspace
uv venv .bmm_venv >/dev/null 2>&1
uv pip install --python .bmm_venv/bin/python numpy pillow >/dev/null 2>&1
.bmm_venv/bin/python bmm/build.py
.bmm_venv/bin/python bmm/make_page.py
echo CHAIN_DONE

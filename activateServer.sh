#!/bin/bash

cd "/Users/hacker/iOrchid Horticulture Management/public" || exit 1

# Activate virtual environment (relative to `public` -> go up one level)
source "../venv/bin/activate"

python webServer2026.py
```

#!/usr/bin/env fish

# Prefer using the venv's pip/python directly to avoid relying on the activate script
if test -x .venv/bin/python
	set VENV_PY .venv/bin/python
	set VENV_PIP .venv/bin/pip
else
	echo "Error: .venv/bin/python not found or not executable. Create the venv with: python3 -m venv .venv" >&2
	exit 1
end

# Upgrade required packages (optional). Comment out if you don't want automatic upgrades.
$VENV_PIP install --upgrade discord openai yt_dlp ffmpeg matplotlib gtts pynacl

# Start the main script using the venv's Python
$VENV_PY NeuroChat.py

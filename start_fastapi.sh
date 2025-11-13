#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(realpath "./src")
export FIM_PROVIDER="${FIM_PROVIDER:-OPENAI}"
PORT="${PORT:-29950}"
uvicorn main:app --host 0.0.0.0 --port "$PORT"


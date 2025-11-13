#!/bin/bash

curl -X POST http://127.0.0.1:29950/infill \
-H "Content-Type: application/json" \
-d '{
  "input_prefix": "Hello ",
  "input_suffix": "!",
  "input_extra": [{"text": ""}],
  "prompt": "w"
}'

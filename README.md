# llama-vim-adapter

This project allows you to use [Mistral's Codestral FIM](https://docs.mistral.ai/models/codestral-25-08) endpoint with the [ggml-org/llama.vim](https://github.com/ggml-org/llama.vim) plugin.  

## Why
The llama.vim plugin is one of the only (and good) working solutions for ghost text completion in Vim 9.  
But it only works with local models. This project aims to allows you to query third party services by starting a small Python server that translates the requests from the Vim plugin to third party's API.

## Compatible third parties

As of now the compatibility is limited to: 
- MistralAI's `codestral-latest` FIM model.

## Configuration

### Required environment variables

You may configure the server with the following environment variables:

| Variable        | Required | Default  | Purpose |
| --------------- | -------- | -------- | ------- |
| `MISTRAL_API_KEY` | ✅       | —        | Secret used to authenticate against Mistral's API. |
| `PORT`          | Optional | `29950`  | Listening port for the server. |
| `HOST_PORT`     | Optional | `29950`  | Host-side port if you use the `docker compose` file. |

### `llama.vim` configuration

Once the server is running, drop the following config into your `vimrc` (or adapt it for Neovim):

```vim
let g:llama_config = {}
let g:llama_config.auto_fim = v:true
let g:llama_config.endpoint = 'http://127.0.0.1:29950/infill'
let g:llama_config.keymap_trigger = "<C-n>"
let g:llama_config.keymap_accept_full = "<Tab>"
let g:llama_config.keymap_accept_line = "<S-Tab>"
let g:llama_config.keymap_accept_word = ""
let g:llama_config.max_line_suffix = 50
let g:llama_config.model = ''
let g:llama_config.n_predict = 258
let g:llama_config.n_prefix = 128
let g:llama_config.n_suffix = 32
let g:llama_config.ring_chunk_size = 64
let g:llama_config.ring_n_chunks = 16
let g:llama_config.ring_scope = 1024
let g:llama_config.ring_update_ms = 3000
let g:llama_config.show_info = v:false
let g:llama_config.stop_strings = []
let g:llama_config.t_max_predict_ms = 3000
let g:llama_config.t_max_prompt_ms = 3000
```

## Installation and usage

### Docker compose

A convenient way to start the server is to use the provided `docker compose` file:

```
MISTRAL_API_KEY=sk-... HOST_PORT=29950 docker compose up --build
```

## Local usage

You may also start the server locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
export MISTRAL_API_KEY="sk-your-mistral-key"
./start_fastapi.sh 
```

## Calling uvicorn directly

You can also launch directly with uvicorn :

```bash
PORT=29950 \
  FIM_PROVIDER=MISTRAL \
  MISTRAL_API_KEY=sk-... \
  PYTHONPATH=$PYTHONPATH:$(realpath "./src") \
  python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Troubleshooting

- Ensure outbound HTTPS access to `api.mistral.ai` and confirm the `MISTRAL_API_KEY` is valid.
- The server logs every completion via the `uvicorn.error` logger; start it with `LOG_LEVEL=debug` if you need the raw prompts/suffixes (see `Context.get_logger`).
- If llama.vim sends empty strings, check that `auto_fim` is enabled and the endpoint matches the host/port you exposed.


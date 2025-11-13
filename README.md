# llama-vim-openai-adapter

This service exposes a fill-in-the-middle endpoint that delegates to a configurable completion provider. By default it uses the OpenAI chat completions API but you can switch to Mistral's FIM endpoint without touching the code.

## Configuration

The adapter reads the following environment variables:

| Variable          | Description                                                                  | Default  |
| ---              | ---                                                                          | --       |
| `FIM_PROVIDER`    | Select the completion provider: `OPENAI` or `MISTRAL`. Defaults to `OPENAI`. | `OPENAI` |
| `OPENAI_API_KEY`  | API key used when `FIM_PROVIDER` is `OPENAI`                                 |          |
| `MISTRAL_API_KEY` | API key used for `codestral` FIM models                                      |          |

## Mistral Adapter

When `FIM_PROVIDER=MISTRAL` the context factory will instantiate `MistralFimWrapper`, which calls Mistral's `/v1/fim/completions` endpoint and unwraps the first choice's assistant message. It mirrors the existing OpenAI wrapper interface so the rest of the service keeps reusing the same `InfillService` logic.

Make sure the service has access to a valid API key and network egress to `https://api.mistral.ai` before enabling the adapter.

## Docker

The provided `Dockerfile` installs the project and runs `start_fastapi.sh`. To run it with the local source mounted (so changes are picked up without rebuilding) and expose the service port, build and run with:

```bash
docker build -t llama-adapter .
docker run --rm -v "$(pwd)":/app -p 29950:29950 llama-adapter
```

Adjust `--env-file` or individual `-e` flags to inject the required credentials such as `OPENAI_API_KEY` or `MISTRAL_API_KEY` as needed.

The compose file maps host port 29960 to container port 29950 by default. If that binding conflicts with another process, override `HOST_PORT`—for example, `HOST_PORT=29970 docker compose up -d` still uses port 29950 inside the container while exposing 29970 on the host. The startup script also respects the `PORT` variable so you can change the listened port inside the container if needed.

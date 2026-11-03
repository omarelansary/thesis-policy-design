# LLM API State Overview

This repository hosts a small nginx-based docker container that serves a overview page of all LLM components and their state.

A one-shot Python program (`api_health`) probes every model the LiteLLM proxy advertises,
writes `/usr/share/nginx/html/state.json`, and exits; `crond` runs it every five minutes and
nginx serves the static page that polls that file.

## Installation

Assuming you have `make` and `docker` installed, run:

```bash
make
```

## Usage

Assuming you have your API key in `$HOME/.scadsai-api-key`, run the container using the following commands:

```bash
export THE_API_KEY=$(cat $HOME/.scadsai-api-key)
make run
```

Then, open <http://localhost> in your browser.

To point the same image at a LiteLLM proxy running on your own machine, use `make run-local`
instead — no source edits are needed.

## Configuration

The container reads three optional environment variables. busybox `crond` hands its own
environment to the jobs it forks, so these already reach the five-minute check; `entrypoint.sh`
also writes them to `/app/cron.env`, which the cron line sources, so the configuration does not
depend on that behaviour.

| Variable | Default | Meaning |
| --- | --- | --- |
| `THE_API_KEY` | *(required)* | Bearer token for the proxy |
| `API_HEALTH_URL` | `https://llm.scads.ai` | Proxy base URL; `/model/info` and `/v1/...` hang off it |
| `API_HEALTH_TIMEOUT` | `180` | Per-probe time budget in seconds |
| `API_HEALTH_CONCURRENCY` | `0` | Maximum simultaneous probes; `0` means unbounded |

`THE_API_KEY` is read from the environment, falling back to `/app/api-token` — the file
`entrypoint.sh` writes, mode 0600, for the benefit of any cron that builds a minimal
environment.

File locations are deliberately *not* configurable through the environment, so a stray variable
cannot redirect where the state document is published. `--state-path` and `--audio-file`
override them for local runs.

## Development

```bash
make check      # ruff lint + format check, mypy --strict, pytest
make test
make dev-run    # run against a proxy on localhost:4000, writing ./state.json
```

## Support

If you have the feeling that the scripts contain errors or otherwise need improvement, please [check whether there is an open issue already](https://gitlab.hrz.tu-chemnitz.de/scads-ai-llm/scads-ai-llm-components/api-state-overview/-/issues). If there is no issue yet, create one.

## Roadmap
When LLM services are updated and improved, we also update this project.

## Contributing
We are very thankful for improvements you provide! We are a very small team.

## License

Please see the [LICENSE](LICENSE).

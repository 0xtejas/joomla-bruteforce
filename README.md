# joomla-bruteforce

Joomla administrator login brute-force helper.

Tested on Joomla! 3.8.8.


## Setup (uv)

```bash
uv sync
# optional: dev tools (ruff, mypy, stubs)
uv sync --group dev
```

Run the CLI (console script from `pyproject.toml`):

```bash
uv run joomla-brute -u http://10.10.10.150 -w /usr/share/wordlists/rockyou.txt -usr admin
```

Or run the module / legacy filename:

```bash
uv run python -m joomla_brute -u http://10.10.10.150 -w /path/to/wordlist.txt -usr admin
uv run python joomla-brute.py -u http://10.10.10.150 -w /path/to/wordlist.txt -usr admin
```

```bash
chmod +x joomla-brute.py
./joomla-brute.py -u http://10.10.10.150 -w /usr/share/wordlists/rockyou.txt -usr admin
```

## Options

| Flag | Description |
|------|-------------|
| `-u`, `--url` | Base site URL (e.g. `http://10.10.10.150`); `/administrator/` is appended automatically. |
| `-w`, `--wordlist` | Password wordlist file. |
| `-usr`, `--username` | Single username (mutually exclusive with `-U`). |
| `-U`, `--userlist` | File of usernames (mutually exclusive with `-usr`). |
| `-p`, `--proxy` | HTTP(S) proxy, e.g. `http://127.0.0.1:8080`. |
| `-v` | Verbose: `-v` info + print failed attempts; `-vv` debug; `-vvv` also enables urllib3 connection debug. |
| `--no-color` | Disable ANSI colors (also respects `NO_COLOR` in the environment). |
| `-t`, `--threads` | Concurrent workers (each has its own HTTP session). Default scales with CPU count (capped). |
| `--no-progress` | Disable the tqdm progress bar (enabled by default on stderr). Without it, the wordlist is scanned once up front to compute the total for the bar. |

Exit code `0` if credentials are found, `1` otherwise.

## Lint and type-check

```bash
uv sync --group dev
uv run ruff check .
uv run ruff format .
uv run mypy joomla_brute
```

## Legal / ethics

Only use on systems you are authorized to test.

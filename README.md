# Configurable Python Logger

A loguru-based logger for Python that easily switches between structured JSON for production and a readable console format for development.

## Features

- Switchable Output: Toggle between structured JSON and a colorful console format.

- Automatic Context: Flattens loguru.bind() data into the top-level JSON object.

- Noise Reduction: Silences verbose logs from libraries like boto3 and urllib3.

## Installation

Install dependencies using uv. It is recommended to use a virtual environment.

### Using uv

```bash
uv add "git+https://git@github.com/ohdowon064/mylogger.git"
```

### Using pip

```bash
pip install "git+https://git@github.com/ohdowon064/mylogger.git"
```

## Usage & Output

Import set_logger to configure the format. Then use the global logger as you would with loguru.

```Python
from mylogger import set_logger, logger

# JSON output for production
set_logger(json_format=True)
logger.bind(user_id=123).info("User logged in")

# Console output for development
set_logger(json_format=False)
logger.bind(request_id="abc").error("Payment failed")
```

### JSON Output (json_format=True)

```JSON
{"level":"info","time":1725638400.123,"caller":"main.py:5","msg":"User logged in","user_id":123}
```

### Console Output (json_format=False)

```console
ERROR    | main:<module>:9 - Payment failed - {'request_id': 'abc'}
```

## License

This project is licensed under the MIT License.

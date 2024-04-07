# Status Checker

Status Checker is a Python script that checks the status of one or multiple URLs/domains and categorizes them based on their HTTP status codes.
Version 1.0.0
Created BY BLACK-SCORP10
[t.me/BLACK-SCORP10](https://t.me/BLACK_SCORP10)

## Features

- Check the status of single or multiple URLs/domains.
- Asynchronous HTTP requests for improved performance.
- Color-coded output for better visualization of status codes.
- Progress bar when checking multiple URLs.
- Save results to an output file.
- Error handling for inaccessible URLs and invalid responses.
- Command-line interface for easy usage.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/status-checker.git
   cd status-checker
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python status_checker.py [-h] [-d DOMAIN] [-l LIST] [-o OUTPUT] [-v] [-update]
```

- `-d`, `--domain`: Single domain/URL to check.
- `-l`, `--list`: File containing a list of domains/URLs to check.
- `-o`, `--output`: File to save the output.
- `-v`, `--version`: Display version information.
- `-update`: Update the tool.

**Example:**

```bash
python status_checker.py -l urls.txt -o results.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```


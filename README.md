# Status Checker
<h1 align="center">
  <br>
  <a href=" https://github.com/BLACK-SCORP10/Email-Vulnerablity-Checker.git"><img src="img/url-status-checker-logo.png"></a>
  <br>
  URL Status Checker v2.1
  <br>
</h1>
Status Checker is a Python script that checks the status of one or multiple URLs/domains and categorizes them based on their HTTP status codes.
Version 2.1.0

## Features

- Check the status of single or multiple URLs/domains.
- Asynchronous HTTP requests for improved performance.
- Follow the Redirections.
- Track all the involved IP addresses.
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

### Using bash watch command:
```bash
watch -n 72000 python url-status-checker.py -l url_list
```

**Example:**

```bash
python status_checker.py -l urls.txt -o results.txt
```
 **Preview:**
 <a href=" https://github.com/BLACK-SCORP10/Email-Vulnerablity-Checker.git"><img src="img/demo.png"></a>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

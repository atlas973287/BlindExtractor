# Blind Exploitation Tool

A powerful and flexible tool for extracting data from blind injection vulnerabilities using binary search algorithms and parallel processing. Currently, the tool only supports base64 extraction, so it is very important to write payloads that check for base64 characters.

## Features

- **Multiple Exploitation Strategies**:
  - Java RCE (Remote Code Execution)
  - Python Pickle Deserialization
  - MySQL SQL Injection
  - Local Testing Mode

- **Smart Output Extraction**:
  - Binary search algorithm for efficient data extraction
  - Parallel processing for faster results
  - Automatic base64 decoding of results
  - Adaptive output length detection

- **Interactive Shell**:
  - Command history
  - Progress bars with real-time output preview
  - Configurable worker count and batch sizes
  - Debug mode for troubleshooting

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/atlas973287/BlindExtractor
   cd BlindExtractor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the tool:
   ```bash
   python main.py [--debug]
   ```

2. Select a strategy by editing `main.py` and uncommenting the appropriate strategy:
   ```python
   # Choose your strategy here - uncomment the one you want to use
   # strategy = JavaRCEStrategy(url="http://localhost/")  # For Java RCE
   # strategy = PickleRCEStrategy(url="http://localhost/")  # For Pickle RCE
   # strategy = SQLiStrategy(url="http://localhost/")  # For SQL Injection
   strategy = LocalTestStrategy()  # For local testing
   ```

3. Use the interactive shell commands:
- `help` - Show available commands
- `workers N` - Set number of parallel workers
- `batch N` - Set batch size
- `debug on/off` - Toggle debug mode
- `history` - Show command history
- `exit` or `quit` - Exit the shell

## How It Works

The tool uses a binary search approach to extract data character by character. For blind vulnerabilities where direct output isn't possible, it:

1. Determines the length of the output using binary search
2. Extracts each character in parallel using binary search
3. Combines the results and decodes from base64

The process is optimized using:
- Parallel processing (configurable worker count)
- Batch processing to prevent server overload
- Automatic retry mechanism for failed requests
- Progress tracking with real-time preview

## Strategies

### Java RCE Strategy
Exploits Java template injection vulnerabilities to achieve remote code execution through Runtime.exec().

### Pickle RCE Strategy
Leverages Python pickle deserialization vulnerabilities to achieve remote code execution.

### MySQL Injection Strategy
Exploits blind SQL injection vulnerabilities in MySQL databases using binary search techniques.

## Debug Mode

Debug mode can be enabled in two ways:
1. Command line: `python main.py --debug`
2. Interactive shell: `debug on`

In debug mode:
- Single-threaded execution
- Detailed output for each operation
- Useful for troubleshooting and understanding the extraction process

## Requirements

- Python 3.7+
- Required packages listed in `requirements.txt`
- For process pooling: Operating system that supports `fork()` (Linux/MacOS) or `spawn` (Windows)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and authorized testing purposes only. Do not use it against systems without explicit permission.

## TODO
- Implement extraction of characters beyond base64 encoding.
- Introduce additional exploitation strategies.
- Provide an example of a time-based robust extraction strategy.
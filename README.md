# TDE - The Data Encoder

**TDE** is a fast, lightweight, dependency-free Command Line Interface (CLI) tool for Base64 encoding and decoding. Built purely with Python's standard libraries, it ensures zero security overhead and absolute portability across Windows, Linux, and macOS.

## Features

* **Zero Dependencies:** Runs natively using built-in Python libraries.
* **Cross-Platform:** Works seamlessly on Command Prompt, PowerShell, Git Bash, and Linux/macOS terminals.
* **File I/O:** Read from and write directly to files for handling large payloads or binaries.
* **URL-Safe Mode:** Seamlessly handle JSON Web Tokens (JWTs) and URL parameters.
* **Strict Validation:** Catch malformed data streams instantly.
* **Garbage Collection:** Force-decode messy inputs by stripping invalid characters automatically.

## Installation

Ensure you have Python 3.x installed. Clone this repository and install it globally using pip:

```bash
git clone https://github.com/yourusername/tde-tool.git
cd tde-tool
pip install .
```

Once installed, the `tde` command will be globally available from any terminal.

## Usage

### Basic Commands

**Encode a simple string:**

```bash
tde encode "hello world"
```

**Decode a string:**

```bash
tde decode "aGVsbG8gd29ybGQ="
```

### Advanced Modifiers

**URL-Safe Encoding:**
Generate Base64 strings safe for web transit (replaces `+`/`/` and removes padding).

```bash
tde encode "https://example.com/api" --url
```

**Strict Decoding:**
Force the tool to halt if the input contains invalid characters.

```bash
tde decode "aGVsbG8gd2!9ybGQ=" --strict
```

**Ignore Garbage:**
Attempt to extract and decode valid Base64 from a messy string containing newlines or random symbols.

```bash
tde decode "aGVsbG8  gd 29ybGQ=" --ignore-garbage
```

### File Operations

Read a payload from a file and write the decoded output to a new file:

```bash
tde decode -i extracted_payload.txt -o clean_binary.exe
```

### Help Menu

For a full list of commands and options, run:

```bash
tde --help
```

## License

MIT

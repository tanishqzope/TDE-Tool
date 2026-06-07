<p align="center">
  <img src="https://img.shields.io/badge/TDE-v1.0.0-00C853?style=for-the-badge&logo=python&logoColor=white" alt="Version"/>
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero-success?style=for-the-badge" alt="Dependencies"/>
  <img src="https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge" alt="Platform"/>
</p>

<h1 align="center">🔐 TDE — The Data Encoder</h1>

<p align="center">
  <strong>A fast, lightweight, dependency-free CLI tool for Base64 encoding & decoding.</strong><br/>
  Built purely with Python's standard libraries — zero security overhead, absolute portability.
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#%EF%B8%8F-architecture">Architecture</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🚫 **Zero Dependencies** | Runs natively using only built-in Python libraries — nothing to install, nothing to break |
| 🖥️ **Cross-Platform** | Works seamlessly on Command Prompt, PowerShell, Git Bash, WSL, and Linux/macOS terminals |
| 📁 **File I/O** | Read from and write directly to files for handling large payloads or binaries |
| 🌐 **URL-Safe Mode** | Seamlessly handle JSON Web Tokens (JWTs) and URL parameters with `-` `_` alphabet |
| 🛡️ **Strict Validation** | Catch malformed data streams instantly with `--strict` mode |
| 🧹 **Garbage Collection** | Force-decode messy inputs by stripping invalid characters automatically |
| 🔄 **Pipe Support** | Chain with other CLI tools via stdin/stdout piping |
| 🎨 **Coloured Output** | ANSI colour support with automatic graceful degradation |

---

## 📦 Installation

> **Prerequisites:** Python 3.7 or higher

### Quick Install

```bash
git clone https://github.com/tanishqzope/TDE-Tool.git
cd TDE-Tool
pip install .
```

Once installed, the `tde` command is globally available from **any terminal**.

### Verify Installation

```bash
tde --version
# Output: TDE v1.0.0
```

---

## 🚀 Usage

### Basic Encoding & Decoding

```bash
# Encode a string to Base64
tde encode "hello world"
# Output: aGVsbG8gd29ybGQ=

# Decode a Base64 string
tde decode "aGVsbG8gd29ybGQ="
# Output: hello world
```

### 🌐 URL-Safe Mode (`--url`)

Generate Base64 strings safe for web transit — replaces `+`/`/` with `-`/`_` and strips `=` padding. Perfect for **JWTs** and **URL parameters**.

```bash
tde encode "https://example.com/api?token=abc" --url
# Output: aHR0cHM6Ly9leGFtcGxlLmNvbS9hcGk_dG9rZW49YWJj
```

### 🛡️ Strict Mode (`--strict`)

Forces the tool to **halt immediately** with a clear error if the input contains any non-Base64 characters.

```bash
tde decode "aGVsbG8gd2!9ybGQ=" --strict
# Error: Strict mode: invalid Base64 character(s) found: '!'
#   Hint: use --ignore-garbage to strip them automatically.
```

### 🧹 Ignore Garbage (`--ignore-garbage`)

Strips whitespace, newlines, and invalid characters before decoding — perfect for messy copy-paste inputs.

```bash
tde decode "aGVsbG8  gd 29ybGQ=" --ignore-garbage
# Output: hello world
```

### 📁 File Operations

Read a payload from a file and write the decoded output to a new file:

```bash
# Encode a file's contents
tde encode -i secret.txt -o encoded_payload.txt

# Decode back to original
tde decode -i encoded_payload.txt -o original.txt
```

### 🔄 Piping Support

Chain TDE with other CLI tools:

```bash
# Pipe from echo
echo "sensitive data" | tde encode

# Chain with curl
curl -s https://api.example.com/data | tde decode

# Pipe between TDE commands (round-trip)
echo "hello" | tde encode | tde decode
```

### 📋 Full Help Menu

```bash
tde --help
```

```
  +========================================+
  |  TDE -- The Data Encoder / Decoder     |
  |  v1.0.0  |  Zero-dependency Base64     |
  +========================================+

positional arguments:
  {encode,decode}    Operation to perform: 'encode' or 'decode'.
  data               Inline string payload (optional if using -i or stdin).

I/O options:
  -i, --input FILE   Read payload from FILE instead of stdin/args.
  -o, --output FILE  Write result to FILE instead of stdout.

Advanced modifiers:
  --url              Use URL-safe Base64 alphabet (- _ instead of + /).
  --strict           Halt with an error on any non-Base64 character.
  --ignore-garbage   Strip whitespace and invalid characters before decoding.
```

---

## 🏗️ Architecture

### High-Level Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        tde <command> [data] [flags]              │
└──────────────────┬───────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                    1. ARGUMENT PARSER (argparse)                 │
│  ┌─────────┐   ┌─────────┐   ┌────────┐   ┌─────────────────┐  │
│  │ command │   │  data   │   │ flags  │   │   I/O options   │  │
│  │encode/  │   │(inline) │   │--url   │   │ -i input file   │  │
│  │decode   │   │         │   │--strict│   │ -o output file  │  │
│  └────┬────┘   └────┬────┘   └───┬────┘   └────────┬────────┘  │
└───────┼──────────────┼───────────┼──────────────────┼───────────┘
        │              │           │                  │
        ▼              ▼           │                  │
┌──────────────────────────────────┼──────────────────┼───────────┐
│          2. INPUT ROUTER         │                  │           │
│  Priority Hierarchy:             │                  │           │
│  ┌──────────────────────┐        │                  │           │
│  │ 1. File  (-i flag)   │◄───────┼──────────────────┘           │
│  │ 2. Stdin (piped)     │        │                              │
│  │ 3. Arg   (inline)    │        │                              │
│  └──────────┬───────────┘        │                              │
└─────────────┼────────────────────┼──────────────────────────────┘
              │                    │
              ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                   3. PROCESSING CORE                             │
│                                                                  │
│  ┌─ ENCODE ──────────────────────────────────────────────────┐   │
│  │  input bytes ──► b64encode() ──► result                   │   │
│  │  --url?       ──► urlsafe_b64encode() ──► strip '=' pad   │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─ DECODE ──────────────────────────────────────────────────┐   │
│  │  --strict?          ──► regex validate ──► halt on bad    │   │
│  │  --ignore-garbage?  ──► regex strip junk chars             │   │
│  │  --url?             ──► restore padding ──► urlsafe_b64   │   │
│  │  (default)          ──► b64decode() ──► result            │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    4. OUTPUT ROUTER                               │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  -o flag set?  ──► Write bytes to file                    │   │
│  │  (default)     ──► Print to stdout                        │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input ──► Argument Parser ──► Input Router ──► Processing Core ──► Output Router
                   │                    │                  │                   │
              Parse command        Read from:         Apply flags:       Deliver to:
              & flags             • File (-i)        • --url             • File (-o)
                                  • Stdin (pipe)     • --strict          • Stdout
                                  • Inline arg       • --ignore-garbage
```

### Module Structure

```
TDE-Tool/
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # This file
├── setup.py             # Installer with console_scripts entry point
└── tde/                 # Main package
    ├── __init__.py      # Version constant (__version__ = "1.0.0")
    └── cli.py           # Complete CLI implementation
                         #   ├── ANSI colour helpers
                         #   ├── Banner & help formatter
                         #   ├── _acquire_input()   → Input Router
                         #   ├── _encode()           → Encoding engine
                         #   ├── _decode()           → Decoding engine
                         #   ├── _emit()             → Output Router
                         #   └── main()              → Entry point
```

---

## 🔧 CLI Reference

| Argument | Type | Description |
|---|---|---|
| `encode` | Command | Convert input to Base64 |
| `decode` | Command | Convert Base64 back to original |
| `<data>` | Positional | Inline string payload |
| `-i`, `--input` | Flag | Read payload from a file |
| `-o`, `--output` | Flag | Write result to a file |
| `-v`, `--version` | Flag | Show version (`TDE v1.0.0`) |
| `-h`, `--help` | Flag | Show help menu with examples |
| `--url` | Modifier | Use URL-safe Base64 alphabet |
| `--strict` | Modifier | Error on invalid characters |
| `--ignore-garbage` | Modifier | Strip invalid characters before decoding |

> ⚠️ `--strict` and `--ignore-garbage` are **mutually exclusive** — they cannot be used together.

---

## 🎯 Use Cases

| Scenario | Command |
|---|---|
| 🔑 Encode API keys for config files | `tde encode "sk-abc123secret"` |
| 🌐 Generate URL-safe JWT tokens | `tde encode "payload" --url` |
| 📧 Decode email attachments | `tde decode -i attachment.b64 -o file.pdf` |
| 🧪 Validate Base64 integrity | `tde decode "data..." --strict` |
| 📋 Clean up messy copy-paste | `tde decode "broken data" --ignore-garbage` |
| 🔄 Round-trip verification | `echo "test" \| tde encode \| tde decode` |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/awesome-feature`)
3. **Commit** your changes (`git commit -m "Add awesome feature"`)
4. **Push** to the branch (`git push origin feature/awesome-feature`)
5. **Open** a Pull Request

### Guidelines

- Use only Python standard library — **no external dependencies**
- Maintain cross-platform compatibility
- Add comments for complex logic
- Test on both Windows and Linux/macOS

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Tanishq Zope** — [@tanishqzope](https://github.com/tanishqzope)

---

<p align="center">
  <sub>Built with ❤️ and pure Python. No dependencies were harmed in the making of this tool.</sub>
</p>

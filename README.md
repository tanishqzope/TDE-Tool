<p align="center">
  <img src="https://img.shields.io/badge/TDE-v1.2.0-00C853?style=for-the-badge&logo=python&logoColor=white" alt="Version"/>
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero-success?style=for-the-badge" alt="Dependencies"/>
  <img src="https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge" alt="Platform"/>
</p>

<h1 align="center">🔐 TDE — Tanishq's Decoder, Encoder & Hasher</h1>

<p align="center">
  <strong>A fast, lightweight, dependency-free CLI tool for multi-format encoding, decoding & hashing.</strong><br/>
  Supports <b>Base64</b>, <b>Hex</b>, <b>Base32</b>, <b>Base85</b>, and <b>12+ Hash Algorithms (SHA-256, MD5, Blake2, etc.)</b> — built purely with Python's standard libraries.
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-supported-formats">Formats</a> •
  <a href="#%EF%B8%8F-architecture">Architecture</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔄 **Multi-Format Encoding** | Supports Base64, Hex, Base32, and Base85 encoding/decoding out of the box |
| 🔑 **Hash Generation** | Instantly generate MD5, SHA-1, SHA-256, SHA-512, Blake2, and more |
| 🚫 **Zero Dependencies** | Runs natively using only built-in Python libraries — nothing to install, nothing to break |
| 🖥️ **Cross-Platform** | Works seamlessly on Command Prompt, PowerShell, Git Bash, WSL, and Linux/macOS terminals |
| 📁 **File I/O** | Read from and write directly to files for handling large payloads or binaries |
| 🌐 **URL-Safe Mode** | Seamlessly handle JSON Web Tokens (JWTs) and URL parameters with `-` `_` alphabet |
| 🛡️ **Strict Validation** | Catch malformed data streams instantly with `--strict` mode (all formats) |
| 🧹 **Garbage Collection** | Force-decode messy inputs by stripping invalid characters automatically |
| 🔄 **Pipe Support** | Chain with other CLI tools via stdin/stdout piping |
| 🎨 **Coloured Output** | ANSI colour support with automatic graceful degradation |

---

## 📦 Installation

> **Prerequisites:** Python 3.7 or higher

### Quick Install

```bash
pip install tde
```
Or
```bash
git clone https://github.com/tanishqzope/TDE-Tool.git
cd TDE-Tool
pip install .
```

Once installed, the `tde` command is globally available from **any terminal**.

### Verify Installation

```bash
tde --version
# Output: TDE v1.2.0
```

---

## 🎯 Supported Formats & Algorithms

### Encoding Formats
| Format | Flag | Alphabet | Use Case |
|---|---|---|---|
| **Base64** | `--format base64` *(default)* | `A-Z a-z 0-9 + /` | General-purpose encoding, email, MIME |
| **Hex** | `--format hex` | `0-9 a-f` | Byte-level inspection, checksums, crypto |
| **Base32** | `--format base32` | `A-Z 2-7` | Case-insensitive contexts, OTP secrets |
| **Base85** | `--format base85` | ASCII 33–117 | Maximum density, PDF internals |

### Hash Algorithms
Supported via the `hash` command and `-a` / `--algo` flag:
`md5`, `sha1`, `sha224`, `sha256` *(default)*, `sha384`, `sha512`, `sha3_224`, `sha3_256`, `sha3_384`, `sha3_512`, `blake2b`, `blake2s`.

> **Shorthand:** Use `-f` instead of `--format` for brevity — e.g., `tde encode "data" -f hex`

---

## 🚀 Usage

### Basic Encoding & Decoding (Base64 — default)

```bash
# Encode a string to Base64
tde encode "hello world"
# Output: aGVsbG8gd29ybGQ=

# Decode a Base64 string
tde decode "aGVsbG8gd29ybGQ="
# Output: hello world
```

### 🔢 Hex Encoding

```bash
# Encode to hexadecimal
tde encode "hello world" --format hex
# Output: 68656c6c6f20776f726c64

# Decode from hex
tde decode "68656c6c6f20776f726c64" --format hex
# Output: hello world
```

### 🔤 Base32 Encoding

```bash
# Encode to Base32
tde encode "hello world" --format base32
# Output: NBSWY3DPEB3W64TMMQ======

# Decode from Base32
tde decode "NBSWY3DPEB3W64TMMQ======" --format base32
# Output: hello world
```

### 📦 Base85 Encoding

```bash
# Encode to Base85 (Ascii85)
tde encode "hello world" --format base85
# Output: Xk~0{Zv

# Decode from Base85
tde decode "Xk~0{Zv" --format base85
# Output: hello world
```

### 🔑 Hashing

Generate cryptographic hashes for any input:

```bash
# SHA-256 (default)
tde hash "hello world"
# Output: b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9

# MD5 Hash
tde hash "hello world" --algo md5
# Output: 5eb63bbbe01eeed093cb22bb8f5acdc3

# Hash a file (e.g. SHA-512)
tde hash -i image.png -a sha512
```

### 🌐 URL-Safe Mode (`--url`)

Generate Base64 strings safe for web transit — replaces `+`/`/` with `-`/`_` and strips `=` padding. Perfect for **JWTs** and **URL parameters**.

```bash
tde encode "https://example.com/api?token=abc" --url
# Output: aHR0cHM6Ly9leGFtcGxlLmNvbS9hcGk_dG9rZW49YWJj
```

> ⚠️ `--url` only applies to `--format base64` (the default).

### 🛡️ Strict Mode (`--strict`)

Forces the tool to **halt immediately** with a clear error if the input contains any invalid characters for the selected format.

```bash
# Strict Base64 decode
tde decode "aGVsbG8gd2!9ybGQ=" --strict
# Error: Strict mode: invalid Base64 character(s) found: '!'

# Strict Hex decode
tde decode "68656c6c6fZZ" --format hex --strict
# Error: Strict mode: invalid hex character(s) found: 'Z'
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

# Hex-encode a binary file
tde encode -i image.png -o image_hex.txt --format hex
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

# Round-trip hex verification
echo "hello" | tde encode -f hex | tde decode -f hex
```

### 📋 Full Help Menu

```bash
tde --help
```

```
  +========================================+
  |  TDE -- The Data Encoder / Decoder     |
  |  v1.2.0  |  Encoder, Decoder & Hasher |
  +========================================+

positional arguments:
  {encode,decode,hash} Operation to perform: 'encode', 'decode', or 'hash'.
  data               Inline string payload (optional if using -i or stdin).

I/O options:
  -i, --input FILE   Read payload from FILE instead of stdin/args.
  -o, --output FILE  Write result to FILE instead of stdout.

Encoding format:
  -f, --format FMT   Encoding format: base64 (default), hex, base32, base85.

Hash options:
  -a, --algo ALGO    Hash algorithm to use (default: sha256).

Advanced modifiers:
  --url              Use URL-safe Base64 alphabet (- _ instead of + /).
  --strict           Halt with an error on any invalid character.
  --ignore-garbage   Strip whitespace and invalid characters before decoding.
```

---

## 🏗️ Architecture

### High-Level Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    tde <command> [data] [flags]                   │
└──────────────────┬───────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                    1. ARGUMENT PARSER (argparse)                 │
│  ┌─────────┐   ┌─────────┐   ┌────────┐   ┌─────────────────┐   │
│  │ command │   │  data   │   │ flags  │   │   I/O options   │   │
│  │encode/  │   │(inline) │   │--url   │   │ -i input file   │   │
│  │decode   │   │         │   │--strict│   │ -o output file  │   │
│  │         │   │         │   │-f fmt  │   │                 │   │
│  └────┬────┘   └────┬────┘   └───┬────┘   └────────┬────────┘   │
└───────┼──────────────┼───────────┼──────────────────┼────────────┘
        │              │           │                  │
        ▼              ▼           │                  │
┌──────────────────────────────────┼──────────────────┼────────────┐
│          2. INPUT ROUTER         │                  │            │
│  Priority Hierarchy:             │                  │            │
│  ┌──────────────────────┐        │                  │            │
│  │ 1. File  (-i flag)   │◄───────┼──────────────────┘            │
│  │ 2. Stdin (piped)     │        │                               │
│  │ 3. Arg   (inline)    │        │                               │
│  └──────────┬───────────┘        │                               │
└─────────────┼────────────────────┼───────────────────────────────┘
              │                    │
              ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                  3. FORMAT DISPATCHER                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  -f base64 (default)  ──► Base64 encode/decode engine       │ │
│  │  -f hex               ──► Hex encode/decode engine          │ │
│  │  -f base32            ──► Base32 encode/decode engine       │ │
│  │  -f base85            ──► Base85 encode/decode engine       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─ ENCODE ──────────────────────────────────────────────────┐   │
│  │  base64:  b64encode() / urlsafe_b64encode()               │   │
│  │  hex:     binascii.hexlify()                              │   │
│  │  base32:  b32encode()                                     │   │
│  │  base85:  b85encode()                                     │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─ DECODE ──────────────────────────────────────────────────┐   │
│  │  --strict?          ──► regex validate per format          │   │
│  │  --ignore-garbage?  ──► regex strip invalid chars          │   │
│  │  base64:  b64decode() / urlsafe_b64decode()               │   │
│  │  hex:     binascii.unhexlify()                            │   │
│  │  base32:  b32decode()                                     │   │
│  │  base85:  b85decode()                                     │   │
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
User Input ──► Argument Parser ──► Input Router ──► Format Dispatcher ──► Output Router
                    │                    │                  │                   │
               Parse command        Read from:         Apply format:       Deliver to:
               & flags             • File (-i)        • base64 (default)  • File (-o)
                                   • Stdin (pipe)     • hex               • Stdout
                                   • Inline arg       • base32
                                                      • base85
                                                      + modifiers:
                                                        --url --strict
                                                        --ignore-garbage
```

### Module Structure

```
TDE-Tool/
├── .github/
│   └── workflows/
│       └── publish.yml  # PyPI auto-publish on release
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # This file
├── setup.py             # Installer with console_scripts entry point
└── tde/                 # Main package
    ├── __init__.py      # Version constant (__version__ = "1.1.0")
    └── cli.py           # Complete CLI implementation
                         #   ├── ANSI colour helpers
                         #   ├── Banner & help formatter
                         #   ├── _acquire_input()        → Input Router
                         #   ├── _encode_base64()        → Base64 encoder
                         #   ├── _encode_hex()           → Hex encoder
                         #   ├── _encode_base32()        → Base32 encoder
                         #   ├── _encode_base85()        → Base85 encoder
                         #   ├── _encode()               → Format dispatcher (encode)
                         #   ├── _decode_base64()        → Base64 decoder
                         #   ├── _decode_hex()           → Hex decoder
                         #   ├── _decode_base32()        → Base32 decoder
                         #   ├── _decode_base85()        → Base85 decoder
                         #   ├── _decode()               → Format dispatcher (decode)
                         #   ├── _emit()                 → Output Router
                         #   └── main()                  → Entry point
```

---

## 🔧 CLI Reference

| Argument | Type | Description |
|---|---|---|
| `encode` | Command | Convert input using the selected format |
| `decode` | Command | Decode encoded data back to original |
| `hash` | Command | Generate a cryptographic hash of the input |
| `<data>` | Positional | Inline string payload |
| `-i`, `--input` | Flag | Read payload from a file |
| `-o`, `--output` | Flag | Write result to a file |
| `-f`, `--format` | Option | Encoding format: `base64` *(default)*, `hex`, `base32`, `base85` |
| `-a`, `--algo` | Option | Hash algorithm (for `hash` command): `sha256` *(default)*, `md5`, etc. |
| `-v`, `--version` | Flag | Show version (`TDE v1.2.0`) |
| `-h`, `--help` | Flag | Show help menu with examples |
| `--url` | Modifier | Use URL-safe Base64 alphabet (Base64 only) |
| `--strict` | Modifier | Error on invalid characters (all formats) |
| `--ignore-garbage` | Modifier | Strip invalid characters before decoding |

> ⚠️ `--strict` and `--ignore-garbage` are **mutually exclusive** — they cannot be used together.

> ⚠️ `--url` only applies to `--format base64`.

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
| 🔍 Inspect binary as hex | `tde encode -i binary.dat -f hex` |
| 🔐 Encode OTP secrets (Base32) | `tde encode "secret" -f base32` |
| 📄 Compact binary (Base85) | `tde encode -i data.bin -f base85` |
| 🔢 Hex round-trip | `echo "test" \| tde encode -f hex \| tde decode -f hex` |
| 🔑 Hash a password | `tde hash "mypassword" -a sha512` |
| 📁 Checksum a file | `tde hash -i release.zip -a sha256` |

---

## 📋 Changelog

### v1.2.0 — Hash Generation
- **New:** Added `hash` command for cryptographic hashing
- **New:** Support for 12+ hash algorithms including `sha256`, `md5`, `blake2b`, etc.
- **New:** Added `-a` / `--algo` flag for selecting hash algorithms

### v1.1.0 — Multi-Format Encoding

- **New:** Added `--format` / `-f` flag with support for `hex`, `base32`, and `base85` encoding
- **New:** Per-format strict validation and garbage stripping
- **New:** Dedicated encode/decode engines for each format
- **Improved:** Banner updated to reflect multi-format capability
- **Improved:** Help text with examples for all formats
- **Backwards-compatible:** Default format remains `base64`; all existing commands work unchanged

### v1.0.0 — Initial Release

- Base64 encoding & decoding
- URL-safe mode (`--url`)
- Strict validation (`--strict`)
- Garbage stripping (`--ignore-garbage`)
- File I/O (`-i`, `-o`)
- Pipe support (stdin/stdout)
- ANSI coloured output

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

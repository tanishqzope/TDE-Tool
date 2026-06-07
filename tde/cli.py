#!/usr/bin/env python3
"""
TDE - The Data Encoder/Decoder

A robust, cross-platform CLI tool for Base64 encoding and decoding.
Built entirely on Python's standard library — zero external dependencies.
"""

import argparse
import base64
import os
import re
import sys

from tde import __version__

# ──────────────────────────────────────────────────────────────────────────────
# ANSI helpers — gracefully degrade on terminals that don't support colours
# ──────────────────────────────────────────────────────────────────────────────

def _supports_colour() -> bool:
    """Return True when stdout is a TTY that likely supports ANSI escapes."""
    if os.getenv("NO_COLOR"):          # https://no-color.org/
        return False
    if os.getenv("TERM") == "dumb":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


_COLOUR = _supports_colour()

def _c(code: str, text: str) -> str:
    """Wrap *text* in an ANSI escape if colour is enabled."""
    return f"\033[{code}m{text}\033[0m" if _COLOUR else text


def _bold(t: str)   -> str: return _c("1", t)
def _cyan(t: str)   -> str: return _c("36", t)
def _green(t: str)  -> str: return _c("32", t)
def _yellow(t: str) -> str: return _c("33", t)
def _red(t: str)    -> str: return _c("31", t)
def _dim(t: str)    -> str: return _c("2", t)


# ──────────────────────────────────────────────────────────────────────────────
# Banner & custom help formatter
# ──────────────────────────────────────────────────────────────────────────────

BANNER = rf"""
  {_cyan("+========================================+")}
  {_cyan("|")}  {_bold("TDE")} -- {_green("The Data Encoder / Decoder")}    {_cyan("|")}
  {_cyan("|")}  {_dim(f"v{__version__}  |  Zero-dependency Base64")}    {_cyan("|")}
  {_cyan("+========================================+")}
"""

EPILOG = f"""
{_bold("Examples:")}

  {_green("Encode a string:")}
    tde encode "hello world"

  {_green("Decode a string:")}
    tde decode "aGVsbG8gd29ybGQ="

  {_green("URL-safe encode:")}
    tde encode "https://example.com/api?q=1" --url

  {_green("Strict decode (halt on bad chars):")}
    tde decode "aGVsbG8gd2!9ybGQ=" --strict

  {_green("Ignore garbage (strip junk, then decode):")}
    tde decode "aGVsbG8  gd 29ybGQ=" --ignore-garbage

  {_green("File I/O -- read from file, write result to file:")}
    tde decode -i payload.txt -o output.bin

  {_green("Pipe from another command:")}
    echo hello | tde encode
"""


class _Formatter(argparse.RawDescriptionHelpFormatter):
    """Widen the help output a bit for readability."""

    def __init__(self, prog: str, **kwargs):
        kwargs.setdefault("max_help_position", 30)
        kwargs.setdefault("width", 80)
        super().__init__(prog, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
# Input acquisition -- file > stdin > positional arg
# ──────────────────────────────────────────────────────────────────────────────

def _acquire_input(args) -> bytes:
    """
    Resolve the data payload using a strict priority hierarchy:
      1. --input / -i  (file path)
      2. stdin          (piped data)
      3. positional     (inline string argument)
    Returns raw bytes ready for processing.
    """
    # 1. File input — highest priority
    if args.input:
        path = os.path.expanduser(args.input)
        if not os.path.isfile(path):
            _die(f"Input file not found: {path}")
        try:
            with open(path, "rb") as fh:
                return fh.read()
        except OSError as exc:
            _die(f"Cannot read file '{path}': {exc}")

    # 2. Piped stdin — detect whether data is waiting on the pipe
    if not sys.stdin.isatty():
        data = sys.stdin.buffer.read()
        if data:
            return data

    # 3. Direct positional argument
    if args.data:
        return args.data.encode("utf-8")

    # Nothing provided
    _die("No input provided. Supply a string, use -i <file>, or pipe data via stdin.")


# ──────────────────────────────────────────────────────────────────────────────
# Processing core — encode / decode with modifiers
# ──────────────────────────────────────────────────────────────────────────────

def _encode(payload: bytes, *, url_safe: bool) -> bytes:
    """
    Encode raw bytes to Base64.

    When --url is active, use the URL-safe alphabet (- and _ instead of
    + and /) and strip trailing '=' padding so the result can be embedded
    safely in URLs and JWTs.
    """
    if url_safe:
        encoded = base64.urlsafe_b64encode(payload)
        return encoded.rstrip(b"=")          # strip padding for URL safety
    return base64.b64encode(payload)


def _decode(payload: bytes, *, url_safe: bool, strict: bool,
            ignore_garbage: bool) -> bytes:
    """
    Decode a Base64 payload back to its original bytes.

    Modifier behaviour:
      --strict          Validate the payload against the Base64 alphabet
                        *before* decoding and abort with a clear error on
                        any illegal character.
      --ignore-garbage  Strip every character that is NOT part of the Base64
                        alphabet (A-Z a-z 0-9 + / = - _) so that messy
                        inputs (e.g. with newlines, tabs, stray symbols)
                        can still be decoded.
      --url             Restore padding and use the URL-safe alphabet for
                        decoding.
    """
    text = payload.decode("ascii", errors="ignore")

    # ── Strict validation ────────────────────────────────────────────────
    # Check BEFORE any cleaning so the user sees exactly what's wrong.
    if strict:
        if url_safe:
            bad = re.findall(r"[^A-Za-z0-9\-_=\s]", text)
        else:
            bad = re.findall(r"[^A-Za-z0-9+/=\s]", text)
        if bad:
            unique = sorted(set(bad))
            _die(
                f"Strict mode: invalid Base64 character(s) found: "
                f"{', '.join(repr(c) for c in unique)}\n"
                f"  Hint: use --ignore-garbage to strip them automatically."
            )

    # ── Garbage stripping ────────────────────────────────────────────────
    # Remove everything outside the valid Base64 alphabet so noisy inputs
    # (copy-paste artefacts, line-wrapping whitespace, etc.) don't break
    # the decoder.
    if ignore_garbage:
        if url_safe:
            text = re.sub(r"[^A-Za-z0-9\-_=]", "", text)
        else:
            text = re.sub(r"[^A-Za-z0-9+/=]", "", text)
    else:
        # Even without --ignore-garbage we strip surrounding whitespace
        text = text.strip()

    # ── URL-safe decoding ────────────────────────────────────────────────
    # Re-pad the string because urlsafe_b64decode expects correct padding.
    if url_safe:
        pad = 4 - len(text) % 4
        if pad != 4:
            text += "=" * pad
        try:
            return base64.urlsafe_b64decode(text)
        except Exception as exc:
            _die(f"Decoding failed: {exc}")

    # ── Standard decoding ────────────────────────────────────────────────
    try:
        return base64.b64decode(text)
    except Exception as exc:
        _die(f"Decoding failed: {exc}")


# ──────────────────────────────────────────────────────────────────────────────
# Output routing — stdout or file
# ──────────────────────────────────────────────────────────────────────────────

def _emit(result: bytes, args) -> None:
    """
    Route the processed result to the appropriate destination.
    If -o / --output is set, write bytes to the specified file.
    Otherwise print to stdout as UTF-8 text (with a trailing newline).
    """
    if args.output:
        path = os.path.expanduser(args.output)
        try:
            with open(path, "wb") as fh:
                fh.write(result)
            _info(f"Output written to {_bold(path)}")
        except OSError as exc:
            _die(f"Cannot write to '{path}': {exc}")
    else:
        # For terminal output, decode to UTF-8 with replacement so binary
        # payloads don't crash the shell.
        sys.stdout.buffer.write(result)
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()


# ──────────────────────────────────────────────────────────────────────────────
# Logging helpers
# ──────────────────────────────────────────────────────────────────────────────

def _info(msg: str) -> None:
    _stderr(f"{_green('[OK]')} {msg}")


def _stderr(msg: str) -> None:
    """Write to stderr, replacing unencodable chars so Windows never crashes."""
    try:
        sys.stderr.write(msg + "\n")
    except UnicodeEncodeError:
        sys.stderr.buffer.write(msg.encode("utf-8", errors="replace"))
        sys.stderr.buffer.write(b"\n")
        sys.stderr.buffer.flush()


def _die(msg: str, code: int = 1) -> None:
    """Print a coloured error message and exit."""
    _stderr(f"\n{_red('Error:')} {msg}")
    sys.exit(code)


# ──────────────────────────────────────────────────────────────────────────────
# Argument parser construction
# ──────────────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tde",
        description=BANNER,
        epilog=EPILOG,
        formatter_class=_Formatter,
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"TDE v{__version__}",
    )

    # ── Positional: command & optional inline data ────────────────────────
    parser.add_argument(
        "command",
        choices=["encode", "decode"],
        help="Operation to perform: 'encode' or 'decode'.",
    )
    parser.add_argument(
        "data",
        nargs="?",
        default=None,
        help="Inline string payload (optional if using -i or stdin).",
    )

    # ── I/O flags ────────────────────────────────────────────────────────
    io_group = parser.add_argument_group("I/O options")
    io_group.add_argument(
        "-i", "--input",
        metavar="FILE",
        help="Read payload from FILE instead of stdin/args.",
    )
    io_group.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="Write result to FILE instead of stdout.",
    )

    # ── Advanced modifiers ───────────────────────────────────────────────
    mod_group = parser.add_argument_group("Advanced modifiers")
    mod_group.add_argument(
        "--url",
        action="store_true",
        default=False,
        help="Use URL-safe Base64 alphabet (- _ instead of + /).",
    )
    mod_group.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Halt with an error on any non-Base64 character.",
    )
    mod_group.add_argument(
        "--ignore-garbage",
        action="store_true",
        default=False,
        help="Strip whitespace and invalid characters before decoding.",
    )

    return parser


# ──────────────────────────────────────────────────────────────────────────────
# Main entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    # Mutually exclusive sanity check
    if args.strict and args.ignore_garbage:
        _die("--strict and --ignore-garbage are mutually exclusive.\n"
             "  --strict  demands perfect input.\n"
             "  --ignore-garbage silently discards bad characters.\n"
             "  Pick one.")

    # Acquire the raw payload bytes
    payload = _acquire_input(args)

    # Route to the appropriate processing function
    if args.command == "encode":
        result = _encode(payload, url_safe=args.url)
    else:
        result = _decode(
            payload,
            url_safe=args.url,
            strict=args.strict,
            ignore_garbage=args.ignore_garbage,
        )

    # Deliver the result
    _emit(result, args)


if __name__ == "__main__":
    main()

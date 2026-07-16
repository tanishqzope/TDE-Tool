import argparse
import base64
import binascii
import os
import re
import sys
import hashlib

from tde import __version__


# ── Supported encoding formats ────────────────────────────────────────
FORMATS = ("base64", "hex", "base32", "base85")
HASH_ALGOS = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_224", "sha3_256", "sha3_384", "sha3_512", "blake2b", "blake2s")


def _supports_colour() -> bool:
    if os.getenv("NO_COLOR"):          
        return False
    if os.getenv("TERM") == "dumb":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


_COLOUR = _supports_colour()

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _COLOUR else text


def _bold(t: str)   -> str: return _c("1", t)
def _cyan(t: str)   -> str: return _c("36", t)
def _green(t: str)  -> str: return _c("32", t)
def _yellow(t: str) -> str: return _c("33", t)
def _red(t: str)    -> str: return _c("31", t)
def _dim(t: str)    -> str: return _c("2", t)
def _magenta(t: str) -> str: return _c("35", t)




BANNER = rf"""
  {_cyan("+========================================+")}
  {_cyan("|")}  {_bold("TDE")} -- {_green("The Data Encoder / Decoder")}    {_cyan("|")}
  {_cyan("|")}  {_dim(f"v{__version__}  |  Encoder, Decoder & Hasher")} {_cyan("|")}
  {_cyan("+========================================+")}
"""

EPILOG = f"""
{_bold("Examples:")}

  {_green("Encode a string (Base64, default):")}
    tde encode "hello world"

  {_green("Decode a string:")}
    tde decode "aGVsbG8gd29ybGQ="

  {_green("Hex encode:")}
    tde encode "hello world" --format hex

  {_green("Base32 encode:")}
    tde encode "hello world" --format base32

  {_green("Base85 (Ascii85) encode:")}
    tde encode "hello world" --format base85

  {_green("URL-safe Base64 encode:")}
    tde encode "https://example.com/api?q=1" --url

  {_green("Strict decode (halt on bad chars):")}
    tde decode "aGVsbG8gd2!9ybGQ=" --strict

  {_green("Ignore garbage (strip junk, then decode):")}
    tde decode "aGVsbG8  gd 29ybGQ=" --ignore-garbage

  {_green("File I/O -- read from file, write result to file:")}
    tde decode -i payload.txt -o output.bin

  {_green("Pipe from another command:")}
    echo hello | tde encode

  {_green("Round-trip hex verification:")}
    echo hello | tde encode -f hex | tde decode -f hex

  {_green("Hash a string (SHA-256, default):")}
    tde hash "hello world"

  {_green("Hash with MD5:")}
    tde hash "hello world" --algo md5
"""


class _Formatter(argparse.RawDescriptionHelpFormatter):

    def __init__(self, prog: str, **kwargs):
        kwargs.setdefault("max_help_position", 30)
        kwargs.setdefault("width", 80)
        super().__init__(prog, **kwargs)




def _acquire_input(args) -> bytes:
  
    if args.input:
        path = os.path.expanduser(args.input)
        if not os.path.isfile(path):
            _die(f"Input file not found: {path}")
        try:
            with open(path, "rb") as fh:
                return fh.read()
        except OSError as exc:
            _die(f"Cannot read file '{path}': {exc}")

    
    if not sys.stdin.isatty():
        data = sys.stdin.buffer.read()
        if data:
            return data

    
    if args.data:
        return args.data.encode("utf-8")

  
    _die("No input provided. Supply a string, use -i <file>, or pipe data via stdin.")


# ── Encoding engines ──────────────────────────────────────────────────

def _encode_base64(payload: bytes, *, url_safe: bool) -> bytes:
    if url_safe:
        encoded = base64.urlsafe_b64encode(payload)
        return encoded.rstrip(b"=")          
    return base64.b64encode(payload)


def _encode_hex(payload: bytes) -> bytes:
    return binascii.hexlify(payload)


def _encode_base32(payload: bytes) -> bytes:
    return base64.b32encode(payload)


def _encode_base85(payload: bytes) -> bytes:
    return base64.b85encode(payload)


def _encode(payload: bytes, *, url_safe: bool, fmt: str) -> bytes:
    if fmt == "base64":
        return _encode_base64(payload, url_safe=url_safe)
    elif fmt == "hex":
        return _encode_hex(payload)
    elif fmt == "base32":
        return _encode_base32(payload)
    elif fmt == "base85":
        return _encode_base85(payload)
    else:
        _die(f"Unknown format: {fmt}")


# ── Decoding engines ──────────────────────────────────────────────────

def _decode_base64(payload: bytes, *, url_safe: bool, strict: bool,
                   ignore_garbage: bool) -> bytes:
    text = payload.decode("ascii", errors="ignore")

 
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

  
    if ignore_garbage:
        if url_safe:
            text = re.sub(r"[^A-Za-z0-9\-_=]", "", text)
        else:
            text = re.sub(r"[^A-Za-z0-9+/=]", "", text)
    else:
        
        text = text.strip()

  
    if url_safe:
        pad = 4 - len(text) % 4
        if pad != 4:
            text += "=" * pad
        try:
            return base64.urlsafe_b64decode(text)
        except Exception as exc:
            _die(f"Base64 decoding failed: {exc}")


    try:
        return base64.b64decode(text)
    except Exception as exc:
        _die(f"Base64 decoding failed: {exc}")


def _decode_hex(payload: bytes, *, strict: bool,
                ignore_garbage: bool) -> bytes:
    text = payload.decode("ascii", errors="ignore")

    if strict:
        bad = re.findall(r"[^0-9a-fA-F\s]", text)
        if bad:
            unique = sorted(set(bad))
            _die(
                f"Strict mode: invalid hex character(s) found: "
                f"{', '.join(repr(c) for c in unique)}\n"
                f"  Hint: use --ignore-garbage to strip them automatically."
            )

    if ignore_garbage:
        text = re.sub(r"[^0-9a-fA-F]", "", text)
    else:
        text = text.strip()

    try:
        return binascii.unhexlify(text)
    except Exception as exc:
        _die(f"Hex decoding failed: {exc}")


def _decode_base32(payload: bytes, *, strict: bool,
                   ignore_garbage: bool) -> bytes:
    text = payload.decode("ascii", errors="ignore")

    if strict:
        bad = re.findall(r"[^A-Z2-7=\s]", text)
        if bad:
            unique = sorted(set(bad))
            _die(
                f"Strict mode: invalid Base32 character(s) found: "
                f"{', '.join(repr(c) for c in unique)}\n"
                f"  Hint: use --ignore-garbage to strip them automatically."
            )

    if ignore_garbage:
        text = re.sub(r"[^A-Z2-7=]", "", text)
    else:
        text = text.strip()

    # Base32 requires uppercase
    text = text.upper()

    try:
        return base64.b32decode(text)
    except Exception as exc:
        _die(f"Base32 decoding failed: {exc}")


def _decode_base85(payload: bytes, *, strict: bool,
                   ignore_garbage: bool) -> bytes:
    text = payload.decode("ascii", errors="ignore")

    if ignore_garbage:
        text = text.strip()
    else:
        text = text.strip()

    try:
        return base64.b85decode(text)
    except Exception as exc:
        _die(f"Base85 decoding failed: {exc}")


def _decode(payload: bytes, *, url_safe: bool, strict: bool,
            ignore_garbage: bool, fmt: str) -> bytes:
    if fmt == "base64":
        return _decode_base64(payload, url_safe=url_safe, strict=strict,
                              ignore_garbage=ignore_garbage)
    elif fmt == "hex":
        return _decode_hex(payload, strict=strict,
                           ignore_garbage=ignore_garbage)
    elif fmt == "base32":
        return _decode_base32(payload, strict=strict,
                              ignore_garbage=ignore_garbage)
    elif fmt == "base85":
        return _decode_base85(payload, strict=strict,
                              ignore_garbage=ignore_garbage)
    else:
        _die(f"Unknown format: {fmt}")


# ── Hash engines ──────────────────────────────────────────────────────

def _hash(payload: bytes, algo: str) -> bytes:
    if algo not in HASH_ALGOS:
        _die(f"Unknown hash algorithm: {algo}")
    h = hashlib.new(algo)
    h.update(payload)
    return h.hexdigest().encode("ascii")


def _emit(result: bytes, args) -> None:
    if args.output:
        path = os.path.expanduser(args.output)
        try:
            with open(path, "wb") as fh:
                fh.write(result)
            _info(f"Output written to {_bold(path)}")
        except OSError as exc:
            _die(f"Cannot write to '{path}': {exc}")
    else:
       
        sys.stdout.buffer.write(result)
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()




def _info(msg: str) -> None:
    _stderr(f"{_green('[OK]')} {msg}")


def _stderr(msg: str) -> None:
    try:
        sys.stderr.write(msg + "\n")
    except UnicodeEncodeError:
        sys.stderr.buffer.write(msg.encode("utf-8", errors="replace"))
        sys.stderr.buffer.write(b"\n")
        sys.stderr.buffer.flush()


def _die(msg: str, code: int = 1) -> None:
    _stderr(f"\n{_red('Error:')} {msg}")
    sys.exit(code)




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

   
    parser.add_argument(
        "command",
        choices=["encode", "decode", "hash"],
        help="Operation to perform: 'encode', 'decode', or 'hash'.",
    )
    parser.add_argument(
        "data",
        nargs="?",
        default=None,
        help="Inline string payload (optional if using -i or stdin).",
    )

  
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

  
    mod_group = parser.add_argument_group("Encoding format")
    mod_group.add_argument(
        "-f", "--format",
        choices=FORMATS,
        default="base64",
        metavar="FMT",
        help="Encoding format: base64 (default), hex, base32, base85.",
    )

    hash_group = parser.add_argument_group("Hash options")
    hash_group.add_argument(
        "-a", "--algo",
        choices=HASH_ALGOS,
        default="sha256",
        metavar="ALGO",
        help="Hash algorithm to use (default: sha256).",
    )

    flag_group = parser.add_argument_group("Advanced modifiers")
    flag_group.add_argument(
        "--url",
        action="store_true",
        default=False,
        help="Use URL-safe Base64 alphabet (- _ instead of + /). Only applies to base64 format.",
    )
    flag_group.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Halt with an error on any invalid character for the chosen format.",
    )
    flag_group.add_argument(
        "--ignore-garbage",
        action="store_true",
        default=False,
        help="Strip whitespace and invalid characters before decoding.",
    )

    return parser




def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    fmt = args.format

    if args.strict and args.ignore_garbage:
        _die("--strict and --ignore-garbage are mutually exclusive.\n"
             "  --strict  demands perfect input.\n"
             "  --ignore-garbage silently discards bad characters.\n"
             "  Pick one.")

    # --url only applies to base64
    if args.url and fmt != "base64":
        _die(f"--url is only valid with --format base64 (current: {fmt}).")

    payload = _acquire_input(args)


    if args.command == "encode":
        result = _encode(payload, url_safe=args.url, fmt=fmt)
    elif args.command == "hash":
        result = _hash(payload, algo=args.algo)
    else:
        result = _decode(
            payload,
            url_safe=args.url,
            strict=args.strict,
            ignore_garbage=args.ignore_garbage,
            fmt=fmt,
        )

 
    _emit(result, args)


if __name__ == "__main__":
    main()

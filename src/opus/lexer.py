from dataclasses import dataclass
from typing import Final, Union

DELIMITERS: Final[set[str]] = set(["\n", "\r", "\b", "\f", " "])
DENIED_SYMBOLS: Final[set[str]] = set(["\t"])
BRACKETS: Final[list[tuple[str, str]]] = [
    ("{", "}"),
    ("[", "]"),
    ("(", ")"),
]
OPEN_BRAKETS: Final[set[str]] = set(map(lambda x: x[0], BRACKETS))
CLOSE_BRAKETS: Final[set[str]] = set(map(lambda x: x[1], BRACKETS))
OPEN_BRAKETS_LIST: Final[list[str]] = list(map(lambda x: x[0], BRACKETS))
CLOSE_BRAKETS_LIST: Final[list[str]] = list(map(lambda x: x[1], BRACKETS))


class UnknownBracketError(Exception):
    def __init__(self, bracket: str):
        self.bracket = bracket
        msg = "Unknown braket type: '{}'".format(bracket)
        super().__init__(msg)


def escape_string(string: str) -> str:
    escapes = [
        ("\\", "\\\\"),
        ('"', r"\""),
        ("'", r"\'"),
        ("\n", r"\n"),
        ("\r", r"\r"),
        ("\t", r"\t"),
        ("\b", r"\b"),
        ("\f", r"\f"),
    ]
    for escape in escapes:
        string = string.replace(escape[0], escape[1])
    return string


@dataclass
class TokenListStart:
    bracket_id: int

    def __init__(self, bracket):
        try:
            self.bracket_id = OPEN_BRAKETS_LIST.index(bracket)
        except ValueError as e:
            raise UnknownBracketError(bracket)

    def __str__(self) -> str:
        return "("


@dataclass
class TokenListEnd:
    bracket_id: int

    def __init__(self, bracket):
        try:
            self.bracket_id = CLOSE_BRAKETS_LIST.index(bracket)
        except ValueError as e:
            raise UnknownBracketError(bracket)

    def __str__(self) -> str:
        return ")"

    def isMatch(self, start: TokenListStart) -> bool:
        return self.bracket_id == start.bracket_id


@dataclass
class TokenAtom:
    text: str

    def __str__(self) -> str:
        return "|{}|".format(self.text)


@dataclass
class TokenAtomQuotted:
    text: str

    def __str__(self) -> str:
        return '|"{}"|'.format(escape_string(self.text))


@dataclass
class TokenColon:
    def __str__(self) -> str:
        return ":"


@dataclass
class TokenSemicolon:
    def __str__(self) -> str:
        return ";"


@dataclass
class TokenComment:
    body: str

    def __str__(self) -> str:
        return "[{}]".format(escape_string(self.body))


Token = Union[
    TokenListStart,
    TokenListEnd,
    TokenAtom,
    TokenAtomQuotted,
    TokenColon,
    TokenSemicolon,
    TokenComment,
]

Tokens = list[Token]


def token_to_string(token: Token) -> str:
    return str(token)


def tokens_to_string(tokens: Tokens) -> str:
    string = ""
    for token in tokens:
        string += " " + str(token)
    return string[1:]


def look(text: str, index: int) -> tuple[str, str | None]:
    cur = text[index]
    nxt = None
    if index + 1 < len(text):
        nxt = text[index + 1]
    return (cur, nxt)


def decode_char_hex_code(code: str) -> str:
    return chr(int("0x" + code, 16))


def decode_char_octo_code(code: str) -> str:
    return chr(int("0o" + code, 8))

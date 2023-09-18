from src.opus import lexer


def test_escape_string():
    assert r"\n\r\t\f\b\'" == lexer.escape_string("\n\r\t\f\b'")
    assert r"\n\r\t\f\b\"" == lexer.escape_string('\n\r\t\f\b"')


def test_pase_brackets():
    cases = [
        ("{", 0, lexer.UnknownBracketError("{")),
        ("[", 1, lexer.UnknownBracketError("[")),
        ("(", 2, lexer.UnknownBracketError("(")),
        ("}", lexer.UnknownBracketError("}"), 0),
        ("]", lexer.UnknownBracketError("]"), 1),
        (")", lexer.UnknownBracketError(")"), 2),
    ]
    for cse in cases:
        bracket = cse[0]
        if isinstance(cse[1], Exception):
            try:
                lexer.TokenListStart(bracket)
            except Exception as e:
                assert str(e) == str(cse[1])
        else:
            lexer.TokenListStart(bracket).bracket_id = cse[1]
        if isinstance(cse[2], Exception):
            try:
                lexer.TokenListEnd(bracket)
            except Exception as e:
                assert str(e) == str(cse[2])
        else:
            lexer.TokenListEnd(bracket).bracket_id = cse[2]


def test_brackets_match():
    cases = [
        ("{", "}"),
        ("[", "]"),
        ("(", ")"),
    ]
    for i in range(len(cases)):
        for j in range(len(cases)):
            left = lexer.TokenListStart(cases[i][0])
            right = lexer.TokenListEnd(cases[j][1])
            assert right.isMatch(left) == (i == j)


def test_tokens_to_string():
    string = "( |abcd'| |\"abcd\\'\"| : ; [comment body] )"
    tokens = [
        lexer.TokenListStart("{"),
        lexer.TokenAtom("abcd'"),
        lexer.TokenAtomQuotted("abcd'"),
        lexer.TokenColon(),
        lexer.TokenSemicolon(),
        lexer.TokenComment("comment body"),
        lexer.TokenListEnd("]"),
    ]
    assert string == lexer.tokens_to_string(tokens)

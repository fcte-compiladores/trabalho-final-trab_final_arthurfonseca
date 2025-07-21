import pytest
from src.lexer import tokenize, Token, TokenType, LexerError

@pytest.mark.parametrize("expr, expected", [
    # Casos simples com uma operação básica
    ("1+2", [
        Token(TokenType.NUMBER, 1),
        Token(TokenType.PLUS, "+"),
        Token(TokenType.NUMBER, 2),
    ]),
    
    # Casos com espaços extras
    ("  12  - 5 ", [
        Token(TokenType.NUMBER, 12),
        Token(TokenType.MINUS, "-"),
        Token(TokenType.NUMBER, 5),
    ]),

    # Casos com múltiplos operadores e números
    ("3*4/ 2", [
        Token(TokenType.NUMBER, 3),
        Token(TokenType.MUL, "*"),
        Token(TokenType.NUMBER, 4),
        Token(TokenType.DIV, "/"),
        Token(TokenType.NUMBER, 2),
    ]),

    # Casos com parênteses
    ("(7)", [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.NUMBER, 7),
        Token(TokenType.RPAREN, ")"),
    ]),

    # Teste com mais de um dígito
    ("12345", [
        Token(TokenType.NUMBER, 12345),
    ]),

    # Expressão com múltiplos operadores e parênteses
    ("(3 + 5) * (2 - 4)", [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.NUMBER, 3),
        Token(TokenType.PLUS, "+"),
        Token(TokenType.NUMBER, 5),
        Token(TokenType.RPAREN, ")"),
        Token(TokenType.MUL, "*"),
        Token(TokenType.LPAREN, "("),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.MINUS, "-"),
        Token(TokenType.NUMBER, 4),
        Token(TokenType.RPAREN, ")"),
    ])
])
def test_tokenize_basic(expr, expected):
    # Compara cada token da lista de saída
    result = tokenize(expr)
    for r, e in zip(result, expected):
        assert r.type == e.type
        assert r.value == e.value

def test_tokenize_multiple_digits():
    # Testa números com mais de um dígito
    assert tokenize("12345") == [Token(TokenType.NUMBER, 12345)]

def test_unexpected_character():
    # Verifica que um caractere inesperado gera um erro
    with pytest.raises(LexerError):
        tokenize("2 & 3")

def test_empty_expression():
    # Teste de expressão vazia
    assert tokenize("") == []

def test_invalid_character_at_start():
    # Caso com caractere inválido no início
    with pytest.raises(LexerError):
        tokenize("@3 + 5")

def test_invalid_character_in_middle():
    # Caso com caractere inválido no meio da expressão
    with pytest.raises(LexerError):
        tokenize("3 + 5 @ 7")

def test_unexpected_operator():
    # Caso de operador no lugar errado
    with pytest.raises(LexerError):
        tokenize("3 + + 5")

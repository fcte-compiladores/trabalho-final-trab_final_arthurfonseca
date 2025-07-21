import re
import sys
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Union
from colorama import Fore, Style, init

# Inicializa o colorama no Windows
init(autoreset=True)

class LexerError(Exception):
    """Erro levantado quando um caractere inesperado ou sequência inválida é encontrada."""
    def __init__(self, message: str, position: int = None):
        if position is not None:
            message = f"{message} (posição {position})"
        super().__init__(message)
        self.position = position

class TokenType(Enum):
    """Enumeração dos tipos de token possíveis."""
    NUMBER  = auto()
    PLUS    = auto()
    MINUS   = auto()
    MUL     = auto()
    DIV     = auto()
    LPAREN  = auto()
    RPAREN  = auto()

# Mapeamento tipo → regex
TOKEN_SPEC = [
    (TokenType.NUMBER,  r'\d+'),
    (TokenType.PLUS,    r'\+'),
    (TokenType.MINUS,   r'-'),
    (TokenType.MUL,     r'\*'),
    (TokenType.DIV,     r'/'),
    (TokenType.LPAREN,  r'\('),
    (TokenType.RPAREN,  r'\)'),
    # WS (whitespace) para ser ignorado
    ('WS',             r'\s+'),
]

# Compila o padrão mestre com grupos nomeados, inclusive 'WS'
master_pattern = re.compile(
    '|'.join(
        f"(?P<{tt.name if isinstance(tt, TokenType) else tt}>{pattern})"
        for tt, pattern in TOKEN_SPEC
    )
)

@dataclass
class Token:
    """
    Representa um token da expressão.

    :param type: Tipo do token (TokenType).
    :param value: Valor textual ou numérico associado.
    """
    type: TokenType
    value: Union[int, str]

    def __repr__(self) -> str:
        color_map = {
            TokenType.NUMBER:  Fore.MAGENTA,
            TokenType.PLUS:    Fore.GREEN,
            TokenType.MINUS:   Fore.RED,
            TokenType.MUL:     Fore.YELLOW,
            TokenType.DIV:     Fore.BLUE,
            TokenType.LPAREN:  Fore.CYAN,
            TokenType.RPAREN:  Fore.CYAN,
        }
        base_color = color_map.get(self.type, Fore.WHITE)
        if self.type == TokenType.NUMBER:
            # CORREÇÃO: Adicionar reset de cor após o valor
            return f"{base_color}{self.type.name}{Fore.WHITE}({self.value}){Style.RESET_ALL}"
        # CORREÇÃO: Adicionar reset de cor para todos os tokens
        return f"{base_color}{self.type.name}{Style.RESET_ALL}"

def tokenize(text: str) -> List[Token]:
    """
    Converte uma string em uma lista de tokens, ignorando espaços em branco.
    Usa re.finditer para iterar sobre os matches e detecta operadores consecutivos.

    :param text: Expressão de entrada, ex: "3 + 4*(2-1)"
    :return: Lista de Token
    :raises LexerError: em caso de caractere inesperado ou operador inválido.
    """
    tokens: List[Token] = []
    last_end = 0
    last_token: Token = None

    for match in master_pattern.finditer(text):
        if match.start() != last_end:
            bad = text[last_end:match.start()]
            raise LexerError(f"Caractere(s) inesperado(s): {bad!r}", last_end)

        kind = match.lastgroup
        value = match.group()
        last_end = match.end()

        if kind == 'WS':
            continue

        # converte valor de NUMBER para int
        if kind == 'NUMBER':
            tok = Token(TokenType.NUMBER, int(value))
        else:
            tok = Token(TokenType[kind], value)

        # detecta operadores consecutivos
        if tok.type in {TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV}:
            if last_token and last_token.type in {TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV}:
                raise LexerError(f"Operador inesperado: {tok.value} após {last_token.value}", match.start())

        tokens.append(tok)
        last_token = tok

    if last_end != len(text):
        bad = text[last_end:]
        raise LexerError(f"Caractere(s) inesperado(s) no final: {bad!r}", last_end)

    return tokens

def main():
    """
    Ponto de entrada: exige exatamente um único argumento de expressão entre aspas.
    Se não for dado ou se não for uma expressão válida dentro de aspas, será
    lançado um erro de lexing.
    """
    args = sys.argv[1:]

    # Verifica se há exatamente um argumento
    if len(args) != 1:
        print(f"\nErro de lexing: Escreva expressão entre \"\"")
        sys.exit(1)

    expr = args[0]  # O argumento é a expressão entre aspas

    # Verifica se a expressão contém apenas espaços ou está vazia
    if not expr.strip():
        print(f"\nErro de lexing: A expressão está vazia ou contém apenas espaços.")
        sys.exit(1)

    try:
        # Tenta tokenizar a expressão
        tokens = tokenize(expr)
        print(f"\nTokens: {tokens}")
    except LexerError as e:
        print(f"\nErro de lexing: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Hppw7Zh2)
# **Scanner Léxico para Expressões Aritméticas**

## **Integrantes:**

Arthur Fonseca - 221031120 - Turma 02


## **Introdução**

Este projeto implementa a fase de análise léxica (tokenização) de uma linguagem de expressões aritméticas simples, suportando:

- Números inteiros (sem sinal).

- Operadores: +, -, *, /.

- Parênteses: (, ).

- Espaços em branco, que são ignorados.

O lexer recebe uma string de entrada e produz uma sequência de tokens, cada token representando um número ou símbolo.

### Tokens e suas representações:
- NUMBER:

  - Representa valores numéricos (inteiros), como 12, 24, 100.

  - Exemplo: NUMBER(12), NUMBER(24).

- PLUS ('+'):

  - Representa o operador de adição.

  - Exemplo: Na expressão "12 + 24", o token PLUS ('+') representa o operador de adição:

- MINUS ('-'):

  - Representa o operador de subtração.

  - Exemplo: Na expressão "5 - 3", o token MINUS ('-') representa a subtração:


- MUL ('*'):

  - Representa o operador de multiplicação.

  - Exemplo: Na expressão "3 * 4", o token MUL ('*') representa a multiplicação:

- DIV ('/'):

  - Representa o operador de divisão.

  - Exemplo: Na expressão "8 / 2", o token DIV ('/'): representa a divisão.

- LPAREN ('('):

  - Representa o parêntese esquerdo (abre a expressão).

  - Exemplo: Na expressão "3 * (2 + 5)", o token LPAREN ('(') abre o parêntese.

- RPAREN (')') :

  - Representa o parêntese direito (fecha a expressão).

  - Exemplo: Exemplo: Na expressão "3 * (2 + 5)", o token LPAREN (')') fecha o parêntese.

## **Instalação**

1. Certifique-se de ter Python 3.8+ instalado.

2. (Opcional) Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale dependências (caso haja):
```bash
pip install -r requirements.txt
```

## **Uso e Exemplos**

Exemplo de chamada via script (Sim, deve-se se usar entre aspas!):
```bash
python src/lexer.py "12 + 24*(3 - 4)"
```

Deve produzir algo como:
```bash
Tokens: [NUMBER(12), PLUS, NUMBER(24), MUL, LPAREN, NUMBER(3), MINUS, NUMBER(4), RPAREN]
```

Assim como uma entrada: 
```bash
python src/lexer.py "7* ( 3 + 5 ) -10"
```
Deve reproduzir uma saída:
```bash
Tokens: [NUMBER(7), MUL, LPAREN, NUMBER(3), PLUS, NUMBER(5), RPAREN, MINUS, NUMBER(10)]
```
## **Referências**

- “Compilers: Principles, Techniques, and Tools” – Aho et al. (para estruturas de token)

- Documentação oficial do módulo re em Python

## **Estrutura do Projeto**
```bash

.
├── README.md
├── requirements.txt       
├── src/
│   └── lexer.py           # implementa o analisador léxico
└── tests/
    └── test_lexer.py      # casos de teste para lexer
```

### **No módulo lexer.py:**

- Definimos uma classe Token com atributos type e value.

- A função principal tokenize(text: str) -> List[Token] percorre a entrada e reconhece padrões:

  - Dígitos consecutivos formam NUMBER.

  - Cada símbolo de operador ou parêntese gera um token específico.

  - Espaços são ignorados.

### **Testes**

No diretório tests/, inclua casos como:

- Expressões válidas simples e complexas.

- Strings vazias ou apenas espaços.

- Expressões com erros (ex.: caractere inválido) — poderíamos lançar exceção LexerErro  

## **Bugs/Limitações/problemas conhecidos:**

- Não suporta floats nem variáveis.

- Não implementa recuperação de erros em tokens inválidos (lança exceção e encerra).


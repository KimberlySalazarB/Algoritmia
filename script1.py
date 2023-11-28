from antlr4 import *
from AlgoritmiaLexer import AlgoritmiaLexer  # Asumiendo que la gramática combinada se llama 'Algoritmia'
from AlgoritmiaParser import AlgoritmiaParser
from Visitor import CombinedVisitor  # Asegúrate de que esta sea la clase de Visitor combinada
import sys

input_stream = FileStream(sys.argv[1], encoding='utf-8')

# Usando el lexer y parser de la gramática combinada 'Algoritmia'
lexer = AlgoritmiaLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = AlgoritmiaParser(token_stream)

# Empieza el análisis sintáctico desde la regla 'program'
tree = parser.program()

# Usando el Visitor combinado para la gramática 'Algoritmia'
visitor = CombinedVisitor()
visitor.visit(tree)

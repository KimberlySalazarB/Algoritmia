from antlr4 import *
from AlgoritmiaLexer import AlgoritmiaLexer
from AlgoritmiaParser import AlgoritmiaParser
from Visitor import Visitor
import sys

# Asegúrate de que se proporciona un archivo de entrada
if len(sys.argv) < 2:
    print("Uso: python script.py <archivo_de_entrada>")
    sys.exit(1)

# Especificar la codificación UTF-8 para el FileStream
try:
    input_stream = FileStream(sys.argv[1], encoding='utf-8')
except UnicodeDecodeError as e:
    print(f"Error al leer el archivo: {e}")
    print("Asegúrate de que el archivo está en formato UTF-8.")
    sys.exit(1)

lexer = AlgoritmiaLexer(input_stream)
tokens = CommonTokenStream(lexer)
parser = AlgoritmiaParser(tokens)

# Empieza el análisis sintáctico desde la regla 'program'
tree = parser.program()

visitor = Visitor()
visitor.visit(tree)

# Generar archivo LilyPond después de visitar el árbol
visitor.generateLilyPondFile()

print("Archivo LilyPond generado con éxito.")

from antlr4 import *
from AlgoritmiaLexer import AlgoritmiaLexer
from AlgoritmiaParser import AlgoritmiaParser
from AlgoritmiaVisitor import AlgoritmiaVisitor
import sys


class Visitor(AlgoritmiaVisitor):
    def __init__(self):
        self.variables = {}
        self.musical_notes = []

    def visitMainStatement(self, ctx):
        print("Entering Hanoi Statement")
        return self.visitBlock(ctx.block())

    def visitHanoiStatement(self, ctx):
        # Obtener las listas 'src', 'dst' y 'aux' de las variables
        src = self.variables.get("src")
        dst = self.variables.get("dst")
        aux = self.variables.get("aux")

        # Asegurarse de que 'src' esté definido y obtener el número de discos (n) como su longitud
        if src is None:
            raise ValueError(
                "La lista 'src' no está definida en HanoiStatement")
        n = len(src)

    # Llamar a la función hanoi con n, src, dst y aux
        self.hanoi(n, src, dst, aux)

    def evaluateExpression(self, expr):
        if isinstance(expr, AlgoritmiaParser.ListListaContext):
            # Obtener la lista como string, ej. "{BCA}" o "{CDFG}"
            listAsString = expr.getText()
            listAsString = listAsString[1:-1]  # Eliminar las llaves
            # Determinar si la lista contiene comas
            if ',' in listAsString:
                # Separar por comas y eliminar espacios en blanco
                return [element.strip() for element in listAsString.split(',')]
            else:
                # Tratar cada carácter como un elemento separado
                return list(listAsString) if listAsString else []
        elif isinstance(expr, AlgoritmiaParser.VariableContext):
            var_name = expr.getText()
            var_value = self.variables.get(var_name)
            if var_value is not None:
                return var_value
            else:
                print(f"Variable '{var_name}' no definida")
                return None
        else:
            # Manejar directamente los nodos terminales para los enteros
            if expr.getChildCount() == 1 and isinstance(expr.getChild(0), TerminalNode):
                token = expr.getChild(0).getSymbol()
                if token.type == AlgoritmiaLexer.INTEGER:
                    return int(token.text)
            return self.visit(expr)

    def hanoi(self, n, src, dst, aux):
        # Asegurarse de que las listas no sean None
        src = src if src is not None else []
        dst = dst if dst is not None else []
        aux = aux if aux is not None else []

        if n > 0:
            # Utiliza copias de las listas
            self.hanoi(n - 1, src[:], aux[:], dst[:])

            if src:
                disco = src.pop()
                dst.append(disco)
                nota = self.getNoteForDisco(disco)
                if nota is not None:
                    self.musical_notes.append(nota)

            # Nuevamente, utiliza copias
            self.hanoi(n - 1, aux[:], dst[:], src[:])

    def getNoteForDisco(self, disco):
        # Asumiendo que 'disco' es una nota musical como 'C', 'D', etc.
        notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
        if disco.lower() in notes:
            return disco.lower()
        else:
            print(f"Valor de disco no válido: {disco}")
            return None

    def generateLilyPondFile(self):
        if not self.musical_notes:
            print("No se han generado notas musicales.")
            return

        lilypond_content = "\\version \"2.20.0\" \n"
        lilypond_content += "\\header { title = \"Torres de Hanoi\" }\n"
        lilypond_content += "\\score {\n"
        lilypond_content += "  \\new Staff \\relative c'{\n"
        lilypond_content += "    \\clef treble\n"
        lilypond_content += "    \\tempo 4=120\n"
        lilypond_content += "    \\time 4/4\n"
        lilypond_content += "    "

        first = False
        for note in self.musical_notes:
            if isinstance(note, str):
                if not first:
                        lilypond_content += note.lower() + " "  
                        first= True
                else:
                        lilypond_content += note.lower() + " "  
            else:
                print(f"Elemento no válido en self.musical_notes: {note}")

        lilypond_content += "\n  }\n"
        lilypond_content += "  \\layout { }\n"
        lilypond_content += "  \\midi { }\n"
        lilypond_content += "}\n"

        with open("hanoi_music.ly", "w") as file:
            file.write(lilypond_content)

        print("Archivo LilyPond generado: hanoi_music.ly")

    def visitAssignment(self, ctx):
        var_name = ctx.variable().getText()
        var_value = self.evaluateExpression(ctx.expression(0))
        self.variables[var_name] = var_value
        print(f"{var_name} asignado a {self.variables[var_name]}")

    def visitListLista(self, ctx):
        return [self.visitListElement(element) for element in ctx.listElement()]

    def visitListElement(self, ctx):
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()  # Retorna la nota musical como string
        elif ctx.INTEGER():
            return int(ctx.INTEGER().getText())

    # ...otros métodos...

    def visitConditional(self, ctx):
        condition = self.visit(ctx.expression())
        if condition:
            return self.visit(ctx.block(0))
        elif ctx.ELSE():
            return self.visit(ctx.block(1))

    def visitLoop(self, ctx):
        while self.visit(ctx.expression()):
            self.visit(ctx.block())

    def visitReproduction(self, ctx):
        notes = self.evaluateExpression(ctx.expression())
        print(f"Playing: {notes}")  # Agregado para depuración
        if isinstance(notes, list):
            for note in notes:
                self.addNote(note)
        else:
            self.addNote(notes)

    def addNote(self, note):
        if note in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            self.musical_notes.append(note)
        else:
            print(f"Elemento no válido en self.musical_notes: {note}")

    def visitWrite(self, ctx):
    	# Llamando al método que maneja el nodo 'printable' y obteniendo el texto
    	printable_text = self.visit(ctx.printable())
    	# Imprimiendo el texto para depuración
    	print(f"Printing: {printable_text}")
    	return printable_text

    def visitPrintable(self, ctx):
    # Esta implementación depende de cómo esté definido tu nodo 'printable'
    	if ctx.STRING():
         # Suponiendo que el nodo tiene un token STRING, extraer el texto
         # Eliminando las comillas si es una cadena de texto
            return ctx.STRING().getText()[1:-1]
    # Agrega aquí más condiciones si 'printable' puede contener otros tipos de nodos
    # ...


    def visitProcedureCall(self, ctx):
        # Implementación del llamado a procedimientos (si es necesario)
        pass

    def visitListOperations(self, ctx):
        list_name = ctx.variable(0).getText()
        if ctx.ADD_TO_LIST():
            element = self.visit(ctx.variable(1))
            self.variables[list_name].append(element)
        elif ctx.REMOVE_FROM_LIST():
            index = self.visit(ctx.expression()) - 1
            if index >= 0 and index < len(self.variables[list_name]):
                return self.variables[list_name].pop(index)

    def visitBlock(self, ctx):
        for statement in ctx.statement():
            print(f"Visiting statement: {statement.getText()}")
            self.visit(statement)




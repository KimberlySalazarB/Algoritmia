if __name__ is not None and "." in __name__:
    from .AlgoritmiaParser import AlgoritmiaParser
    from .AlgoritmiaVisitor import AlgoritmiaVisitor
else:
    from AlgoritmiaParser import AlgoritmiaParser
    from AlgoritmiaVisitor import AlgoritmiaVisitor

class CombinedVisitor(AlgoritmiaVisitor):
    def __init__(self):
        super().__init__()
        self.variables = {}

    def visitProgram(self, ctx):
        return self.visitMain(ctx.main())

    def visitMain(self, ctx):
        if ctx.NOMBRE():
            name = ctx.NOMBRE().getText()
            self.variables[name]= None
            if ctx.block():
                self.visitBlock(ctx.block())
            elif ctx.expr():
                values = [self.visitExpr(expr) for expr in ctx.expr()]
                
                self.visitChildren(ctx)
            if ctx.NOMBRE() and ctx.NOMBRE().getText() == "Hanoi":
                n = self.visit(ctx.expr(0))
                ori = self.visit(ctx.expr(1))
                dst = self.visit(ctx.expr(2))
                aux = self.visit(ctx.expr(3))
                
                self.solveHanoi(n,ori,dst,aux)
          
    def solveHanoi(self,n, ori, dst, aux):
        if n > 0:
       
            self.solveHanoi(n - 1, ori, aux, dst)
            if ori is not None and dst is not None:
                print(f"{ori} -> {dst}") 
            self.solveHanoi(n - 1, aux, dst, ori)
        
    def visitBlock(self, ctx):
        for instruction in ctx.instruction():
                self.visit(instruction)
        if ctx.main():
                return self.visitMain(ctx.main())
        return None

    def visitInstruction(self, ctx):
        return self.visitChildren(ctx)

 
    def visitWritestatement(self, ctx):
        if ctx.ASSIGNW():
            # Asegúrate de que hay dos expresiones disponibles
            if len(ctx.expr()) >= 2:
                var_name = self.visit(ctx.expr(0))
                var_value = self.visit(ctx.expr(1))
                # Solo imprime si ambos var_name y var_value no son None
                if var_name is not None and var_value is not None:
                    print(f"{var_name} -> {var_value}")
        else:
            expr_values = [self.visit(expr) for expr in ctx.expr() if self.visit(expr) is not None]
            print(" ".join(str(val) for val in expr_values))

    def visitReadStatement(self, ctx):
        var_name = ctx.VARIABLE().getText()
        value = int(input(f"Ingrese el valor de '{var_name}': "))
        self.variables[var_name] = value

    def visitAssignment(self, ctx):
        var_name = ctx.VARIABLE().getText()
        var_value = self.visit(ctx.expr())
        self.variables[var_name] = var_value

    def visitConditional(self, ctx):
        if self.visit(ctx.expr()):
            return self.visit(ctx.block(0))
        elif ctx.block(1):
            return self.visit(ctx.block(1))
        return None
        
            
    def visitWhileStatement(self, ctx):
        while self.visit(ctx.expr()):
            self.visit(ctx.block())

    def visitListOperation(self, ctx):
        return self.visitChildren(ctx)

    def visitListAddOperation(self, ctx):
        list_name = ctx.VARIABLE().getText()
        value = self.visit(ctx.expr())
        if list_name in self.variables:
            self.variables[list_name].append(value)
        else:
            self.variables[list_name] = [value]

    def validate_list_and_index(self, list_name, index):
        if list_name not in self.variables:
            print(f"Error: La lista '{list_name}' no está definida.")
            return False
        if not isinstance(index, int):
            print(f"Error: El índice '{index}' no es un número entero.")
            return False
        if not (0 <= index < len(self.variables[list_name])): 
            print(f"Error: Índice {index} fuera de rango para la lista '{list_name}'. Rango válido: 0 a {len(self.variables[list_name]) - 1}.")
            return False
        return True

    def visitListRemoveOperation(self, ctx):
        list_name = ctx.VARIABLE().getText()
        index = self.visit(ctx.exprWithinBrackets())
        if self.validate_list_and_index(list_name, index):
            del self.variables[list_name][index]

    def visitListRetrieveOperation(self, ctx):
        list_name = ctx.VARIABLE().getText()
        index = self.visit(ctx.exprWithinBrackets())
        if self.validate_list_and_index(list_name, index):
            return self.variables[list_name][index]
        return None

    def visitListLengthOperation(self, ctx):
        list_name = ctx.VARIABLE().getText()
        if list_name in self.variables:
            return len(self.variables[list_name])
        else:
            # Manejo de error si la lista no está definida
            print(f"Error: La lista '{list_name}' no está definida.")
            return None

    def visitExprWithinBrackets(self, ctx):
        return self.visit(ctx.expr())

    def visitListDefinition(self, ctx):
        elements = []
        if ctx.expr():
            for expr in ctx.expr():
                elements.append(self.visit(expr))
        return elements

    def visitExpr(self, ctx):
        if ctx.STRING():
            return ctx.STRING().getText()
        if ctx.NUMBER():
            return int(ctx.NUMBER().getText())
        if ctx.VARIABLE():
            var_name = ctx.VARIABLE().getText()
            return self.variables.get(var_name)
        if ctx.listDefinition():
            return self.visitListDefinition(ctx.listDefinition())
        if ctx.listLengthOperation():
            return self.visitListLengthOperation(ctx.listLengthOperation())
        if ctx.listRetrieveOperation():
            return self.visitListRetrieveOperation(ctx.listRetrieveOperation())
        if ctx.listAddOperation():
            return self.visitListAddOperation(ctx.listAddOperation())
        if ctx.MULTIPLY():
            return self.visit(ctx.expr(0)) * self.visit(ctx.expr(1))
        if ctx.DIVIDE():
            divisor = self.visit(ctx.expr(1))
            if divisor == 0:
                print("Error: División por cero.")
               
            else:
                return self.visit(ctx.expr(0)) / divisor
        if ctx.MODULO():
            return self.visit(ctx.expr(0)) % self.visit(ctx.expr(1))
        if ctx.PLUS():
            return self.visit(ctx.expr(0)) + self.visit(ctx.expr(1))
        if ctx.MINUS():
            return self.visit(ctx.expr(0)) - self.visit(ctx.expr(1))
        if ctx.EQ():
            return self.visit(ctx.expr(0)) == self.visit(ctx.expr(1))
        if ctx.NOT_EQUAL():
            return self.visit(ctx.expr(0)) != self.visit(ctx.expr(1))
        if ctx.MAYORIG():
            return self.visit(ctx.expr(0)) >= self.visit(ctx.expr(1))
        if ctx.MENORIG():
            return self.visit(ctx.expr(0)) <= self.visit(ctx.expr(1))
        if ctx.MAYOR():
            return self.visit(ctx.expr(0)) > self.visit(ctx.expr(1))
        if ctx.MENOR():
            return self.visit(ctx.expr(0)) < self.visit(ctx.expr(1))
        if ctx.LPAREN():
            inner_expr = self.visit(ctx.expr(0))
            return inner_expr
        

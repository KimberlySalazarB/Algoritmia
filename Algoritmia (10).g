grammar Algoritmia;

program         : statement+ EOF ;
statement       : mainStatement
                | hanoiStatement
                | assignment
                | conditional
                | loop
                | reproduction
                | write
                | procedureCall
                | listOperations
                | hanoiRecStatement ;

mainStatement   : IDENTIFIER  block ;
hanoiStatement  : IDENTIFIER expression+ (block)? ;
assignment      : variable ASSIGN expression+ ;
conditional     : IF expression block (ELSE block)?;
loop            : WHILE expression block ;
reproduction    : PLAY expression ;
write           : WRITE printable ;
procedureCall   : IDENTIFIER params ;
listOperations  : variable ADD_TO_LIST variable
                | REMOVE_FROM_LIST variable LBRACK expression RBRACK ;

hanoiRecStatement : IDENTIFIER expression+;

block           : PIPE_COLON statement+ COLON_PIPE ;
params          : LPAREN expressionList RPAREN ;
expressionList  : expression (COMMA expression)* ;
expression      : INTEGER
                | variable
                | LPAREN expression RPAREN
                | HASH expression 
                | LBRACK HASH expression RBRACK 
                | expression binaryOp expression
                | listElement
                | listLista ;

listElement     : IDENTIFIER | INTEGER ;
listLista       : LBRACE (listElement (COMMA listElement)*)? RBRACE ;
printable       : STRING | variable | listLista ;
variable        : IDENTIFIER ;

binaryOp        : PLUS | MINUS | MUL | DIV | LT | GT | EQ | NEQ ;
PLUS            : '+' ;
MINUS           : '-' ;
MUL             : '*' ;
DIV             : '/' ;
LT              : '<' ;
GT              : '>' ;
EQ              : '=' ;
NEQ             : '/=' ;
ASSIGN          : '<-' ;
ADD_TO_LIST     : '<<' ;
REMOVE_FROM_LIST: '8<' ;
IF              : 'if' ;
ELSE            : 'else' ;
WHILE           : 'while' ;
PLAY            : '(:)' ;
WRITE           : '<w>' ;
LPAREN          : '(' ;
RPAREN          : ')' ;
LBRACE          : '{' ;
RBRACE          : '}' ;
LBRACK          : '[' ;
RBRACK          : ']' ;
PIPE_COLON      : '|:' ;
COLON_PIPE      : ':|' ;
COMMA           : ',' ;
HASH            : '#' ;  // Se mantiene este token para '#'

IDENTIFIER      : [a-zA-Z_] [a-zA-Z_0-9]* ;
INTEGER         : [0-9]+ ;
STRING          : '"' (~["\r\n])* '"' ; 

WS              : [ \t\r\n]+ -> skip ;


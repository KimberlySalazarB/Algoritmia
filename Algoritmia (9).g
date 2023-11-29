grammar Algoritmia;

program: main EOF;

main: NOMBRE block (main)*
    | NOMBRE (expr)+ (OPEN_BLOCK instruction* CLOSE_BLOCK)*
    | NOMBRE (expr expr | expr)?
    ;

block: OPEN_BLOCK instruction* CLOSE_BLOCK (main)?;

instruction
    : writestatement
    | assignment
    | conditional
    | whileStatement
    | readStatement
    | listOperation
    | main
    ;

listOperation
    : listAddOperation
    | listRemoveOperation
    | listRetrieveOperation
    | listLengthOperation
    ;

listAddOperation: VARIABLE LISTADD expr;
listRemoveOperation: LISTREMOVE VARIABLE exprWithinBrackets;
listRetrieveOperation: VARIABLE exprWithinBrackets;
listLengthOperation: LISTLENGTH VARIABLE;
readStatement: READ (VARIABLE | expr);

exprWithinBrackets: '[' expr ']';

writestatement: WRITE (expr)+ (ASSIGNW expr)?;

assignment: VARIABLE ASSIGN expr;

conditional: IF expr block (ELSE block)? ;

whileStatement: WHILE expr block;


listDefinition: CORCHE (expr ( COMA expr)*)? CCORCHE;

expr
    : STRING
    | VARIABLE
    | NUMBER
    | listAddOperation
    | listDefinition
    | listLengthOperation
    | listRetrieveOperation
    | expr (MULTIPLY | DIVIDE | MODULO) expr
    | expr (MINUS | PLUS) expr
    | expr EQ expr
    | expr NOT_EQUAL expr
    | expr MAYORIG expr
    | expr MENORIG expr
    | expr MAYOR expr
    | expr MENOR expr
    | LPAREN expr RPAREN
    ;


WHILE: 'while';
OPEN_BLOCK: '|:';
CLOSE_BLOCK: ':|';
WRITE: '<w>';
READ: '<?>';
ASSIGN: '<-';
ASSIGNW: '"->"';
EQ: '=';
NOT_EQUAL: '/=';
IF: 'if';
ELSE: 'else';
PLUS: '+';
MINUS: '-';
CORCHE: '[';
CCORCHE: ']';
COMA: ',';
MULTIPLY: '*';
DIVIDE: '/';
MODULO: '%';
MAYOR: '>';
MAYORIG: '>=';
MENORIG: '<=';
MENOR: '<';
LPAREN: '(';
RPAREN: ')';
NUMBER: [0-9]+;
LISTADD: '<<' ;
LISTREMOVE: '8<';
LISTLENGTH: '#';
VARIABLE: [a-z][a-zA-Z0-9]*;
NOMBRE: [A-Z][a-z]+ ;
STRING: '"' (~["\r\n])* '"';
COMMENT: '###' .*? '###' -> skip;
WS: [ \t\n\r\f]+ -> skip;

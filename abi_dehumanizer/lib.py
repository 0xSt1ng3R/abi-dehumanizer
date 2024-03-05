class ABILexer:
    """
    A lexer for parsing human-readable ABI strings into a format that can be used with eth_abi.decode().
    """
    TERMINATORS = {'(', ')', '[', ']', ','}

    def __init__(self, abi_string):
        self.abi_string = abi_string
        self.current_position = 0
        self.lookahead_token = None

    @classmethod
    def is_terminator(cls, char):
        """
        Checks if a character is a terminator, which includes symbols and whitespace.
        """
        return char in cls.TERMINATORS or char.isspace()

    def peek(self):
        """
        Returns the next token without consuming it.
        """
        if self.lookahead_token is None:
            self.lookahead_token = self.next()
        return self.lookahead_token

    def next(self):
        """
        Returns the next token and advances the lexer's position.
        """
        if self.lookahead_token is not None:
            token = self.lookahead_token
            self.lookahead_token = None
            return token
        while self.current_position < len(self.abi_string) and self.abi_string[self.current_position].isspace():
            self.current_position += 1
        if self.current_position >= len(self.abi_string):
            return None
        if self.abi_string[self.current_position] in self.TERMINATORS:
            token = self.abi_string[self.current_position]
            self.current_position += 1
            return token
        start_position = self.current_position
        while self.current_position < len(self.abi_string) and not self.is_terminator(self.abi_string[self.current_position]):
            self.current_position += 1
        return self.abi_string[start_position:self.current_position]

class ABIParser:
    """
    A parser for transforming human-readable ABI strings into a format compatible with eth_abi.decode().
    """
    def __init__(self, abi_string):
        self.lexer = ABILexer(abi_string)
        self.ignore_function_name()

    def ignore_function_name(self):
        """
        Skips the function name in the ABI string until it finds an opening parenthesis.
        """
        token = self.lexer.next()
        while token and token not in {'(', None}:
            token = self.lexer.next()

    def parse(self):
        """
        Parses the parameter types from the ABI string.
        """
        if self.lexer.peek() == '(':
            self.lexer.next()  # Skip opening parenthesis
        return self.parse_parameters()

    def parse_parameters(self, end_token=')'):
        """
        Parses and returns a list of parameter types.
        """
        parameters = []
        token = self.lexer.peek()
        while token and token != end_token:
            if token == ',':
                self.lexer.next()  # Consume comma
            else:
                parameters.append(self.parse_parameter())
            token = self.lexer.peek()
        if token == end_token:
            self.lexer.next()  # Consume the end token ')'
        return parameters

    def parse_parameter(self):
        """
        Parses a single parameter, which could be a basic type or a tuple.
        """
        token = self.lexer.peek()
        if token == '(':
            return self.parse_tuple()
        elif token in {')', ',', None}:
            raise ValueError(f'Unexpected token "{token}"')
        else:
            return self.parse_type()

    def parse_tuple(self):
        """
        Parses a tuple parameter type.
        """
        self.lexer.next()  # Consume the opening '('
        tuple_params = self.parse_parameters(end_token=')')
        tuple_str = '(' + ','.join(tuple_params) + ')'
        if self.lexer.peek() == '[':
            self.lexer.next()  # Consume the '['
            if self.lexer.next() != ']':
                raise ValueError('Expected "]" after "[" to denote array type')
            tuple_str += '[]'
        return tuple_str

    def parse_type(self):
        """
        Parses a basic parameter type, possibly followed by array brackets.
        """
        param_type = self.lexer.next()  # Consume the type
        if self.lexer.peek() == '[':
            self.lexer.next()  # Consume the '['
            if self.lexer.next() != ']':
                raise ValueError('Expected "]" after "[" to denote array type')
            param_type += '[]'
        return param_type

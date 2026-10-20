import re

class Scanner:
    def __init__(self, token_file = "token.in", symbol_table = None):
        self.symbol_table = symbol_table
        self.keywords = set()
        self.operators = set()
        self.separators = set()

        self.load_tokens(token_file)

        self.token_pattern = re.compile(
            r"('[^']*')" 
            r"|(\b(?:0|-?[1-9][0-9]*)\b)"
            r"|(>=|<=|==|!=|>|<|=|\+|\-|\*|/)"
            r"|(;|\{|\}|:|,|\[|\]|\(|\)|\.)"
            r"|(\b[a-zA-Z][a-zA-Z0-9_]*\b)"
        )

    def load_tokens(self, token_file):
        with open(token_file, "r") as f:
            for line in f:
                token = line.strip()
                if not token:
                    continue
                if token in ["=", ">", "<", ">=", "<=", "==", "!=", "+", "-", "*", "/"]:
                    self.operators.add(token)
                elif token in [";", "{", "}", ":", ",", "[", "]", "(", ")", "."]:
                    self.separators.add(token)
                else:
                    self.keywords.add(token)

    def is_constant(self, token):
        return bool(re.fullmatch(r"'[^']*'|0|-?[1-9][0-9]*", token))

    def is_identifier(self, token):
        return bool(re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]*", token))

    def scan(self, file_path):
        pif = []
        errors = []

        with open(file_path, "r") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, start=1):
            column = 0
            while column < len(line):
                if line[column].isspace():
                    column += 1
                    continue

                match = self.token_pattern.match(line, column)
                if match:
                    token_str = match.group(0)
                    if token_str in self.keywords:
                        pif.append((token_str, (-1, -1)))

                    elif token_str in self.operators:
                        pif.append((token_str, (-1, -1)))

                    elif token_str in self.separators:
                        pif.append((token_str, (-1, -1)))

                    elif self.is_constant(token_str):
                        st_pos = self.symbol_table.insert(token_str)
                        pif.append(("CONST", st_pos))

                    elif self.is_identifier(token_str):
                        st_pos = self.symbol_table.insert(token_str)
                        pif.append(("ID", st_pos))

                    column = match.end()
                else:
                    invalid_char = line[column:].split()[0]
                    errors.append(
                        f"Lexical Error at Line {line_num}, Column {column + 1}: Unrecognized token starting with '{invalid_char}'"
                    )
                    column += len(invalid_char)
        return pif, errors
class FiniteAutomaton:
    def __init__(self, file_path = None):
        self.states = []
        self.alphabet = []
        self.initial_state = ""
        self.final_states = []
        self.transitions = {}

        if file_path:
            self.read_from_file(file_path)

    def read_from_file(self, file_path):
        lines = []
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            if line.startswith("Q:"):
                self.states = line.split(":", 1)[1].strip().split()
            elif line.startswith("Alphabet:"):
                self.alphabet = line.split(":", 1)[1].strip().split()
            elif line.startswith("Initial:"):
                self.initial_state = line.split(":", 1)[1].strip()
            elif line.startswith("Final:"):
                self.final_states = line.split(":", 1)[1].strip().split()
            else:
                parts = line.split()
                if len(parts) == 3:
                    from_state, symbol, to_state = parts
                    self.transitions[(from_state, symbol)] = to_state

    def _classify_char(self, char):
        if char == "0":
            return ["0", "digit"]
        elif char in "123456789":
            return ["non_zero_digit", "digit"]
        elif char == "-":
            return ["minus", "special_sign"]
        elif char.isalpha():
            return ["letter"]
        elif char in " _-:.":
            return ["special_sign"]
        return [char]

    def accepts(self, sequence):
        if not sequence:
            return self.initial_state in self.final_states

        current_state = self.initial_state

        for char in sequence:
            possible_symbols = self._classify_char(char) + [char]
            next_state = None

            for symbol in possible_symbols:
                if (current_state, symbol) in self.transitions:
                    next_state = self.transitions[(current_state, symbol)]
                    break

            if next_state is None:
                return False

            current_state = next_state

        return current_state in self.final_states

    def display(self):
        print("=" * 40)
        print("FINITE AUTOMATON DEFINITION")
        print("=" * 40)
        print(f"States (Q):          {', '.join(self.states)}")
        print(f"Alphabet (Sigma):   {', '.join(self.alphabet)}")
        print(f"Initial State (q0): {self.initial_state}")
        print(f"Final States (F):   {', '.join(self.final_states)}")
        print("\nTransitions:")
        print(f"{'From State':<12} | {'Symbol':<15} | {'To State':<12}")
        print("-" * 45)
        for (from_state, symbol), to_state in self.transitions.items():
            print(f"{from_state:<12} | {symbol:<15} | {to_state:<12}")
        print("=" * 40)
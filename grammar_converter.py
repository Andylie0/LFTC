class GrammarConverter:
    @staticmethod
    def fa_to_rg(fa):
        non_terminals = list(fa.states)
        terminals = list(fa.alphabet)
        start_symbol = fa.initial_state
        productions = {nt: [] for nt in non_terminals}

        if fa.initial_state in fa.final_states:
            productions[start_symbol].append("ε")

        for (q1, symbol), q2 in fa.transitions.items():
            rule_with_next_state = f"{symbol} {q2}"
            if rule_with_next_state not in productions[q1]:
                productions[q1].append(rule_with_next_state)

            if q2 in fa.final_states:
                if symbol not in productions[q1]:
                    productions[q1].append(symbol)
        return {
            "non_terminals": non_terminals,
            "terminals": terminals,
            "start_symbol": start_symbol,
            "productions": productions,
        }

    @staticmethod
    def display_rg(rg):
        print("=" * 40)
        print("REGULAR GRAMMAR (RG)")
        print("=" * 40)
        print(f"Non-Terminals (N): {', '.join(rg['non_terminals'])}")
        print(f"Terminals (T):     {', '.join(rg['terminals'])}")
        print(f"Start Symbol (S):  {rg['start_symbol']}")
        print("\nProduction Rules (P):")
        for nt, rhs_list in rg["productions"].items():
            if rhs_list:
                rhs_str = " | ".join(rhs_list)
                print(f"  {nt} -> {rhs_str}")
        print("=" * 40)

    @staticmethod
    def save_rg_to_file(rg, output_path):
        with open(output_path, "w") as f:
            f.write(f"N: {' '.join(rg['non_terminals'])}\n")
            f.write(f"T: {' '.join(rg['terminals'])}\n")
            f.write(f"S: {rg['start_symbol']}\n")
            f.write("P:\n")
            for nt, rhs_list in rg["productions"].items():
                if rhs_list:
                    rhs_str = " | ".join(rhs_list)
                    f.write(f"  {nt} -> {rhs_str}\n")

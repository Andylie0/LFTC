import os
from symbol_table import SymbolTable
from lexical_analysis import Scanner
from finite_automata import FiniteAutomaton
from grammar_converter import GrammarConverter

def run_pipeline(input_file, pif_out_path, st_out_path, err_out_path):
    st = SymbolTable(buckets=17)
    scanner = Scanner(token_file="inputs/token.in", symbol_table=st)

    pif,errors = scanner.scan(input_file)
    with open(pif_out_path, "w") as f:
        f.write(f"{'Token / Code':<20} | Position (Bucket, Index)\n")
        f.write("-" * 45 + "\n")
        for token, pos in pif:
            f.write(f"{token:<20} | {pos}\n")

    st.display(st_out_path)

    with open(err_out_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("Lexically correct - No errors found.\n")


def fa_menu():
    fa_files = {
        "1": ("Identifier FA", "inputs/fa_identifier.in"),
        "2": ("Integer FA", "inputs/fa_integer.in"),
        "3": ("String FA", "inputs/fa_string.in"),
    }

    loaded_fa = None
    loaded_name = ""

    while True:
        print("\n" + "=" * 45)
        print("              FA & RG MENU")
        print("=" * 45)
        print("1. Load Finite Automaton from file")
        print("2. Display FA elements (States, Alphabet, Transitions)")
        print("3. Verify if a sequence is accepted by FA")
        print("4. Convert current FA to Regular Grammar (RG)")
        print("5. Run Scanner Pipeline")
        print("0. Exit")
        print("=" * 45)

        choice = input("Select an option: ").strip()

        if choice == "1":
            print("\nAvailable Automata:")
            for key, (name, path) in fa_files.items():
                print(f"  {key}. {name} ({path})")
            sel = input("Choose file number: ").strip()
            if sel in fa_files:
                loaded_name, path = fa_files[sel]
                if os.path.exists(path):
                    loaded_fa = FiniteAutomaton(path)
                    print(f"\n[+] Successfully loaded {loaded_name} from '{path}'.")
                else:
                    print(f"\n[-] File '{path}' not found!")
            else:
                print("\n[-] Invalid selection!")

        elif choice == "2":
            if loaded_fa:
                print(f"\n--- {loaded_name} ---")
                loaded_fa.display()
            else:
                print("\n[-] Please load an FA first (Option 1).")

        elif choice == "3":
            if loaded_fa:
                seq = input("\nEnter sequence to verify: ").strip()
                is_accepted = loaded_fa.accepts(seq)
                if is_accepted:
                    print(f"\n[RESULT] Sequence '{seq}' is ACCEPTED by {loaded_name}.")
                else:
                    print(f"\n[RESULT] Sequence '{seq}' is REJECTED by {loaded_name}.")
            else:
                print("\n[-] Please load an FA first (Option 1).")

        elif choice == "4":
            if loaded_fa:
                rg = GrammarConverter.fa_to_rg(loaded_fa)
                GrammarConverter.display_rg(rg)

                safe_name = loaded_name.lower().replace(" ", "_")
                out_path = f"outputs/generated_rg_{safe_name}.out"
                GrammarConverter.save_rg_to_file(rg, out_path)
                print(f"\n[+] Regular Grammar successfully exported to '{out_path}'.")
            else:
                print("\n[-] Please load an FA first (Option 1).")

        elif choice == "5":
            print("\nExecuting Scanner pipeline for input programs...")
            run_pipeline(
                input_file="Utils/first_program.txt",
                pif_out_path="outputs/PIF1.out",
                st_out_path="outputs/ST1.out",
                err_out_path="outputs/LexicalErrors1.out"
            )
            run_pipeline(
                input_file="Utils/second_program.txt",
                pif_out_path="outputs/PIF2.out",
                st_out_path="outputs/ST2.out",
                err_out_path="outputs/LexicalErrors2.out"
            )
            print("[+] Scanner pipeline executed successfully. Check the 'outputs/' directory.")

        elif choice == "0":
            print("\nExiting program.")
            break
        else:
            print("\n[-] Invalid option! Please try again.")


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)

    fa_menu()
import os
from symbol_table import SymbolTable
from lexical_analysis import Scanner

def run_pipeline(input_file, pif_out_path, st_out_path, err_out_path):
    st = SymbolTable(buckets=17)
    scanner = Scanner(token_file="token.in", symbol_table=st)

    pif,errors = scanner.scan(input_file)
    with open(pif_out_path, "w") as f:
        f.write(f"{'Token / Code':<20} | Position (Bucket, Index)\n")
        f.write("-" * 45 + "\n")
        for token, pos in pif:
            f.write(f"{token:<20} | {pos}\n")

    st.display()

    with open(err_out_path, "w") as f:
        if errors:
            for err in errors:
                f.write(err + "\n")
        else:
            f.write("Lexically correct - No errors found.\n")


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)

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
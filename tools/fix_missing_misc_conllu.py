"""
Makes the CONLL files CONLL-U friendly.
"""

import sys

def make_conllu_friendly(file_path):
    with open(file_path) as f, open(file_path + ".conllu", "w") as w:
        for line in f:
            if line.strip() != "":
                w.write(line.rstrip() + "\t_\n")
            else:
                w.write(line)


if __name__ == "__main__":
    make_conllu_friendly(sys.argv[1])

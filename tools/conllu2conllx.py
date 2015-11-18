import udtree
from os.path import join

project_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/resources/universaldependencies1-1/ud-treebanks-v1.1"

def convert(to_convert_files):
    for lang, files in to_convert_files.items():
        outfile = join(project_base, lang, files[0].split(".")[0] + ".conllx")
        trees = udtree.from_files([join(project_base, lang, path) for path in files])
        with open (outfile, "w") as w:
            for tree in trees:
                if not any(tree.postags):
                    print("Found for {}".format(lang))
                    tree.postags = tree.cpostags
                w.write("\n".join(tree.to_conllx_format()) + "\n\n")

train_files = {'UD_Basque': ['eu-ud-train.conllu'],
               'UD_Croatian': ['hr-ud-train.conllu'],
               'UD_Danish': ['da-ud-train.conllu'],
               'UD_Finnish': ['fi-ud-train.conllu'],
               'UD_French': ['fr-ud-train.conllu'],
               'UD_Greek': ['el-ud-train.conllu'],
               'UD_Hungarian': ['hu-ud-train.conllu'],
               'UD_Irish': ['ga-ud-train.conllu'],
               'UD_Persian': ['fa-ud-train.conllu'],
               'UD_Swedish': ['sv-ud-train.conllu'],
               'UD_Bulgarian': ['bg-ud-train.conllu'],
               'UD_Czech': ['cs-ud-train-c.conllu',
                            'cs-ud-train-m.conllu',
                            'cs-ud-train-v.conllu',
                            'cs-ud-train-l.conllu'],
               'UD_English': ['en-ud-train.conllu'],
               'UD_Finnish-FTB': ['fi_ftb-ud-train.conllu'],
               'UD_German': ['de-ud-train.conllu'],
               'UD_Hebrew': ['he-ud-train.conllu'],
               'UD_Indonesian': ['id-ud-train.conllu'],
               'UD_Italian': ['it-ud-train.conllu'],
               'UD_Spanish': ['es-ud-train.conllu']}

test_files = {'UD_Basque': ['eu-ud-test.conllu'],
               'UD_Croatian': ['hr-ud-test.conllu'],
               'UD_Danish': ['da-ud-test.conllu'],
               'UD_Finnish': ['fi-ud-test.conllu'],
               'UD_French': ['fr-ud-test.conllu'],
               'UD_Greek': ['el-ud-test.conllu'],
               'UD_Hungarian': ['hu-ud-test.conllu'],
               'UD_Irish': ['ga-ud-test.conllu'],
               'UD_Persian': ['fa-ud-test.conllu'],
               'UD_Swedish': ['sv-ud-test.conllu'],
               'UD_Bulgarian': ['bg-ud-test.conllu'],
               'UD_Czech': ['cs-ud-test.conllu'],
               'UD_English': ['en-ud-test.conllu'],
               'UD_Finnish-FTB': ['fi_ftb-ud-test.conllu'],
               'UD_German': ['de-ud-test.conllu'],
               'UD_Hebrew': ['he-ud-test.conllu'],
               'UD_Indonesian': ['id-ud-test.conllu'],
               'UD_Italian': ['it-ud-test.conllu'],
               'UD_Spanish': ['es-ud-test.conllu']}

convert(train_files)
convert(test_files)

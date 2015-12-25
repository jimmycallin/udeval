import udtree
from os.path import join
import lang_utils

# change this if you only want coarse grained dependency relations
fine_grained_deprels = False

project_base = "/home/stp11/kanin/udeval/resources/universaldependencies1-2/universal-dependencies-1.2/"

def convert(to_convert_files):
    for lang, files in to_convert_files.items():
        file_ending = ".conllx"
        if not fine_grained_deprels:
            file_ending = ".coarse_deprels.conllx"
        if lang == "UD_Czech" and len(files) > 1:
            file_name = "cs-ud-train" + file_ending
        else:
            file_name = files[0].split("/")[-1].split(".")[0] + file_ending

        outfile = join(project_base, "UD_" + lang, file_name)
        trees = udtree.from_files(files)
        with open (outfile, "w") as w:
            for tree in trees:
                for word in tree.sentence_structure:
                    word['deps'] = None
                    word['misc'] = None
                if not any(tree.postags):  # Copy CPOSTAG to POSTAG
                    tree.postags = tree.cpostags
                w.write("\n".join(tree.to_conllx_format(fine_grained_deprels=fine_grained_deprels)) + "\n\n")


train_files = lang_utils.get_ud_paths(project_base, type_="train", format_="conllu", coarse=False)
dev_files = lang_utils.get_ud_paths(project_base, type_="dev", format_="conllu", coarse=False)
test_files = lang_utils.get_ud_paths(project_base, type_="test", format_="conllu", coarse=False)

convert(train_files)
convert(dev_files)
convert(test_files)

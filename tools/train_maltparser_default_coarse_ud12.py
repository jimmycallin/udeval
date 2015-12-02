#!/usr/local/bin/python3
# TODO: Convert conll-u to conll-x and then back again

# To run MaltOptimizer, you have to be in the MaltOptimizer directory:
# cd {project_base}/tools/MaltOptimizer-1.0.3
# ~/dev/miniconda/bin/python3 ../train_maltparser.py

from subprocess import call
from os.path import join
from os import rename
import lang_utils

treebank_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/resources/universaldependencies1-2/universal-dependencies-1.2/"
train_files = lang_utils.get_ud_paths(treebank_base, type_="train", format_="conllx", coarse=True)
project_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/"

maltparser_path = join(project_base, "tools",
                       "maltparser-1.8.1", "maltparser-1.8.1.jar")
maltoptimizer_path = join(project_base, "tools", "MaltOptimizer-1.0.3", "MaltOptimizer.jar")

base_cmd = ["java", "-Xmx8G"]  # 8G is only necessary for Czech
jar_path = ["-jar", maltparser_path]
mode = ["-m", "learn"]

for lang, train_file in train_files.items():
    print("Training language {}".format(lang))
    training_path = ["-i", train_file[0]]
    model_path = ["-c", "ud-1.2." + lang]
    call(base_cmd + jar_path + ["-grl", "root"] + model_path + mode + training_path)

    # Move model file to resources
    rename(model_path[1] + ".mco", join(project_base, "resources", "maltdefault_coarse_models_1-2", model_path[1] + ".mco"))

# java -jar maltparser-1.8.1.jar -c es-model -m learn -i ../../resources/universaldependencies1-1/ud-treebanks-v1.1/UD_Spanish/es-ud-dev.conllx

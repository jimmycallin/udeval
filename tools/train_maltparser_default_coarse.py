#!/usr/local/bin/python3
# TODO: Convert conll-u to conll-x and then back again

# To run MaltOptimizer, you have to be in the MaltOptimizer directory:
# cd {project_base}/tools/MaltOptimizer-1.0.3
# ~/dev/miniconda/bin/python3 ../train_maltparser.py

from subprocess import call
from os.path import join
from os import rename

train_files = {
               'UD_Basque': 'eu-ud-train.coarse_deprels.conllx',
               'UD_Croatian': 'hr-ud-train.coarse_deprels.conllx',
               'UD_Danish': 'da-ud-train.coarse_deprels.conllx',
               'UD_Finnish': 'fi-ud-train.coarse_deprels.conllx',
               'UD_French': 'fr-ud-train.coarse_deprels.conllx',
               'UD_Greek': 'el-ud-train.coarse_deprels.conllx',
               'UD_Hungarian': 'hu-ud-train.coarse_deprels.conllx',
               'UD_Irish': 'ga-ud-train.coarse_deprels.conllx',
               'UD_Persian': 'fa-ud-train.coarse_deprels.conllx',
               'UD_Swedish': 'sv-ud-train.coarse_deprels.conllx',
               'UD_Bulgarian': 'bg-ud-train.coarse_deprels.conllx',
               'UD_Czech': 'cs-ud-train.coarse_deprels.conllx',
               'UD_English': 'en-ud-train.coarse_deprels.conllx',
               'UD_Finnish-FTB': 'fi_ftb-ud-train.coarse_deprels.conllx',
               'UD_German': 'de-ud-train.coarse_deprels.conllx',
               'UD_Hebrew': 'he-ud-train.coarse_deprels.conllx',
               'UD_Indonesian': 'id-ud-train.coarse_deprels.conllx',
               'UD_Italian': 'it-ud-train.coarse_deprels.conllx',
               'UD_Spanish': 'es-ud-train.coarse_deprels.conllx'
               }

project_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/"

maltparser_path = join(project_base, "tools",
                       "maltparser-1.8.1", "maltparser-1.8.1.jar")
maltoptimizer_path = join(project_base, "tools", "MaltOptimizer-1.0.3", "MaltOptimizer.jar")

base_cmd = ["java", "-Xmx8G"]  # 8G is only necessary for Czech
jar_path = ["-jar", maltparser_path]
mode = ["-m", "learn"]

for lang, train_file in train_files.items():
    print("Training language {}".format(lang))
    training_path = ["-i", join(project_base, "resources", "universaldependencies1-1", "ud-treebanks-v1.1", lang, train_file)]
    model_path = ["-c", "ud-1.1." + lang]
    call(base_cmd + jar_path + model_path + mode + training_path)

    # Move model file to resources
    rename(model_path[1] + ".mco", join(project_base, "resources", "maltdefault_coarse_models", model_path[1] + ".mco"))

# java -jar maltparser-1.8.1.jar -c es-model -m learn -i ../../resources/universaldependencies1-1/ud-treebanks-v1.1/UD_Spanish/es-ud-dev.conllx

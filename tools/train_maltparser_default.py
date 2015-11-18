#!/usr/local/bin/python3
# TODO: Convert conll-u to conll-x and then back again

# To run MaltOptimizer, you have to be in the MaltOptimizer directory:
# cd {project_base}/tools/MaltOptimizer-1.0.3
# ~/dev/miniconda/bin/python3 ../train_maltparser.py

from subprocess import call
from os.path import join
from os import rename

train_files = {'UD_Basque': 'eu-ud-train.conllx',
               'UD_Croatian': 'hr-ud-train.conllx',
               'UD_Danish': 'da-ud-train.conllx',
               'UD_Finnish': 'fi-ud-train.conllx',
               'UD_French': 'fr-ud-train.conllx',
               'UD_Greek': 'el-ud-train.conllx',
               'UD_Hungarian': 'hu-ud-train.conllx',
               'UD_Irish': 'ga-ud-train.conllx',
               'UD_Persian': 'fa-ud-train.conllx',
               'UD_Swedish': 'sv-ud-train.conllx',
               'UD_Bulgarian': 'bg-ud-train.conllx',
               'UD_Czech': 'cs-ud-train.conllx',
               'UD_English': 'en-ud-train.conllx',
               'UD_Finnish-FTB': 'fi_ftb-ud-train.conllx',
               'UD_German': 'de-ud-train.conllx',
               'UD_Hebrew': 'he-ud-train.conllx',
               'UD_Indonesian': 'id-ud-train.conllx',
               'UD_Italian': 'it-ud-train.conllx',
               'UD_Spanish': 'es-ud-train.conllx'}

project_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/"

maltparser_path = join(project_base, "tools",
                       "maltparser-1.8.1", "maltparser-1.8.1.jar")
maltoptimizer_path = join(project_base, "tools", "MaltOptimizer-1.0.3", "MaltOptimizer.jar")
optimized_config_base = join(project_base, "resources", "maltopt_configs")

base_cmd = ["java", "-Xmx8G"]
jar_path = ["-jar", maltparser_path]
mode = ["-m", "learn"]

def optimize_model(lang, train_file):
    call(["java", "-jar", maltoptimizer_path, "-p", "1", "-m", maltparser_path, "-c", train_file])
    call(["java", "-jar", maltoptimizer_path, "-p", "2", "-m", maltparser_path, "-c", train_file])
    call(["java", "-jar", maltoptimizer_path, "-p", "3", "-m", maltparser_path, "-c", train_file])
    rename("finalOptionsFile.xml", join(project_base, "resources", "maltopt_configs", lang + "_finalOptionsFile.xml"))

for lang, train_file in train_files.items():
    print("Optimizing language {}".format(lang))
    # optimize_model(lang, join(project_base, "resources", "universaldependencies1-1", "ud-treebanks-v1.1", lang, train_file))
    print("Training language {}".format(lang))
    training_path = ["-i", join(project_base, "resources", "universaldependencies1-1",
                               "ud-treebanks-v1.1", lang, train_file)]
    model_path = ["-c", "ud-1.1." + lang]
    call(base_cmd + jar_path + model_path + mode + training_path)

    # Move model file to resources
    rename(model_path[1] + ".mco", join(project_base, "resources", "maltdefault_models", model_path[1] + ".mco"))


# java -jar maltparser-1.8.1.jar -c es-model -m learn -i ../../resources/universaldependencies1-1/ud-treebanks-v1.1/UD_Spanish/es-ud-dev.conllx

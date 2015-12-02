# TODO: Convert conll-u to conll-x and then back again

from subprocess import call
from os.path import join
from os import remove
from shutil import copyfile
import lang_utils

project_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/"
treebank_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/resources/universaldependencies1-2/universal-dependencies-1.2/"
test_files = lang_utils.get_ud_paths(treebank_base, type_="test", format_="conllx")
maltparser_path = join(project_base, "tools",
                       "maltparser-1.8.1", "maltparser-1.8.1.jar")

base_cmd = ["java", "-Xmx8G"]
jar_path = ["-jar", maltparser_path]
mode = ["-m", "parse"]

for lang, test_file in test_files.items():
    # Get language's parsing model
    print("Parsing {} from {}".format(lang, test_file))
    model_path = ["-c", "ud-1.2." + lang]
    copyfile(join(project_base, "resources", "maltdefault_models_1-2", model_path[1] + ".mco"), model_path[1] + ".mco")
    test_path = ["-i", join(treebank_base, lang, test_file[0])]
    output_path = ["-o", join(project_base, "resources", "maltdefault_output_1-2", lang + ".conllx")]
    call(base_cmd + jar_path + model_path + mode + test_path + output_path)
    remove(model_path[1] + ".mco")

# java -jar maltparser-1.8.1.jar -c es-model -m learn -i ../../resources/universaldependencies1-1/ud-treebanks-v1.1/UD_Spanish/es-ud-dev.conllx

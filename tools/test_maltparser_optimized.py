# TODO: Convert conll-u to conll-x and then back again

from subprocess import call
from os.path import join
from os import remove
from shutil import copyfile

test_files = {'UD_Basque': 'eu-ud-dev.conllx',
               'UD_Croatian': 'hr-ud-dev.conllx',
               'UD_Danish': 'da-ud-dev.conllx',
               'UD_Finnish': 'fi-ud-dev.conllx',
               'UD_French': 'fr-ud-dev.conllx',
               'UD_Greek': 'el-ud-dev.conllx',
               'UD_Hungarian': 'hu-ud-dev.conllx',
               'UD_Irish': 'ga-ud-dev.conllx',
               'UD_Persian': 'fa-ud-dev.conllx',
               'UD_Swedish': 'sv-ud-dev.conllx',
               'UD_Bulgarian': 'bg-ud-dev.conllx',
               'UD_Czech': 'cs-ud-dev.conllx',
               'UD_English': 'en-ud-dev.conllx',
               'UD_Finnish-FTB': 'fi_ftb-ud-dev.conllx',
               'UD_German': 'de-ud-dev.conllx',
               'UD_Hebrew': 'he-ud-dev.conllx',
               'UD_Indonesian': 'id-ud-dev.conllx',
               'UD_Italian': 'it-ud-dev.conllx',
               'UD_Spanish': 'es-ud-dev.conllx'}

project_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/"

maltparser_path = join(project_base, "tools",
                       "maltparser-1.8.1", "maltparser-1.8.1.jar")

base_cmd = ["java", "-Xmx8G"]
jar_path = ["-jar", maltparser_path]
mode = ["-m", "parse"]

for lang, test_file in test_files.items():
    # Get language's parsing model
    model_path = ["-c", "ud-1.1." + lang]
    copyfile(join(project_base, "resources", "maltopt_models", model_path[1] + ".mco"), model_path[1] + ".mco")
    test_path = ["-i", join(project_base, "resources", "universaldependencies1-1", "ud-treebanks-v1.1", lang, test_file)]
    output_path = ["-o", join(project_base, "resources", "maltopt_output", lang + ".conllx")]
    call(base_cmd + jar_path + model_path + mode + test_path + output_path)
    remove(model_path[1] + ".mco")

# java -jar maltparser-1.8.1.jar -c es-model -m learn -i ../../resources/universaldependencies1-1/ud-treebanks-v1.1/UD_Spanish/es-ud-dev.conllx

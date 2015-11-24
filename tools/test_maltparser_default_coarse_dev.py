# TODO: Convert conll-u to conll-x and then back again

from subprocess import call
from os.path import join
from os import remove
from shutil import copyfile

test_files = {
               'UD_Basque': 'eu-ud-dev.coarse_deprels.conllx',
               'UD_Croatian': 'hr-ud-dev.coarse_deprels.conllx',
               'UD_Danish': 'da-ud-dev.coarse_deprels.conllx',
               'UD_Finnish': 'fi-ud-dev.coarse_deprels.conllx',
               'UD_French': 'fr-ud-dev.coarse_deprels.conllx',
               'UD_Greek': 'el-ud-dev.coarse_deprels.conllx',
               'UD_Hungarian': 'hu-ud-dev.coarse_deprels.conllx',
               'UD_Irish': 'ga-ud-dev.coarse_deprels.conllx',
               'UD_Persian': 'fa-ud-dev.coarse_deprels.conllx',
               'UD_Swedish': 'sv-ud-dev.coarse_deprels.conllx',
               'UD_Bulgarian': 'bg-ud-dev.coarse_deprels.conllx',
               'UD_Czech': 'cs-ud-dev.coarse_deprels.conllx',
               'UD_English': 'en-ud-dev.coarse_deprels.conllx',
               'UD_Finnish-FTB': 'fi_ftb-ud-dev.coarse_deprels.conllx',
               'UD_German': 'de-ud-dev.coarse_deprels.conllx',
               'UD_Hebrew': 'he-ud-dev.coarse_deprels.conllx',
               'UD_Indonesian': 'id-ud-dev.coarse_deprels.conllx',
               'UD_Italian': 'it-ud-dev.coarse_deprels.conllx',
               'UD_Spanish': 'es-ud-dev.coarse_deprels.conllx'
               }

project_base = "/Users/jimmy/dev/edu/nlp-rod/udeval/"

maltparser_path = join(project_base, "tools",
                       "maltparser-1.8.1", "maltparser-1.8.1.jar")

base_cmd = ["java", "-Xmx8G"]
jar_path = ["-jar", maltparser_path]
mode = ["-m", "parse"]

for lang, test_file in test_files.items():
    # Get language's parsing model
    model_path = ["-c", "ud-1.1." + lang]
    copyfile(join(project_base, "resources", "maltdefault_coarse_models", model_path[1] + ".mco"), model_path[1] + ".mco")
    test_path = ["-i", join(project_base, "resources", "universaldependencies1-1", "ud-treebanks-v1.1", lang, test_file)]
    output_path = ["-o", join(project_base, "resources", "maltdefault_coarse_output_dev", lang + ".conllx")]
    call(base_cmd + jar_path + model_path + mode + test_path + output_path)
    remove(model_path[1] + ".mco")

# java -jar maltparser-1.8.1.jar -c es-model -m learn -i ../../resources/universaldependencies1-1/ud-treebanks-v1.1/UD_Spanish/es-ud-dev.conllx

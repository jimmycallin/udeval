#!/usr/local/bin/python3
# TODO: Convert conll-u to conll-x and then back again

# To run MaltOptimizer, you have to be in the MaltOptimizer directory:
# cd {project_base}/tools/MaltOptimizer-1.0.3
# ~/dev/miniconda/bin/python3 ../train_maltparser.py

from subprocess import call
from os.path import join
from os import rename
import lang_utils
import smtplib

treebank_base = "/home/stp11/kanin/udeval/resources/universaldependencies1-2/universal-dependencies-1.2/"
train_files = lang_utils.get_ud_paths(treebank_base, type_="train", format_="conllx", coarse=True)
project_base = "/home/stp11/kanin/udeval/"

maltparser_path = join(project_base, "tools",
                       "maltparser-1.8.1", "maltparser-1.8.1.jar")
maltoptimizer_path = join(project_base, "tools", "MaltOptimizer-1.0.3", "MaltOptimizer.jar")
optimized_config_base = join(project_base, "resources", "maltopt_configs_1-2")

base_cmd = ["java", "-Xmx8G"]
jar_path = ["-jar", maltparser_path]
mode = ["-m", "learn"]

def get_feature_model(filepath):
    with open(filepath) as f:
        feat_model = None
        for line in f:
            if "feature_model (-F)" in line:
                feat_model = line.split(":")[1].strip()
        if not feat_model:
            raise ValueError
    return feat_model


def optimize_model(lang, train_file):
    call(["java", "-jar", maltoptimizer_path, "-p", "1", "-m", maltparser_path, "-c", train_file, "-e", "las", "-s", "false"])
    call(["java", "-jar", maltoptimizer_path, "-p", "2", "-m", maltparser_path, "-c", train_file, "-e", "las", "-s", "false"])
    call(["java", "-jar", maltoptimizer_path, "-p", "3", "-m", maltparser_path, "-c", train_file, "-e", "las", "-s", "false"])
    feature_model = get_feature_model("phase3_optFile.txt")
    rename("finalOptionsFile.xml", join(project_base, "resources", "maltopt_configs_1-2", lang + "_finalOptionsFile.xml"))
    rename("phase1_logFile.txt", join(project_base, "resources", "maltopt_configs_1-2", lang + "_phase1_logFile.txt"))
    rename("phase3_logFile.txt", join(project_base, "resources", "maltopt_configs_1-2", lang + "_phase3_logFile.txt"))
    rename("phase3_optFile.txt", join(project_base, "resources", "maltopt_configs_1-2", lang + "_phase3_optFile.txt"))
    rename(feature_model, join(project_base, "resources", "maltopt_configs_1-2", lang + "_finalFeatureModel.xml"))

for lang, train_file in train_files.items():
    print(train_file)
    train_file = train_file[0]
    print("Optimizing language {}".format(lang))
    optimize_model(lang, train_file)
    print("Training language {}".format(lang))
    training_path = ["-i", train_file]
    optimized_config = ["-f", join(project_base, "resources", "maltopt_configs_1-2", lang + "_finalOptionsFile.xml"),
                        "-F", join(project_base, "resources", "maltopt_configs_1-2", lang + "_finalFeatureModel.xml")]
    model_path = ["-c", "ud-1.2." + lang]
    call(base_cmd + jar_path + ["-grl", "root"] + model_path + optimized_config + mode + training_path)

    # Move model file to resources
    rename(model_path[1] + ".mco", join(project_base, "resources", "maltopt_models_1-2", model_path[1] + ".mco"))

    s = smtplib.SMTP('localhost')
    s.sendmail('kanin@stp.lingfil.uu.se', 'jimmy.callin@gmail.com', "Subject: {} done".format(lang))
    s.quit()

s.sendmail('kanin@stp.lingfil.uu.se', 'jimmy.callin@gmail.com', "Subject: ALL DONE")

# java -jar MaltOptimizer.jar -p 1 -m ../maltparser-1.8.1/maltparser-1.8.1.jar -c /Users/jimmy/dev/edu/nlp-rod/udeval/resources/universaldependencies1-1/ud-treebanks-v1.1/UD_English/en-ud-train.conllx
# java -jar maltparser-1.8.1.jar -c es-model -m learn -i ../../resources/universaldependencies1-1/ud-treebanks-v1.1/UD_Spanish/es-ud-dev.conllx

from os import listdir
from os.path import join

ignore = {"Ancient_Greek", "German", "Ancient_Greek-PROIEL", "Estonian",
          "Finnish-FTB", "French", "German", "Hungarian", "Indonesian",
          "Irish", "Japanese-KTC", "Latin", "Latin-ITT", "Latin-PROIEL",
          "Romanian", "Tamil", "Basque", "Dutch",
"Bulgarian",
"Danish",
"Polish",
"Spanish",
"Czech",
"Finnish",
"Portuguese",
"Swedish",
"Czech"}

udname2lang =  {"UD_Ancient_Greek": "Ancient_Greek",
                "UD_Danish": "Danish",
                "UD_German": "German",
                "UD_Irish": "Irish",
                "UD_Old_Church_Slavonic": "Old_Church_Slavonic",
                "UD_Ancient_Greek-PROIEL": "Ancient_Greek-PROIEL",
                "UD_Dutch": "Dutch",
                "UD_Gothic": "Gothic",
                "UD_Italian": "Italian",
                "UD_Persian": "Persian",
                "UD_Arabic": "Arabic",
                "UD_English": "English",
                "UD_Greek": "Greek",
                "UD_Japanese-KTC": "Japanese-KTC",
                "UD_Basque": "Basque",
                "UD_Estonian": "Estonian",
                "UD_Hebrew": "Hebrew",
                "UD_Latin": "Latin",
                "UD_Bulgarian": "Bulgarian",
                "UD_Finnish": "Finnish",
                "UD_Hindi": "Hindi",
                "UD_Latin-ITT": "Latin-ITT",
                "UD_Croatian": "Croatian",
                "UD_Finnish-FTB": "Finnish-FTB",
                "UD_Hungarian": "Hungarian",
                "UD_Latin-PROIEL": "Latin-PROIEL",
                "UD_Czech": "Czech",
                "UD_French": "French",
                "UD_Indonesian": "Indonesian",
                "UD_Norwegian": "Norwegian",
                "UD_Portuguese": "Portuguese",
                "UD_Polish": "Polish",
                "UD_Romanian": "Romanian",
                "UD_Slovenian": "Slovenian",
                "UD_Tamil": "Tamil",
                "UD_Spanish": "Spanish",
                "UD_Swedish": "Swedish"}

lang2udname = {y: x for x,y in udname2lang.items()}

lang2code = {"Ancient_Greek": "grc",
             "Ancient_Greek-PROIEL": "grc_proiel",
             "Old_Church_Slavonic": "cu",
             "Gothic": "got",
             "Arabic": "ar",
             "Japanese-KTC": "ja_ktc",
             "Latin": "la",
             "Hindi": "hi",
             "Latin-ITT": "la_itt",
             "Latin-PROIEL": "la_proiel",
             "Norwegian": "no",
             "Dutch": "nl",
             "Estonian": "et",
             "Basque": "eu",
             "Croatian": "hr",
             "Danish": "da",
             "Finnish": "fi",
             "French": "fr",
             "Greek": "el",
             "Hungarian": "hu",
             "Irish": "ga",
             "Persian": "fa",
             "Swedish": "sv",
             "Bulgarian": "bg",
             "Czech": "cs",
             "English": "en",
             "Finnish-FTB": "fi_ftb",
             "German": "de",
             "Hebrew": "he",
             "Indonesian": "id",
             "Italian": "it",
             "Spanish": "es",
             "Portuguese": "pt",
             "Polish": "pl",
             "Romanian": "ro",
             "Slovenian": "sl",
             "Tamil": "ta"
             }

code2lang = {y: x for x,y in lang2code.items()}

def get_ud_paths(base_path, type_, format_, coarse):
    assert type_ in {'dev', 'train', 'test'}
    assert format_ in {'conllu', 'conllx'}
    treebanks = [tb for tb in listdir(base_path) if not tb.startswith(".") and udname2lang[tb] not in ignore]
    coarse_grained_path = ""
    if coarse:
        coarse_grained_path = ".coarse_deprels"
    path_format = lambda tb: join(base_path, tb, "{}-ud-{}{}.{}".format(lang2code[udname2lang[tb]], type_, coarse_grained_path, format_))
    tb_paths = {udname2lang[lang]: [path_format(lang)] for lang in treebanks}
    # this is such a hack, but i don't have time to do it correctly right now
    if format_ == "conllu" and type_ == "train":
        tb_paths["Czech"] = [join(base_path, "UD_Czech", f) for f in ['cs-ud-train-c.conllu',
                                                                      'cs-ud-train-m.conllu',
                                                                      'cs-ud-train-v.conllu',
                                                                      'cs-ud-train-l.conllu']]
    return tb_paths

def get_system_output_paths(base_path, type_, format_):
    assert type_ in {'dev', 'test'}
    assert format_ in {'conllu', 'conllx'}
    treebanks = [tb for tb in listdir(base_path) if not tb.startswith(".") and tb.endswith(format_) and tb.split(".")[0] not in ignore]
    return {lang.split(".")[0]: join(base_path, lang) for lang in treebanks}

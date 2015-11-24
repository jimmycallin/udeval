from os import listdir
from os.path import join

udname2lang = {"UD_Basque": "Basque",
               "UD_Croatian": "Croatian",
               "UD_Danish": "Danish",
               "UD_Finnish": "Finnish",
               "UD_French": "French",
               "UD_Greek": "Greek",
               "UD_Hungarian": "Hungarian",
               "UD_Irish": "Irish",
               "UD_Persian": "Persian",
               "UD_Swedish": "Swedish",
               "UD_Bulgarian": "Bulgarian",
               "UD_Czech": "Czech",
               "UD_English": "English",
               "UD_Finnish-FTB": "Finnish-FTB",
               "UD_German": "German",
               "UD_Hebrew": "Hebrew",
               "UD_Indonesian": "Indonesian",
               "UD_Italian": "Italian",
               "UD_Spanish": "Spanish"}

lang2udname = {y: x for x,y in udname2lang.items()}

lang2code = {"Basque": "eu",
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
             "Spanish": "es"}

code2lang = {y: x for x,y in lang2code.items()}

def get_ud_paths(base_path, type_, format_):
    assert type_ in {'dev', 'train', 'test'}
    assert format_ in {'conllu', 'conllx'}
    treebanks = [tb for tb in listdir(base_path) if tb.startswith("UD_")]
    path_format = lambda tb: join(base_path, tb, "{}-ud-{}.{}".format(lang2code[udname2lang[tb]], type_, format_))
    tb_paths = {udname2lang[lang]: path_format(lang) for lang in treebanks}
    return tb_paths

def get_system_output_paths(base_path, type_, format_):
    assert type_ in {'dev', 'test'}
    assert format_ in {'conllu', 'conllx'}
    treebanks = [tb for tb in listdir(base_path) if tb.startswith("UD_") and tb.endswith(format_)]
    return {udname2lang[lang.split(".")[0]]: join(base_path, lang) for lang in treebanks}

import fileinput

def conllu_to_sentence_structure(conllu_tree):
    """
    This takes a conllu sentence as input and outputs its parsed instance.

    Given this:
    6-7     isn't    _       _       _       _       _       _       _       _
    6       is       _       DET     DET     PronType=Art    7       det:def _       _

    We output:
    [..., {"word": "is",
     "part_of_token": "isn't",
     "token_ids": (6, 7),
     "id": 6,
     "lemma": None,
     "cpostag": "DET",
     "postag": "DET",
     "feats": {"Gender": "Masc",
               "Number": "Sing"},
     "head": 5,
     "deprel": "nmod:smixut",
     "deps": None,
     "misc": None}, ...]
    """

    sentence_structure = []
    token_first, token_last = -1, -1
    token = None

    for line in conllu_tree:
        if line.strip().startswith("#"):
            sentence_structure.append({"metadata": line[1:].strip()})
            continue
        elif line.strip() == "":
            continue

        (w_id, word, lemma, cpostag, postag,
         feats, head, deprel, deps, misc) = line.split("\t")

        # Replace _ with None for where it's allowed
        (cpostag, postag, feats,
         head, deps, misc) = [param if param != "_" else None for param in
                              (cpostag, postag, feats, head, deps, misc)]

        # We only want lemma to be None if the word form itself isn't _
        if lemma == "_" and word != "_":
            lemma = None

        # Keep track of where the multi-word token starts and ends
        if "-" in w_id:
            token_first, token_last = map(int, w_id.split("-"))
            token_ids = (token_first, token_last)
            token = word
            continue
        elif int(w_id) > token_last:
            token_ids = None
            token = None

        # Parse features into dict. Unary features have None as value.
        feats_map = {}
        if feats is not None:
            for param in map(lambda f: f.split("="), feats.split("|")):
                if len(param) == 1:
                    feats_map[param[0]] = None
                else:
                    feats_map[param[0]] = param[1]


        word_structure = {"id": int(w_id),
                          "word": word,
                          "lemma": lemma,
                          "cpostag": cpostag,
                          "postag": postag,
                          "feats": feats_map,
                           "head": int(head),
                           "deprel": deprel,
                           "deps": deps,
                           "misc": misc,
                           "token_ids": token_ids,
                           "token": token}

        sentence_structure.append(word_structure)

    return sentence_structure


class UDTree:
    def __init__(self, conllu_tree):
        self.raw = list(conllu_tree)
        sentence_structure = conllu_to_sentence_structure(self.raw)
        self.metadata = [w["metadata"] for w in sentence_structure
                         if "metadata" in w]

        self.sentence_structure = [w for w in sentence_structure
                                   if "metadata" not in w]

    def verify_tree_structure(self):
        raise NotImplementedError("Todo")

    @property
    def ids(self):
        return [w["id"] for w in self.sentence_structure]

    @property
    def lemmas(self):
        return [w["lemma"] for w in self.sentence_structure]

    @property
    def cpostags(self):
        return [w["cpostag"] for w in self.sentence_structure]

    @property
    def postags(self):
        return [w["postag"] for w in self.sentence_structure]

    @postags.setter
    def postags(self, vals):
        for w, val in zip(self.sentence_structure, vals):
            w["postag"] = val

    @property
    def words(self):
        return [w["word"] for w in self.sentence_structure]

    @property
    def tokens(self):
        ts = []
        token_printed = False
        for w in self.sentence_structure:
            if w["token"] is not None and not token_printed:
                ts.append(w["token"])
                token_printed = True
                continue
            elif token_printed and w["token_ids"] is None:
                token_printed = False
            elif token_printed and w["token_ids"][1] >= w["id"]:
                continue

            ts.append(w["word"])
        return ts

    @property
    def deprels(self):
        return [w["deprel"] for w in self.sentence_structure]

    @property
    def feats(self):
        return [w["feats"] for w in self.sentence_structure]

    @property
    def heads(self):
        return [w["head"] for w in self.sentence_structure]

    @property
    def deps(self):
        return [w["deps"] for w in self.sentence_structure]

    @property
    def miscs(self):
        return [w["misc"] for w in self.sentence_structure]

    def to_conllu_format(self):
        return self.raw

    def to_conllx_format(self):
        columns = zip(self.ids, self.words, self.lemmas, self.cpostags, self.postags,
                      self.feats, self.heads, self.deprels, self.deps, self.miscs)
        str_repr = []
        for colvalues in columns:
            colvalues = list(colvalues)
            colvalues[5] = "|".join([param + "=" + val for param, val in colvalues[5].items()])
            colvalues = ["_" if val is None or val == "" else val for val in colvalues]
            str_repr.append("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(*colvalues))
        return str_repr

    def __str__(self):
        return "UDTree{\n\t" + str(self.words) + "\n\t" + str(self.deprels) + "\n}"

    def __repr__(self):
        return str(self)


def to_trees(f):
    """
    This takes something iterable, like an open file object,
    and converts each conll-u sentence into a UDTree instance.
    """
    tree = []
    for line in f:
        line = line.strip()

        if len(line) == 0:  # end of sentence
            yield UDTree(tree)
            tree.clear()
            continue

        tree.append(line)

    if len(tree) > 0: # Collect the last stuff
        yield UDTree(tree)


def from_files(conllu_path):
    """
    Takes a path to a CONLL-U treebank and converts it into a list of UDTree instances.
    """
    with fileinput.FileInput(conllu_path) as f:
        for tree in to_trees(f):
            yield tree

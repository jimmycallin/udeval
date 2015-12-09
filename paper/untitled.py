"""
Calculates ratio of non-projectivity.
"""
import lang_utils, udtree

def is_non_projective(tree):
    is_non_projective = False
    for i, head in zip(tree.ids, tree.heads):
        if head-1 < 0:
            continue
        else:
            for j, inner_head in zip(tree.ids[i:head-1], tree.heads[i:head-1]):
                if inner_head < i or inner_head > head:
                    is_non_projective = True
    return is_non_projective

def get_np_trees(trees):
    np = []
    for tree in trees:
        if is_non_projective(tree):
            np.append(tree)

    return np

def get_non-projectivity_ratios():
    lang_trees = lang_utils.get_ud_paths('../resources/universaldependencies1-2/universal-dependencies-1.2/', type_='train', format_='conllu', coarse=False)

    np = dict()
    tot = dict()
    for lang, path in lang_trees.items():
        trees = list(udtree.from_files(path))
        tot[lang] = len(trees)
        np[lang] = get_np_trees(trees)

    rel = {}
    for lang, n in zip(np.keys(), np.values()):
        rel[lang] =  len(n) / tot[lang]

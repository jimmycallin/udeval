import udtree
import string

def is_only_punctuation(gold_path):
    is_punct = {}
    puncts = set(string.punctuation)

    for gold_tree in udtree.from_files(gold_path):
        for token, deprel in zip(gold_tree.tokens, gold_tree.deprels):
            all_puncts = True
            for char in token:
                if char not in puncts:
                    all_puncts = False
                    break
            if all_puncts:
                is_punct[deprel] = True
            else:
                is_punct[deprel] = False
    return {deprel for deprel,val in is_punct.items() if val}


def match_tree_attachments(system_tree, gold_tree, labeled=False, fine_grained_deprels=True, ignore_deprels=None):
    if ignore_deprels:
        ignore_deprels = set(ignore_deprels)
    correct, incorrect = [], []
    total = 0
    for (index,
         system_head,
         system_label,
         gold_head,
         gold_label) in zip(gold_tree.ids,
                            system_tree.heads,
                            system_tree.deprels,
                            gold_tree.heads,
                            gold_tree.deprels):

        if not fine_grained_deprels:
            gold_label = gold_label.split(":")[0]
            system_label = system_label.split(":")[0]

        if ignore_deprels and gold_label in ignore_deprels:
            continue

        is_correct = False
        if system_head == gold_head:
            is_correct = True
            if labeled and system_label != gold_label:
                is_correct = False

        if is_correct:
            correct.append((index, system_head, system_label, gold_head, gold_label))
        else:
            incorrect.append((index, system_head, system_label, gold_head, gold_label))

    return correct, incorrect

def attachment_score(system_output_path, gold_path, labeled=True, fine_grained_deprels=True, include_punct=False):
    puncts = None
    if not include_punct:
        puncts = set.union(is_only_punctuation(gold_path), {'punct'})
    system = udtree.from_files(system_output_path)
    gold = udtree.from_files(gold_path)
    correct, incorrect = 0, 0
    for system_tree, gold_tree in zip(system, gold):
        (tree_correct,
         tree_incorrect) = match_tree_attachments(system_tree, gold_tree, labeled,
                                                  fine_grained_deprels=fine_grained_deprels,
                                                  ignore_deprels=puncts)
        correct += len(tree_correct)
        incorrect += len(tree_incorrect)

    if (correct + incorrect) == 0:
        return float("NaN")

    return correct / (correct + incorrect)


def labels_precision_recall(system_output_path,
                            gold_path,
                            labels=["nsubj", "nsubjpass"],
                            fine_grained_deprels=True):
    system = udtree.from_files(system_output_path)
    gold = udtree.from_files(gold_path)
    system_correct, system_incorrect, gold_count = 0, 0, 0
    for system_tree, gold_tree in zip(system, gold):
        (tree_correct,
         tree_incorrect) = match_tree_attachments(system_tree, gold_tree, True,
                                                  fine_grained_deprels=fine_grained_deprels)
        for _, _, system_label, _, _ in tree_correct:
            if system_label in labels:
                system_correct += 1
                gold_count += 1
        for _, _, system_label, _, gold_label in tree_incorrect:
            if gold_label in labels:
                gold_count += 1
            if system_label in labels:
                system_incorrect += 1

    if system_correct + system_incorrect == 0:
        precision = float("NaN")
    else:
        precision = system_correct / (system_correct + system_incorrect)

    if gold_count == 0:
        recall = float("NaN")
    else:
        recall = system_correct / (gold_count)

    return precision, recall

def weighted_las(system_output_path, gold_path, weights):
    system = udtree.from_files(system_output_path)
    gold = udtree.from_files(gold_path)
    correct, incorrect = 0, 0
    for system_tree, gold_tree in zip(system, gold):
        (tree_correct,
           tree_incorrect) = match_tree_attachments(system_tree, gold_tree, True,
                                                  fine_grained_deprels=False)
        for _, _, _, _, gold_label in tree_correct:
            correct += weights[gold_label]

        for _, _, _, _, gold_label in tree_incorrect:
            incorrect += weights[gold_label]

    if (correct + incorrect) == 0:
        return float("NaN")

    return correct / (correct + incorrect)


def root_distance(tree, index):
    if tree.heads[index-1] == 0:
        return 1
    else:
        return 1 + root_distance(tree, tree.heads[index-1])

def root_distance_las(system_output_path, gold_path, include_punct=False):
    puncts = None
    if not include_punct:
        puncts = set.union(is_only_punctuation(gold_path), {'punct'})
    system = udtree.from_files(system_output_path)
    gold = udtree.from_files(gold_path)
    correct, incorrect = 0, 0
    for system_tree, gold_tree in zip(system, gold):
        (tree_correct,
           tree_incorrect) = match_tree_attachments(system_tree, gold_tree, True,
                                                  fine_grained_deprels=False,
                                                  ignore_deprels=puncts)
        for index, _, _, _, gold_label in tree_correct:
            correct += 1 / root_distance(gold_tree, index)

        for index, _, _, _, gold_label in tree_incorrect:
            incorrect += 1 / root_distance(gold_tree, index)

    if (correct + incorrect) == 0:
        return float("NaN")

    return correct / (correct + incorrect)

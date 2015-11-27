import udtree


def match_tree_attachments(system_tree, gold_tree, labeled=False, fine_grained_deprels=True):
    correct, incorrect = [], []
    total = 0
    for (system_head,
         system_label,
         gold_head,
         gold_label) in zip(system_tree.heads,
                            system_tree.deprels,
                            gold_tree.heads,
                            gold_tree.deprels):

        if not fine_grained_deprels:
            gold_label = gold_label.split(":")[0]
            system_label = system_label.split(":")[0]

        is_correct = False
        if system_head == gold_head:
            is_correct = True
            if labeled and system_label != gold_label:
                is_correct = False

        if is_correct:
            correct.append((system_head, system_label, gold_head, gold_label))
        else:
            incorrect.append((system_head, system_label, gold_head, gold_label))

    return correct, incorrect

def attachment_score(system_output_path, gold_path, labeled=True, fine_grained_deprels=True):
    system = udtree.from_files(system_output_path)
    gold = udtree.from_files(gold_path)
    correct, incorrect = 0, 0
    for system_tree, gold_tree in zip(system, gold):
        (tree_correct,
         tree_incorrect) = match_tree_attachments(system_tree, gold_tree, labeled,
                                                  fine_grained_deprels=fine_grained_deprels)
        #print("Correct: {} \n".format(tree_correct))
        #print("Incorrect: {}".format(tree_incorrect))
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
        for _, system_label, _, _ in tree_correct:
            if system_label in labels:
                system_correct += 1
                gold_count += 1
        for _, system_label, _, gold_label in tree_incorrect:
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

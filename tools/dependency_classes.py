# My classes
content_dependents = {"acl", "advcl", "advmod", "amod", "appos", "ccomp", "compound", "conj", "csubj", "csubjpass", "dislocated", "dobj", "iobj", "list", "name", "nmod", "nsubj", "nsubjpass", "nummod", "parataxis", "remnant", "root", "vocative", "xcomp"}
function_dependents = {'aux', 'auxpass', 'case', 'cc', 'cop', 'det', 'expl', 'mark', 'neg', 'mwe'}
nonsemantic_dependents = {"punct", "discourse", "reparandum", "dep", "goeswith", "foreign"}

dep2class = {label: 'content' for label in content_dependents}
dep2class.update({label: 'function' for label in function_dependents})
dep2class.update({label: 'nonsemantic' for label in nonsemantic_dependents})

# UD classes
core_dependents = {'nsubj', 'csubj', 'nsubjpass', 'csubjpass', 'dobj', 'ccomp', 'xcomp', 'iobj'}
noncore_dependents = {'nmod', 'advcl', 'advmod', 'neg'}
coordination_dependents = {'conj', 'cc', 'punct'}
special_clausal_dependents = {'vocative', 'aux', 'mark', 'discourse', 'auxpass', 'expl', 'cop', 'punct'}
noun_dependents = {'nummod', 'acl', 'amod', 'appos', 'nmod', 'det', 'neg'}
other_dependents = {'root', 'dep'}
compound_and_unanalyzed_dependents = {'compound', 'name', 'mwe' 'foreign', 'goeswith'}
case_marking_dependents = {'case'}
loose_joining_dependents = {'list', 'parataxis', 'remnant', 'dislocated', 'reparandum'}

udep2class = {label: 'core_dependents' for label in core_dependents}

all_labels = set.union(content_dependents, function_dependents, nonsemantic_dependents)
all_labels_excl_nonsemantic = set.union(content_dependents, function_dependents)

---
title: "A typological perspective on evaluation for Universal Dependencies"
author:
- name: Jimmy Callin
  affiliation: Uppsala University
  email: jimmy.callin@gmail.com
tags: [universal dependencies, parsing, evaluation, dependency, attachment score]
abstract: |
  Established evaluation metrics assume that all dependency relations are equally important. Furthermore, when comparing parsing results in a cross-linguistic manner, it is easy to assume equal attachment scores is equivalent to equal performance. We demonstrate why this is not the case, especially when comparing languages with large difference in morphological complexity, and emphasize the necessity for new evaluation metrics that takes these considerations into account. We also present two alternative evaluation metrics motivated by these findings: one based on scoring only content dependency relations, and another where dependency relation are weighted by their Inverse Word Entropy score.
bibliography: bibliography.bib
---

# Introduction

The role of language processing is becoming increasingly multi-lingual. This is reflected in recent efforts into providing dependency parsing frameworks that can reliably be applied on a multitude of languages. One of the currently most ambitious projects in this area is the Universal Dependencies (UD) framework [@nivre_universal_2015], where the aim is to create a parsing framework with a cross-linguistically consistent grammatical annotation. The purpose of this work is to primarily allow sound comparison of parsing representations between languages. 

Data-driven evaluation metrics have been used as long as the availability of treebanks (see @collins_headdriven_1999 chap. 4 and @carroll_parser_1998 for surveys on early methods and results). To evaluate statistical dependency parsing models, _Unlabeled Attachment Score_ (UAS) has been in use under different names since the early days. @eisner_empirical_1997 was first to call it attachment score, which refers to work done by @lin_dependencybased_1998. _Labeled Attachment Score_ (LAS) was first introduced in @nivre_memorybased_2004 to emphasize the importance of correct labeling. UAS is defined as the accuracy of correct attachments in a test collection, while LAS includes the additional constraint of requiring a correct attachment label. These have in their simplicity and intuitiveness served the research area well, but their design relies on a number of assumptions we argue do not hold in the context of UD.

\begin{figure}
\begin{center}
\begin{dependency}
   \begin{deptext}[column sep=1em]
      Ammuin \&[0.5em] elefantin \&[0.8em] pyjamassani \&[0.5em] . \\
   \end{deptext}
   \deproot{1}{ROOT}
   \depedge{1}{2}{dobj}
   \depedge{1}{3}{nmod}
   \depedge{1}{4}{punct}
\end{dependency}
\begin{dependency}[edge below, edge vertical padding=0.2em]
   \begin{deptext}[column sep=0.2em]
         I \& shot \&[.5em] an \& elephant \&[.5em] in \& my \& pajamas \& . \\
    \end{deptext}
    \depedge{2}{1}{nsubj}
    \depedge[edge unit distance=1.7ex]{2}{8}{punct}
    \depedge{4}{3}{det}
    \depedge{2}{4}{dobj}
    \depedge[edge unit distance=1.5ex]{2}{7}{nmod}
    \depedge{7}{5}{case}
    \deproot[edge unit distance=3.5ex]{2}{ROOT}
    \wordgroup{1}{1}{2}{}
    \wordgroup{1}{3}{4}{}
    \wordgroup{1}{5}{7}{}
    \depedge{7}{6}{nmod:poss}
\end{dependency}

\end{center}
\caption{Finnish and English dependency tree for \emph{I shot an elephant in my pajamas}. Each group of English words corresponds to one Finnish word. Note the edge count of Finnish being 4, while the English edge count is 8.}
\label{finnishparsing}
\end{figure}

Firstly, the design of attachment scores assumes that we know next to nothing about the taxonomy and design choices of the parsing framework. This has historically been necessary since there has not been a consistently adapted framework for dependency parsing across many languages. We argue that recent progress in UD has made this assumption invalid. UD has a carefully specified framework that its treebanks have to adapt, and we can exploit this constraint to learn more about the performance of a model.

Secondly, parsing results are increasingly juxtaposed in a cross-linguistic manner, and this trend will likely continue with the establishment of UD. It is not uncommon to compare the output of e.g. English and Finnish under the assumption that equal evaluation scores is equivalent to equal parsing performance. Why this is problematic becomes apparent when studying grammatical morphemes in languages where these may be free (i.e. function words) with languages where they typically are bound on content words (i.e. affixes).

In Figure \ref{finnishparsing}, we have a Finnish sentence with four edges, while the equivalent sentence in English requires a total of eight edges. The problem appears as soon as we introduce a parsing error into the trees: one faulty edge in the Finnish sentence would result in a performance reduction of 25%, while the same error in the English sentence only would reduce the accuracy by 12.5%. Function words are regular in their appearance, and should therefore be relatively easy for a model to parse correctly. Our hypothesis is that languages with a comparatively large number of function words, like English, receive a more or less free performance boost when using classic evaluation metrics.

Based on these intuitions, our aim is to contribute to these two questions:

- How much do languages with a large number of free grammatical morphemes benefit from current evaluation schemes?
- Would focusing on correct classification of content word dependencies be a better evaluation scheme for cross-linguistic parsing performance?

The first question will be answered in Section 6 by looking at the correlation of function relations' frequency ratio with a parsing model's labelled attachment score across languages. For the second question, we set up two alternative evaluation metrics in Section 5, with correlation scores against human judgment data and analysis of cross-treebank variance in Section 6.

# Related Work

Not much work has been done in cross-linguistic evaluation, and papers presenting evaluation scores on several languages simply use previously available metrics without analyzing their shortcomings in such a context. Before the work on UD was initiated, there have been several attempts at automatic normalization of dependency treebanks into a common format for a more robust evaluation [@zeman2012hamledt]. In light of this work on cross-linguistically consistent annotation frameworks, @tsarfaty_evaluating_2011 take a separate approach with cross-framework evaluation, where they suggest an evaluation technique that is robust towards differing annotation criteria. 

Since UAS arguably has been more popular of the two attachment scores, finding performance results on subsets of labeled dependency relations is difficult. In cases of extensive error analysis it is possible to find sections devoted to this [@plank_domain_2011, chapter 6.6]. There has also been work looking at specific constructions, e.g. unbounded dependency evaluation [@nivre_evaluation_2010; @rimell_unbounded_2009], where they argue that some dependency relations are more critical for a parser to get right than others.

@plank_dependency_2015 look closer at whether or not manual parsing evaluation correlate with standard dependency metrics, coming to the conclusion that none of today's established metrics are especially well correlated with human quality judgment. One of their main findings is that humans tend to consider content dependencies to be of more importance than function dependencies, which fits well with the assumptions made in this paper.

# Data

\begin{table}[t]
\begin{center}
\resizebox{0.9\columnwidth}{!}{
\begin{tabular}{lrr}
\toprule
Treebank & Token size & Non-proj ratio\\
\midrule
Arabic & 282K & 0.01 \\
Bulgarian & 156K & 0.03 \\
Croatian & 87K & 0.05 \\
Czech & 1503K & 0.09 \\
Danish & 100K & 0.12 \\
English & 254K & 0.02 \\
Finnish & 181K & 0.04 \\
Gothic & 56K & 0.12 \\
Greek & 59K & 0.21 \\
Hebrew & 115K & 0.00 \\
Hindi & 351K & 0.04 \\
Italian & 252K & 0.01 \\
Norwegian & 311K & 0.02 \\
Old Church Slavonic & 57K & 0.13 \\
Persian & 151K & 0.04 \\
Polish & 83K & 0.00 \\
Portuguese & 212K & 0.15 \\
Slovenian & 140K & 0.11 \\
Spanish & 423K & 0.02 \\
Swedish & 96K & 0.01 \\
\bottomrule 
\end{tabular}}
\caption{Selected treebanks from the UD 1.2 treebank collection, with their token size and amount of non-projective trees.}
\label{tbl:ud-treebanks}
\end{center}
\end{table}

We will be using a subset of the Universal Dependencies treebank 1.2 [@nivre_universal_2015-1]. To keep them as internally consistent as possible, all treebanks must adhere to the following criteria:

- They have morphological features.
- They have at least 30K tokens.
- They have less than 25% non-projective trees.
- In the case of more than one valid treebank for a language, choose the treebank with manual corrections or largest token count.

A total of 17 treebanks were removed. 5 of these had too few tokens, 4 lacked features, 4 had too many non-projective trees, while 4 treebanks were language duplicates. This leaves us with the 20 languages listed in Table \ref{tbl:ud-treebanks}. Most notably we lost the French and German treebanks due to their lack of morphological features.

For measuring the correlation of metrics to manual evaluation, we will be using parts of the human judgment data as provided by @plank_dependency_2015. Not all languages in the dataset are from the UD treebanks, thus only English, German, and Spanish are used. For this particular task, we are not interested in cross-lingual performance comparison, which is why we include German here but not elsewhere.

\begin{table}[t]
\begin{center}
\begin{tabular}{p{3.2cm} p{3.2cm}}
\toprule
Function relations & Content relations \tabularnewline
\midrule


\begin{tabular}[t]{@{} p{3cm}}
    \mbox{aux} \mbox{auxpass} \mbox{case} \mbox{cc} \mbox{cop} \mbox{det} \mbox{expl} \mbox{mark} \mbox{neg} \tabularnewline
\addlinespace[0.15cm]
\toprule
    Other  \tabularnewline
\midrule
    \mbox{list} \mbox{dep} \mbox{foreign} \mbox{mwe} \mbox{reparandum}  \mbox{punct} \mbox{name} \mbox{goeswith} \mbox{discourse} 
\end{tabular}

&

   acl advcl \mbox{advmod} \mbox{amod} \mbox{appos} \mbox{ccomp} \mbox{compound} \mbox{conj} \mbox{csubj} \mbox{csubjpass} \mbox{dislocated} dobj iobj nmod nsubj \mbox{nsubjpass} nummod parataxis remnant root \mbox{vocative} xcomp  \\ 
\bottomrule
\end{tabular}
\caption{Classification of content and function relations.}
\label{tbl:dependency-relations}
\end{center}
\end{table}


# Categorizing Dependency Relations

We motivate our choice of function and content relations based on the specification of universal dependency relations\footnote{\url{http://universaldependencies.github.io/docs/u/dep/index.html}}, linguistic intuition, and a newly developed statistical method. First, let us define what we consider to be function and content relations:

- A _function relation_ is a relation that links a word with a function word.
- A _content relation_ is a relation that either has _root_ as its head, or links a content word with another content word.

## Categorization by Specification

Given the previous definition as well as the specification of universal dependency relations, we can categorize a relation based on how it should occur in UD treebanks. Going through each dependency relation in this manner  produces a classification as presented in table \ref{tbl:dependency-relations}. 

We chose to remove some relations where we cannot make assumptions of its content, labeled _other_. The _foreign_ relation has no restrictions on what type of word it should choose as a dependent as long as it is a foreign word. _list_ is used in cases where the content cannot be easily analyzed. _reparandum_ and _dep_ are neither of semantic nor syntactic nature and we cannot make any assumptions of their content. _mwe_ and _name_ lack a clear intrinsic dependency structure, and are rather used to bind words that belong together. _punct_ and _discourse_ are removed for similar reasons, but also due to particles often being ignored in other evaluation schemes.

## Placing Dependency Relations on a Function--Content Spectrum

Next question to answer is if we can motivate our classification not only on linguistic intuition and the specification of dependency relations, but also from an empirical perspective. We do this by adhering to our previous definition on function and content relations, and what we know of the nature of function words. Since function words are part of closed word classes, meaning new words rarely get introduced into their categories, we can expect the number of distinct word types to be quite small, especially when compared to the word classes shared by typical content words such as _nsubj_. 

\begin{figure}[t]
\centering
\includegraphics{figures/word_dependency_entropy.pdf}
\caption{Averaged word dependency entropy for all universal dependency relations, with the manually created categories.}
\label{fig:averaged_wde}
\end{figure}

\begin{figure}[t]
\hspace*{-1cm}
\includegraphics{figures/standard_ttr.pdf}
\caption{Standardized type/token ratio for chunks of 1000 tokens (blue), with content relation frequency ratio (green) and function relation frequency ratio (red). High STTR score implies high morphological complexity. $R(\mbox{Content freq}, \mbox{STTR}) = 0.23$, $R(\mbox{Function freq}, \mbox{STTR}) = -0.52$.}
\label{fig:standard_ttr}
\end{figure}


Assuming this holds, we expect that the probability of a word given a function relation to be zero for all but a few cases, while the probability of a word given a content relation should be much more evenly spread. This can be quantified by measuring a relation's entropy for its word probabilities. We call this measure _word dependency entropy_ (WDE). Calculated for all treebanks we get the averaged WDE. For the averaged WDE, we add the assumption that a function relation should be occurring in all treebanks, and make sure to punish relations that are missing by implying that they are neither function nor content relations.

Here we formally define word dependency entropy. A probability distribution $p$ takes as input a word $w$ conditioned on a treebank $t \in T$, and a dependency relation $r$. $H$ is the entropy function that takes $p(w|r,t)$ as input and calculates its entropy. The entropy function is normalized by its upper bound $\log n_w$, where $n_w$ is the size of the vocabulary. This keeps the range of the function to $[0,1]$. To calculate the WDE for a set of treebanks, we average WDE for all treebanks $t \in T$. In the case a dependency relation is not present in a treebank, we set its WDE to 0.5.

This produces the following mathematical functions:

$$\mbox{WDE}(r,t) = \dfrac{H(p(w|r,t))}{\log n_w}$$

$$\mbox{Averaged WDE}(r, T) = \dfrac{1}{n_T} \sum_{t \in T}{\mbox{WDE}(r,t)}$$

The averaged WDE for UD 1.2 is presented in Figure \ref{fig:averaged_wde}, along with our manual categorization of dependency relations. Ignoring the _other_ relations, we find that the WDE gives an intuitive ordering of the dependency relations, while empirically supporting our choice of content and function relations. As expected, _cc_ and _neg_ are at the bottom of the list. While _conj_ might not be as prototypical of a content relation as _nmod_, it is still highly dependent on content words.

<!-- Overall las scores -->
\begin{figure*}[t]
\centering
\includegraphics{figures/content_las_comparison.pdf}
\caption{Overall LAS, WLAS, precision and recall for content dependencies. Sorted by LAS.}
\label{fig:content_las_comparison}
\end{figure*}


## Finding Correlation with External Measurements

We would expect the ratio of function words in a given language's treebank to correlate with its degree of synthesis. Measuring degree of synthesis is not a trivial task, and there have been several proposed algorithms for this. Despite having obvious drawbacks, an often used indirect measurement of degree of synthesis is the type/token ratio [@kettunen_can_2014]. This assumes that synthetic languages, with their morphologically rich systems, will have fewer tokens per word than analytic languages such as English or Hindi. This is not particularly robust when comparing across corpora of different sizes. As such, we will be using the _standardized_ type/token ratio (STTR), which calculates average TTR in chunks of 1000 tokens\footnote{Introduced by Mike Scott in \url{http://lexically.net/downloads/version6/HTML/index.html?type_token_ratio_proc.htm}}. Figure \ref{fig:standard_ttr} shows that there is a weak correlation between languages' frequency ratio of content relations and their STTR, while the negative correlation against ratio of function relations is much stronger. Some languages for content relations are clear outliers such as Old Church Slavonic, Arabic, Gothic, Persian, English, and Hindi. It is not clear why the ratio correlation is stronger for function relations than for content relations. Whether this is a result of a bad degree of synthesis measurement, a bad classification of content dependency relations, or a combination of both is up for discussion. 


# Experimental Setup {#expsetup}

Based on the previous findings, we propose two alternative metrics to the LAS. The first metric is based on our manual classification of content and function dependencies, while the latter is exploiting the weights outputted by the WDE. 

For testing the evaluation metrics, we train MaltParser 1.7 with configuration settings retrieved by running MaltOptimizer on the corresponding treebanks [@nivre2006maltparser; @ballesteros2012maltoptimizer]. Due to the size of the Czech treebanks and hardware restrictions, we only use half of the Czech training data in the optimization step. Since MaltParser 1.7 does not natively support the CoNLL-U format, all treebanks are converted to CoNLL-X by only keeping word level dependencies. In the process, if the `CPOSTAG` column is empty, all corresponding `POSTAG` values are copied over since MaltParser primarily relies upon this column. Most importantly, since we are interested in a cross-lingual analysis of dependency relation performance, we remove all fine-grained relations. That is, in the case of _nmod:poss_ we only keep _nmod_.

#### Performance of Content Relations

In this metric, we look at the precision and recall for all content dependency relations, ignoring any relation that is not a part of this class. Since not all dependency relations are involved, the precision and recall can differ and thus become interesting to analyze separately. We call these _content precision_ and _content recall_.

#### Weighting Relations by their WDE

We weight each dependency relation by its averaged WDE as presented in Figure \ref{fig:averaged_wde}. This will increase the importance of content relations, while the function relations provide less to the overall score. We call this the _Weighted Labeled Attachment Score_ (WLAS). Using WLAS has the additional interesting property of also being easily calculated and deployable to non-UD frameworks.


# Evaluation {#evaluation}


Figure \ref{fig:content_las_comparison} lists the parsing results for all languages, with LAS, WLAS, and content precision and recall. We can tell that LAS is consistently providing higher scores for each output compared to WLAS, while the content precision and recall scores are substantially lower. There are small differences for precision and recall for all except the worst performing languages where, given the higher recall, the parsing model seems to have a bias towards content dependencies.

Table \ref{tbl:res_corrs} lists the Pearson correlation coefficient between treebanks for WLAS, LAS, content precision and recall, function precision and recall, and the frequency ratio of content and function relations in the treebanks. The correlation between the various suggested measurements, as well as with LAS, are quite strong. The content frequency ratio has a strong negative correlation with function frequency ratio, and negative across all the other measurements as well. Function frequency ratio has more or less strong positive correlations with all metrics.

Figure \ref{fig:cumul_vars} shows what happens with the variance when cumulatively adding languages in a top-scoring fashion for each measurement. For content precision and recall as well as WLAS, the variance is lower for high performing languages, but takes off for content precision and recall when you get past the first eleven treebanks. WLAS keeps an even score for less well-performing languages compared with LAS until the end where they join content performance in a variance of about $0.0035$.

Table \ref{tbl:human_judgment} lists Spearman correlations between manual evaluation of two parser models, where the evaluators given parsed sentences in each case chose which of two parser models they consider to provide the best output. Content precision and recall are in all cases except one inferior to LAS and WLAS, where the two latter are indistinguishable.

Table \ref{tbl:cascading_errors} lists the ratio of correct parent dependency relations given a faulty relation of either function or content class, labeled or unlabeled. The parent of a token with a faulty relation is defined as the parent of the system output relation, and _not_ as the parent of the gold relation. A lower ratio means that the dependency class is more prone to cascading errors. The results show that function dependencies have more cascading errors than content dependencies.


<!-- Correlation matrix -->
\begin{table}[t]
\centering
\resizebox{\columnwidth}{!}{
    \input{tables/res_corrs.latex}
}
\caption{Pearson correlation matrix between treebanks for content and function frequency ratio  (\emph{C freq} and \emph{F freq}), content precision and recall  (\emph{C prec} and \emph{C rec}), function precision and recall  (\emph{C prec} and \emph{C rec}), LAS, and WLAS. Boldfaced figures are mentioned in the discussion.}
\label{tbl:res_corrs}
\end{table}

<!-- Cumulative variance -->
\begin{figure}[t]
\centering
\includegraphics{figures/cumul_vars.pdf}
\caption{Cumulative variance when adding languages in a top-scoring order.}
\label{fig:cumul_vars}
\end{figure}

<!-- Human judgment correlations -->
\begin{table}[t]
\centering
\resizebox{\columnwidth}{!}{\input{tables/human_judgment.latex}}
\caption{Correlations of LAS, WLAS, content precision and recall against human judgment data.}
\label{tbl:human_judgment}
\end{table}

<!-- Cascading errors -->
\begin{table}[t]
\centering
\resizebox{\columnwidth}{!}{\input{tables/cascading_errors.latex}}
\caption{In the case of incorrect dependency relation of either function or content class, how frequent is it to have a correct (system output) parent relation? The lower the ratio, the more common are cascading errors.}
\label{tbl:cascading_errors}
\end{table}

# Discussion {#discussion}

Looking at function frequency and its precision in Table \ref{tbl:res_corrs}, they have a correlation of $0.71$. This suggests that the larger rate of function words in a language, the easier it is to parse its function words. What is interesting is that this does not hold when looking at the content frequency ratio and its precision or recall, where one might expect that there is a strong positive correlation which would indicate that a high degree of content relations makes it easier to parse these classes. Instead, we find a weak negative correlation of $-0.39$ for recall. Furthermore, given languages' LAS scores, the more function words there is in a language, the better it performs. Even when looking at the relation between the amount of function words in a language with how well it does on content words, the correlation is weakly positive. We take this to mean that our choice of parser, while not explicitly tuned for any particular language, still benefits from a context with a high rate of grammatical function words. These findings support our hypothesis, that languages with a high degree of function dependency relations has an unfair advantage when comparing attachment scores across languages.

Regarding the evaluation scores for different evaluation metrics, as presented in Figure \ref{fig:content_las_comparison}, it is difficult to tell if any metric is better than the other. One might expect that the scoring difference of LAS and WLAS, or LAS and content performance, would correlate with its STTR score, since analytic languages like Hebrew and English have more to lose on decreasing the importance of function words. Unfortunately, this correlation is rather weak. Assuming that the STTR scoring is reliable, we believe this has to do with what we described above: languages with a high rate of function words provide a better context for content words for parsers. 

Going back to Table \ref{tbl:res_corrs}, a better measurement than LAS would be expected to have a weaker correlation with the function frequency ratio, showing that the importance of the amount of function words in a language decrease. Since WLAS has a weaker correlation than LAS at $0.42$ versus $0.54$, it suggests that the measurement is on the right path. Even more so, content precision and recall at $0.17$ and $0.20$ respectively indicates that content performance in this aspect is a better evaluator than WLAS.

We ran the measurements on the human judgment data with the results given in Table \ref{tbl:human_judgment}. Unfortunately, none of the metrics seem to improve upon the LAS score, which was the top scoring metric reported in the original paper. Only content recall sees some improvements over LAS for English, but other than that the results are either worse or equal to those of LAS. WLAS has overall very small changes compared to LAS, which is somewhat surprising given that the original paper commented on content relations being considered more important than function relations by the manual evaluators. This could possibly be explained by function relations overall performing quite well, and whenever there are erroneous function relations they are cascaded from faulty content relations. While this hypothesis is supported by Table \ref{tbl:cascading_errors}, showing how erroneous function relations in all languages are more commonly having faulty parents than incorrect content relations, the differences are not large enough to indicate that this is the only reason. This might also just be an effect of function dependencies being further down in the tree than content dependencies,   

Another approach is to look at the variance of the metrics. If our initial hypothesis holds, this should mean that some of the differences found between languages before evens out, and thereby lowering the variance when compared to LAS. Figure \ref{fig:cumul_vars} reveals that this does not hold when looking at all treebanks, but by cumulatively adding treebanks it is possible to study the effect as the performance decreases. Indeed, the variance is lower among high-performing languages for WLAS and and content performance, and could potentially be explained by that differences among top-scoring languages are much less random due to a poor parsing model and it is first among these that the choice of metric starts to matter.

That brings us to the choice of parser model and its effect on the results. In the name of consistent treebanks, we chose to remove treebanks with a large number of non-projective trees. Another motivation was that our parser can not handle these types of trees especially well, and the results are thus unreliable when comparing across languages. Is is quite possible, and even probable, that there are many similar factors playing a role in the discussed results. For instance, the size of the treebank has definitely an effect. In future work, we should reproduce these results with alternative models and look for any similarities or differences that might strengthen our claims or explain some of the peculiarities we have seen in this work.

# Conclusion

In this paper we have presented experiments that suggest that languages with many function dependency relations are easier to parse than languages with richer morphology, given current parser models. We have motivated the necessity for new evaluation metrics that take these considerations into account from a typological perspective, while also referring to research that motivates this from human judgment standards. We suggested two new evaluation metrics that raise the importance of content dependency relations with some initial experiments indicating their usefulness.

# Acknowledgements

We thank Jörg Tiedemann for providing his parsing output on UD 1.0 for initial experiment development.

\section*{References}

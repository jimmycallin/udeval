---
title: "Towards a better evaluation scheme for Universal Dependencies"
author:
- name: Jimmy Callin
  affiliation: Uppsala University
  email: jimmy.callin@gmail.com
tags: [universal dependencies, parsing, evaluation]
abstract: |
  Todo:

  - Write this abstract.
  - Add human judgment results
      + expand upon this in introduction and conclusion
  - Write results section
  - Discuss results.
bibliography: bibliography.biblatex
---

# Introduction

The role of language processing is becoming increasingly multi-lingual, which  is reflected in recent efforts into providing dependency parsing frameworks that can reliably be applied on a multitude of languages. One of the most ambitious projects in this area is the Universal Dependencies (UD) framework [@nivre_universal_2015], where the goal is to create a parsing framework with a cross-linguistically consistent grammatical annotation. The purpose of this work is to remove the requirement of language specific components which has up to this point been a necessity due to inconsistent annotation standards.

Data-driven evaluation metrics have been used as long as treebanks have been available (see @collins_headdriven_1999 chap. 4 for a survey on early results). To evaluate statistical parsing models, two of the most ubiquitous evaluation metrics are Labeled Attachment Score (LAS) and Unlabeled Attachment Score (UAS).
These have in their simplicity and intuitiveness served the research area well, but their design relies on a number of assumptions that we argue do not hold in the context of UD.

\begin{figure}
\begin{center}
\begin{dependency}
   \begin{deptext}[column sep=1em]
      Ammuin \& elefantin \& pyjamassani \& . \\
      \emph{I\_shot} \& \emph{an\_elephant} \& \emph{in\_my\_pajamas} \& . \\
   \end{deptext}
   \deproot{1}{ROOT}
   \depedge{1}{2}{dobj}
   \depedge{1}{3}{nmod}
   \depedge{1}{4}{punct}
\end{dependency}

\end{center}
\label{finnishparsing}
\caption{Finnish dependency tree for \emph{I shot an elephant in my pajamas}. Note the edge count of Finnish being 4, while the English edge count is 8.}
\end{figure}

Firstly, the design of attachment scores assumes that we know next to nothing about the taxonomy and design choices of the parsing framework. This has historically been necessary since there have not been a consistently adapted framework for dependency parsing across many languages. We argue that recent progress in UD has made this assumption invalid. UD has a carefully specified framework that all UD treebanks has to adapt, and we can exploit this constraint to learn more about the performance of a model.

Secondly, parsing results are increasingly juxtaposed in a cross-linguistic manner, and this will likely continue with the establishment of UD. It is not uncommon to compare the output of e.g. English and Finnish under the assumption that equal evaluation scores is equivalent to equal parsing performance. The reason why this is problematic becomes apparent when studying grammatical morphemes in languages where these may be unbounded (i.e. function words) with languages where they typically are bounded on content words (i.e. affixes).

In figure \ref{finnishparsing}, we have a Finnish sentence with four edges, while the equivalent sentence in English requires a total of eight edges. The problem appears as soon as we introduce a parsing error into the trees: one faulty edge in the Finnish sentence would result in a performance reduction of 25%, while the same error in the English sentence only would reduce the accuracy by 12.5%. Function words are regular in their appearance, and should therefore be relatively easy for a model to parse correctly. Our hypothesis is that languages with a comparatively large number of function words, like English, receive a more or less free performance boost when using classic evaluation metrics.

Based on these intuitions, we hope to contribute to these two questions:

- How much does languages with a large number of unbounded grammatical morphemes benefit from current evaluation schemes?
- Would focusing on correct classification of content word dependencies be a better evaluation scheme for cross-linguistic parsing performance?

# Related work

Not much work has been done in cross-linguistic evaluation, and papers presenting evaluation scores on several languages simply use previously available metrics without analyzing their shortcomings in such a context. Before UD was publicly available, there have been several attempts at automatic normalization of dependency treebanks into a common format for a more robust evaluation [@zeman2012hamledt]. In light of this work on cross-linguistically consistent annotation frameworks, @tsarfaty_evaluating_2011 take a separate approach with cross-framework evaluation, where they suggest an evaluation technique that is robust towards differing annotation criteria. 

Since UAS arguably has been more popular of the two attachment scores, finding performance results on subsets of dependency relations has been difficult. In cases of extensive error analysis it is possible to find sections devoted to this [@plank_domain_2011, chapter 6.6]. There have also been work looking at specific constructions, e.g. unbounded dependency evaluation [@nivre_evaluation_2010], where they argue that some dependency relations are more critical for a parser to get right than others.

@plank_dependency_2015 look closer at whether or not manual parsing evaluation correlate with standard dependency metrics, coming to the conclusion that none of today's established metrics are especially well correlated with human quality judgment. One of their main findings is that humans tend to consider content dependencies to be of more importance than function dependencies, which fits well with the assumptions made in this paper.

# Data

\begin{table}[t]
\begin{center}
\begin{tabular}{ll}
\toprule
Treebank & Token size \\
\midrule
Arabic & 282K \\
Basque & 121K \\
Bulgarian & 156K \\
Croatian & 87K \\
Czech & 1503K \\
Danish & 100K \\
Dutch & 200K \\
English & 254K \\
Finnish & 181K \\
Gothic & 56K \\
Greek & 59K \\
Hebrew & 115K \\
Hindi & 351K \\
Italian & 252K \\
Norwegian & 311K \\
Old Church Slavonic & 57K \\
Persian & 151K \\
Polish & 83K \\
Portuguese & 212K \\
Slovenian & 140K \\
Spanish & 423K \\
Swedish & 96K \\
\bottomrule 
\end{tabular}
\caption{Selected treebanks from the UD 1.2 treebank collection, with their token size.}
\label{tbl:ud-treebanks}
\end{center}
\end{table}

We will be using a subset of the Universal Dependencies treebank 1.2 [@nivre_universal_2015]. To keep them as internally consistent as possible, all treebanks must adhere to the following criteria:

- They have morphological features.
- They have at least 30K tokens.
- They have a small ratio of non-projective trees.
- In the case of more than one valid treebank for a language, choose the treebank with manual corrections or largest token count.

A total of 15 treebanks where removed. 5 of these had too few tokens, 4 lacked features, 2 had too many non-projective trees, while 4 treebanks were language duplicates. This leaves us with the 22 languages listed in table \ref{tbl:ud-treebanks}. Most notably we lost the French and German treebanks.


\begin{table}[t]
\begin{center}
\begin{tabular}{p{3.2cm} p{3.2cm}}
\toprule
Function relations & Content relations \tabularnewline
\midrule


\begin{tabular}[t]{@{} p{3cm}}
    \mbox{aux} \mbox{auxpass} \mbox{case} \mbox{cc} \mbox{cop} \mbox{det} \mbox{expl} \mbox{mark} \mbox{neg} \mbox{mwe} \tabularnewline
\addlinespace[1.1cm]
\toprule
    Other  \tabularnewline
\midrule
    \mbox{list} \mbox{dep} \mbox{foreign} \mbox{reparandum}  \mbox{punct} \mbox{goeswith} \mbox{discourse} 
\end{tabular}

&

   acl advcl \mbox{advmod} \mbox{amod} \mbox{appos} \mbox{ccomp} \mbox{compound} \mbox{conj} \mbox{csubj} \mbox{csubjpass} \mbox{dislocated} dobj iobj list name nmod nsubj \mbox{nsubjpass} nummod parataxis remnant root \mbox{vocative} xcomp  \\ 
\bottomrule
\end{tabular}
\caption{Classification of content and function relations.}
\label{tbl:dependency-relations}
\end{center}
\end{table}


# Experimental setup

For testing our alternative evaluation metrics, we train MaltParser 1.7 using Nivre Arc-Eager with default settings on each treebank's training data and parse the included test data [@nivre2006maltparser]. We will also be using the human judgment data from @plank_dependency_2015 to see how well the evaluation metrics correlate with how well people consider the parsing output of a certain model is better than the parsing output of another model. Before continuing, we must split up the UD dependency relations into categories of function and content relations. 

We motivate our categorization based on the specification of universal dependency relations\footnote{\url{http://universaldependencies.github.io/docs/u/dep/index.html}}, linguistic intuition, and a newly developed statistical method. First, let us define what we consider to be function and content relations:

- A _function relation_ is a relation that links a word with a function word.
- A _content relation_ is a relation that links a content word with another content word.

## Categorization by specification

Given the previous definition as well as the specification of universal dependency relations, we can categorize a relation based on how it should occur in UD treebanks. Going through each dependency relation in this manner we ended up with a classification as presented in table \ref{tbl:dependency-relations}. 

We chose to remove some relations where we cannot make assumptions of its content, labeled _other_. The _foreign_ relation has no restrictions on what type of word it should choose as a dependent as long as it is a foreign word. _List_ are used in cases where the content cannot be easily analyzed. _Reparandum_ and _dep_ are neither of semantic nor syntactic nature and we cannot make any assumptions of their content. _Punct_ and _discourse_ are removed for similar reasons, but also due to particles often being ignored in other evaluation schemes.

## Placing dependency relations on a function--content spectrum

Next question to answer is if we can motivate our classification not only on linguistic intuition and the specification of dependency relations, but also from an empirical perspective. We do this by adhering to our previous definition on function dependencies, and what we know of the nature of function words. Since they are part of closed word classes, meaning new words rarely get introduced into their categories, we can expect the number of distinct word types to be quite small, especially when compared to the word classes shared by typical content words such as _nsubj_. 

\begin{figure}[t]
\centering
\input{figures/inverse_word_entropy.pgf}
\label{fig:averaged_wde}
\caption{Averaged word dependency entropy for all universal dependency relations, with the manually created categories.}
\end{figure}

\begin{figure}[t]
\hspace*{-1cm}
\input{figures/standard_ttr.pgf}
\label{fig:standard_ttr}
\caption{Standardized type/token ratio for chunks of 1000 tokens (blue) and content dependency (green). $R=0.27$}
\end{figure}


Assuming this holds, we expect that the probability of a word given a function relation to be zero for all but a few cases, while the probability of a word given a content relation should be much more evenly spread. This can be quantified by measuring a relation's entropy given its word probabilities. We call this measure _word dependency entropy_ (WDE). Calculated for all treebanks we get the averaged WDE. 

Here we formally define word dependency entropy. A probability distribution $p$ takes as input a word $w$ conditioned on a treebank $t \in T$, and a dependency relation $r$. $H$ is the entropy function that takes $p(w|r,t)$ as input and calculates its entropy. The entropy function is normalized by its upper bound $\log n_w$, where $n_w$ is the size of the vocabulary. This keeps the range of the function to $[0,1]$. To calculate the WDE for a set of treebanks, we average WDE for all treebanks $t \in T$. In the case a dependency relation is not present in a treebank, we set its WDE to 0.5 to imply that it is neither a content nor a function relation.

This gives us the following mathematical functions:

$$\mbox{WDE}(r,t) = \dfrac{H(p(w|r,t))}{\log n_w}$$

$$\mbox{Averaged WDE}(r, T) = \dfrac{1}{n_T} \sum_{t \in T}{\mbox{WDE}(r,t)}$$

The averaged WDE for UD 1.2 is presented in figure \ref{fig:averaged_wde}, along with our manual categorization of dependency relations. Ignoring the _other_ relations, we find that the WDE gives an intuitive ordering of the dependency relations, while empirically supporting our choice of content and function relations.

## Finding correlation with external measurements

We would expect the ratio of function words in a given language's treebank to correlate with its degree of synthesis. Measuring degree of synthesis is not a trivial task, and there have been several proposed algorithms for this. Despite having obvious drawbacks, an often used indirect measurement of degree of synthesis is the type/token ratio [@kettunen_can_2014]. This assumes that synthetic languages, with their morphologically rich systems, will have fewer tokens per word than analytic languages such as English or Hindi. This is not particularly robust when comparing across corpora of different sizes. As such, we will be using the _standardized_ type/token ratio (STTR), which calculates average TTR in chunks of 1000 tokens\footnote{Introduced by Mike Scott in \url{http://lexically.net/downloads/version6/HTML/index.html?type_token_ratio_proc.htm}}. Figure \ref{fig:standard_ttr} shows that there is a weak correlation between languages' frequency ratio of function relations and their STTR. Some languages are clear outliers such as Old Church Slavonic, Arabic, Gothic, Persian, English, and Hindi. Whether this is a result of a bad degree of synthesis measurement, a bad classification of function dependency relations, or a combination of both is up for discussion. 

## Alternative evaluation metrics

Based on the previous findings, we propose two alternative metrics to the LAS. The first metric is based on our manual classification of content and function dependencies, while the latter is exploiting the weights outputted by the WDE.

#### Precision and recall of content relations

In this metric, we look at the precision and recall for all content dependency relations, ignoring any relation that is not a part of this class. Since not all dependency relations are involved, the precision and recall can differ and thus become interesting to analyze separately. We call these _content precision_ and _content recall_.

#### Weighting relations by their WDE

We weight each dependency relation by its averaged WDE as presented in figure \ref{fig:averaged_wde}. This will increase the importance of content relations, while the function relations provide less to the overall score. We call this the _Weighted Labeled Attachment Score_ (WLAS). Using WLAS has the additional interesting property of also being easily calculated and deployable to non-UD frameworks.

# Parsing results

<!-- Overall las scores -->
\begin{figure*}[t]
\centering
\input{figures/content_las_comparison.pgf}
\label{fig:content_las_comparison}
\caption{Overall LAS, WLAS, precision and recall for content dependencies. Sorted by WLAS.}
\end{figure*} <!-- TODO: Sort by LAS. Recalculate to make sure punct is not present. -->


<!-- Cumulative variance -->
\begin{figure}[t]
\centering
\input{figures/cumul_vars.pgf}
\label{fig:cumul_vars}
\caption{Cumulative variance when adding languages in a top-scoring order.}
\end{figure}

<!-- Correlation matrix -->
\begin{table}[t]
\centering
\resizebox{\columnwidth}{!}{
    \input{tables/res_corrs.latex}
}
\label{tbl:res_corrs}
\caption{Pearson correlation matrix for content and function frequency ratio, content precision and recall, function precision and recall, LAS, and WLAS. Correlation measured across languages. Boldfaced figures are mentioned in the discussion.}
\end{table}

Figure \ref{fig:content_las_comparison} lists the parsing results for all languages, with LAS, WLAS, and content precision and recall. We can tell that WLAS is consistently providing larger scores for each output than LAS, while the content precision and recall scores are substantially lower. Despite the lower significance of functional dependencies, even including them at all gives a good performance boost for the measurment. There are small differences for precision and recall for all except the worst performing languages where,given the higher recall, the parsing model seems to have a bias towards content dependencies.

By studying figure \ref{figure:function-parsing-ratio}, we see that there is a clear correlation between the frequency ratio of function relations in a language with its precision of the same relation class. What is interesting is that this does not hold when looking at content relations, as seen in figure \ref{figure:content-parsing-ratio}. This suggests that languages with a high degree of function dependency relations has an unfair advantage when comparing attachment scores across languages.

<!-- Below not finished -->

Figure \ref{fig:results} shows how the variance for high performing languages has decreased, while the overall variance has not been affected when looking at the whole language spectrum. 

One hypothesis for why we do not see a relative decrease that is correlated to their sTTR values is that the function words works better as a structure to make a better classification for the content words. 

# Discussion

A natural question that comes up is whether we should use function weights as determined by the average WDE across many languages, or if it would be beneficial to let language specific WDE produce each language's weights.

# Conclusion

In this paper we have presented experiments that suggest that languages with many function dependency relations are easier to parse than languages with richer morphology, given current parser models. We have motivated the necessity for new evaluation metrics that takes this into account from a typological perspective, while also referring to research that motivates this from human judgment standards. We suggested two new evaluation metrics that raise the importance of content dependency relations with some initial experiments indicating their usefulness.

# Acknowledgements

We thank Jörg Tiedemann for providing his parsing output on UD 1.0 for initial experiment development.

\section*{References}

<!-- \begin{figure}[t]
\centering
\resizebox{\columnwidth}{!}{\input{figures/function_ratio_vs_function_precision.pgf}}
\caption{Precision of functional dependency relations, and the frequency ratio of functional dependency relations for each language. $R=0.67$}
\label{figure:function-parsing-ratio}
\end{figure}
 -->

<!-- \begin{figure}[t]
\centering
\resizebox{\columnwidth}{!}{\input{figures/content_deprel_las_ratio_corr.pgf}}
\caption{Precision of content dependency relations, and the frequency ratio of content dependency relations for each language. $R=-0.33$}
\label{figure:content-parsing-ratio}
\end{figure}
 -->

<!-- \begin{table*}[t]
\resizebox{\textwidth}{!}{
    \input{tables/maltdefault_results.latex}
}
\caption{Overall LAS score, precision and recall for content dependencies.}
\end{table*} -->

---
title: "A typological perspective on evaluation for Universal Dependencies"
author:
- name: Jimmy Callin
  affiliation: Uppsala University
  email: jimmy.callin@gmail.com
tags: [universal dependencies, parsing, evaluation, dependency, attachment score]
abstract: |
  Established evaluation metrics assumes that all dependency relations are equally important. Furthermore, when comparing parsing results in a cross-linguistic manner, it is easy to assume equal attachment scores is equivalent to equal performance. We demonstrate why this is not the case, especially when comparing languages with large difference in morphological complexity, and emphasize the necessity for new evaluation metrics that takes these considerations into account. We also present two alternative evaluation metrics motivated by these findings.
bibliography: bibliography.bib
---

# Introduction

The role of language processing is becoming increasingly multi-lingual. This is reflected in recent efforts into providing dependency parsing frameworks that can reliably be applied on a multitude of languages. One of the currently most ambitious projects in this area is the Universal Dependencies (UD) framework [@nivre_universal_2015], where the goal is to create a parsing framework with a cross-linguistically consistent grammatical annotation. The purpose of this work is to remove the requirement of language specific components which has up to this point been a necessity due to inconsistent annotation standards.

Data-driven evaluation metrics have been used as long as the availability of treebanks (see @collins_headdriven_1999 chap. 4 and @carroll_parser_1998 for surveys on early results). To evaluate statistical parsing models, _Unlabeled Attachment Score_ (UAS) has been in use under different names since the early days. @eisner_empirical_1997 was first to call it attachment score, which refers to work done by @lin_dependencybased_1998. _Labeled Attachment Score_ (LAS) was first introduced in @nivre_memorybased_2004 to emphasize the importance of correct labeling. UAS is defined as the accuracy of correct attachments in a test collection, while LAS includes the additional constraint of requiring a correct attachment label. These have in their simplicity and intuitiveness served the research area well, but their design relies on a number of assumptions we argue do not hold in the context of UD.

\begin{figure}
\begin{center}
\begin{dependency}
   \begin{deptext}[column sep=1em]
      Ammuin \& elefantin \& pyjamassani \& . \\
      \emph{I shot} \& \emph{an elephant} \& \emph{in my pajamas} \& . \\
   \end{deptext}
   \deproot{1}{ROOT}
   \depedge{1}{2}{dobj}
   \depedge{1}{3}{nmod}
   \depedge{1}{4}{punct}
\end{dependency}

\end{center}
\caption{Finnish dependency tree for \emph{I shot an elephant in my pajamas}. Note the edge count of Finnish being 4, while the English edge count is 8.}
\label{finnishparsing}
\end{figure}

Firstly, the design of attachment scores assumes that we know next to nothing about the taxonomy and design choices of the parsing framework. This has historically been necessary since there have not been a consistently adapted framework for dependency parsing across many languages. We argue that recent progress in UD has made this assumption invalid. UD has a carefully specified framework that all UD treebanks have to adapt, and we can exploit this constraint to learn more about the performance of a model.

Secondly, parsing results are increasingly juxtaposed in a cross-linguistic manner, and this trend will likely continue with the establishment of UD. It is not uncommon to compare the output of e.g. English and Finnish under the assumption that equal evaluation scores is equivalent to equal parsing performance. The reason why this is problematic becomes apparent when studying grammatical morphemes in languages where these may be unbounded (i.e. function words) with languages where they typically are bounded on content words (i.e. affixes).

In figure \ref{finnishparsing}, we have a Finnish sentence with four edges, while the equivalent sentence in English requires a total of eight edges. The problem appears as soon as we introduce a parsing error into the trees: one faulty edge in the Finnish sentence would result in a performance reduction of 25%, while the same error in the English sentence only would reduce the accuracy by 12.5%. Function words are regular in their appearance, and should therefore be relatively easy for a model to parse correctly. Our hypothesis is that languages with a comparatively large number of function words, like English, receive a more or less free performance boost when using classic evaluation metrics.

Based on these intuitions, our aim is to contribute to these two questions:

- How much do languages with a large number of unbounded grammatical morphemes benefit from current evaluation schemes?
- Would focusing on correct classification of content word dependencies be a better evaluation scheme for cross-linguistic parsing performance?

# Related work

Not much work has been done in cross-linguistic evaluation, and papers presenting evaluation scores on several languages simply use previously available metrics without analyzing their shortcomings in such a context. Before the work on UD was initiated, there have been several attempts at automatic normalization of dependency treebanks into a common format for a more robust evaluation [@zeman2012hamledt]. In light of this work on cross-linguistically consistent annotation frameworks, @tsarfaty_evaluating_2011 take a separate approach with cross-framework evaluation, where they suggest an evaluation technique that is robust towards differing annotation criteria. 

Since UAS arguably has been more popular of the two attachment scores, finding performance results on subsets of labeled dependency relations is difficult. In cases of extensive error analysis it is possible to find sections devoted to this [@plank_domain_2011, chapter 6.6]. There have also been work looking at specific constructions, e.g. unbounded dependency evaluation [@nivre_evaluation_2010], where they argue that some dependency relations are more critical for a parser to get right than others.

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

A total of 15 treebanks were removed. 5 of these had too few tokens, 4 lacked features, 2 had too many non-projective trees, while 4 treebanks were language duplicates. This leaves us with the 22 languages listed in table \ref{tbl:ud-treebanks}. Most notably we lost the French and German treebanks.

For measuring the correlation of metrics to manual evaluation, we will be using parts of the human judgment data as provided by @plank_dependency_2015. Not all languages in the dataset are from the UD treebanks, thus only English, German, and Spanish are used.

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


# Categorizing dependency relations

We motivate our categorization into categories of function and content relations based on the specification of universal dependency relations\footnote{\url{http://universaldependencies.github.io/docs/u/dep/index.html}}, linguistic intuition, and a newly developed statistical method. First, let us define what we consider to be function and content relations:

- A _function relation_ is a relation that links a word with a function word.
- A _content relation_ is a relation that either has _root_ as its head, or links a content word with another content word.

## Categorization by specification

Given the previous definition as well as the specification of universal dependency relations, we can categorize a relation based on how it should occur in UD treebanks. Going through each dependency relation in this manner we ended up with a classification as presented in table \ref{tbl:dependency-relations}. 

We chose to remove some relations where we cannot make assumptions of its content, labeled _other_. The _foreign_ relation has no restrictions on what type of word it should choose as a dependent as long as it is a foreign word. _List_ is used in cases where the content cannot be easily analyzed. _Reparandum_ and _dep_ are neither of semantic nor syntactic nature and we cannot make any assumptions of their content. _Punct_ and _discourse_ are removed for similar reasons, but also due to particles often being ignored in other evaluation schemes.

## Placing dependency relations on a function--content spectrum

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
\caption{Standardized type/token ratio for chunks of 1000 tokens (blue), with content relation frequency ratio (green) and function relation frequency ratio (red). High STTR score implies high morphological complexity. $R(\mbox{Content freq}, \mbox{STTR}) = 0.27$, $R(\mbox{Function freq}, \mbox{STTR}) = -0.57$.}
\label{fig:standard_ttr}
\end{figure}


Assuming this holds, we expect that the probability of a word given a function relation to be zero for all but a few cases, while the probability of a word given a content relation should be much more evenly spread. This can be quantified by measuring a relation's entropy given its word probabilities. We call this measure _word dependency entropy_ (WDE). Calculated for all treebanks we get the averaged WDE. 

Here we formally define word dependency entropy. A probability distribution $p$ takes as input a word $w$ conditioned on a treebank $t \in T$, and a dependency relation $r$. $H$ is the entropy function that takes $p(w|r,t)$ as input and calculates its entropy. The entropy function is normalized by its upper bound $\log n_w$, where $n_w$ is the size of the vocabulary. This keeps the range of the function to $[0,1]$. To calculate the WDE for a set of treebanks, we average WDE for all treebanks $t \in T$. In the case a dependency relation is not present in a treebank, we set its WDE to 0.5 to imply that it is neither a content nor a function relation.

This produces the following mathematical functions:

$$\mbox{WDE}(r,t) = \dfrac{H(p(w|r,t))}{\log n_w}$$

$$\mbox{Averaged WDE}(r, T) = \dfrac{1}{n_T} \sum_{t \in T}{\mbox{WDE}(r,t)}$$

The averaged WDE for UD 1.2 is presented in figure \ref{fig:averaged_wde}, along with our manual categorization of dependency relations. Ignoring the _other_ relations, we find that the WDE gives an intuitive ordering of the dependency relations, while empirically supporting our choice of content and function relations.

<!-- Overall las scores -->
\begin{figure*}[t]
\centering
\includegraphics{figures/content_las_comparison.pdf}
\caption{Overall LAS, WLAS, precision and recall for content dependencies. Sorted by LAS.}
\label{fig:content_las_comparison}
\end{figure*}


## Finding correlation with external measurements

We would expect the ratio of function words in a given language's treebank to correlate with its degree of synthesis. Measuring degree of synthesis is not a trivial task, and there have been several proposed algorithms for this. Despite having obvious drawbacks, an often used indirect measurement of degree of synthesis is the type/token ratio [@kettunen_can_2014]. This assumes that synthetic languages, with their morphologically rich systems, will have fewer tokens per word than analytic languages such as English or Hindi. This is not particularly robust when comparing across corpora of different sizes. As such, we will be using the _standardized_ type/token ratio (STTR), which calculates average TTR in chunks of 1000 tokens\footnote{Introduced by Mike Scott in \url{http://lexically.net/downloads/version6/HTML/index.html?type_token_ratio_proc.htm}}. Figure \ref{fig:standard_ttr} shows that there is a weak correlation between languages' frequency ratio of content relations and their STTR, while the negative correlation against ratio of function relations is much stronger. Some languages for content relations are clear outliers such as Old Church Slavonic, Arabic, Gothic, Persian, English, and Hindi. We are not certain of why the ratio correlation is stronger for function relations than for content relations. Whether this is a result of a bad degree of synthesis measurement, a bad classification of  content dependency relations, or a combination of both is up for discussion. 


# Experimental setup

Based on the previous findings, we propose two alternative metrics to the LAS. The first metric is based on our manual classification of content and function dependencies, while the latter is exploiting the weights outputted by the WDE.

#### Performance of content relations

In this metric, we look at the precision and recall for all content dependency relations, ignoring any relation that is not a part of this class. Since not all dependency relations are involved, the precision and recall can differ and thus become interesting to analyze separately. We call these _content precision_ and _content recall_.

#### Weighting relations by their WDE

We weight each dependency relation by its averaged WDE as presented in figure \ref{fig:averaged_wde}. This will increase the importance of content relations, while the function relations provide less to the overall score. We call this the _Weighted Labeled Attachment Score_ (WLAS). Using WLAS has the additional interesting property of also being easily calculated and deployable to non-UD frameworks.

For testing the evaluation metrics, we train MaltParser 1.7 using Nivre Arc-Eager with default settings on each treebank's training data and parse the included test data [@nivre2006maltparser]. Before continuing, we must split up the UD dependency relations into categories of function and content relations. 


# Evaluation


Figure \ref{fig:content_las_comparison} lists the parsing results for all languages, with LAS, WLAS, and content precision and recall. We can tell that LAS is consistently providing higher scores for each output compared to WLAS, while the content precision and recall scores are substantially lower. There are small differences for precision and recall for all except the worst performing languages where, given the higher recall, the parsing model seems to have a bias towards content dependencies.

Table \ref{tbl:res_corrs} lists the Pearson correlation coefficient between treebanks for WLAS, LAS, content relations precision and recall, function relations precision and recall, and the frequency ratio of content and function relations in the treebanks. The correlation between the various suggested measurements, as well as with LAS, are quite strong. The content relations frequency has a strong negative correlation with function relations frequency, and negative across all the other measurements as well. Function relations frequency has more or less strong positive correlations with all metrics.

Figure \ref{fig:cumul_vars} shows what happens with the variance when cumulatively adding languages in a top-scoring fashion for each measurement. For content precision and recall as well as WLAS, the variance is lower for high performing languages, but takes off for content precision and recall when you get past the first eleven treebanks. WLAS keeps a lower score compared with LAS until the end where it joins LAS in a variance of 0.0045.

Table \ref{tbl:human_judgment} lists Spearman correlations between manual evaluation of two parser models, where the evaluators given parsed sentences in each case chose which of two parser models they consider to provide the best output. Content precision and recall are in all cases except one inferior to LAS and WLAS, where the two latter are indistinguishable.


<!-- Correlation matrix -->
\begin{table}[t]
\centering
\resizebox{\columnwidth}{!}{
    \input{tables/res_corrs.latex}
}
\caption{Pearson correlation matrix between treebanks for content and function frequency ratio, content precision and recall, function precision and recall, LAS, and WLAS. Boldfaced figures are mentioned in the discussion.}
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

# Discussion

Looking at function frequency and its precision in table \ref{tbl:res_corrs}, they have a correlation of $0.67$. This suggests that the larger rate of function words in a language, the easier it is to parse its function words. What is interesting is that this does not hold when looking at content frequency and its precision where one might expect that there is a strong positive correlation which would indicate that a high degree of content relations makes it easier to parse these classes. Instead, we find a weak negative correlation of $-0.25$. Furthermore, given languages' LAS scores, the more function words there is in a language, the better it performs. Even when looking at the relation between the amount of function words in a language with how well it does on content words, the correlation is weakly positive. We take this to mean that our choice of parser, while not explicitly tuned for any particular language, still benefits from a context with a high rate of grammatical function words. These findings support our hypothesis, that languages with a high degree of function dependency relations has an unfair advantage when comparing attachment scores across languages.

Regarding the evaluation scores for different evaluation metrics, as presented in figure \ref{fig:content_las_comparison}, it is difficult to tell if any metric is better than the other. One might expect that the scoring difference of LAS and WLAS, or LAS and content performance, would correlate with its STTR score, since analytic languages like Hebrew and English have more to lose on decreasing the importance of function words. Unfortunately, this correlation is rather weak. Assuming that the STTR scoring is reliable, we believe this has to do with what we described above: languages with a high rate of function words provide a better context for content words for parsers. 

Going back to table \ref{tbl:res_corrs}, a better measurement than LAS would be expected to have a weaker correlation with the function frequency ratio, showing that the importance of the amount of function words in a language decrease. While WLAS stays on the same level of correlation as LAS, content performance is much weaker.

We ran the measurements on the human judgment data with the results given in table \ref{tbl:human_judgment}. Unfortunately, none of the metrics seems to improve upon the LAS score, which was the top scoring metric reported in the original paper. Only content recall sees some improvements over LAS for English, but other than that the results are either worse or equal to those of LAS. WLAS has overall very small changes compared to LAS, which is somewhat surprising given that the original paper commented on content relations being considered more important than function relations by the manual evaluators. This could possibly be explained by function relations overall performing quite well, and whenever there are erroneous function relations they are cascaded from faulty content relations. This hypothesis is as of yet untested.

Another approach is to look at the variance of the metrics. If our initial hypothesis holds, this should mean that some of the differences found between languages before evens out, and thereby lowering the variance when compared to LAS. As figure \ref{fig:cumul_vars} shows this does not hold when looking at all treebanks, but by cumulatively adding treebanks it is possible to study the effect as the performance decreases. This shows indeed that the variance is much lower among high-performing languages for WLAS and and content performance. This could potentially be explained by that differences among top-scoring languages are much less random due to a poor parsing model, and it is first among these that the effects of choice of metric really matters.

That brings us to the choice of parser model and its effect on the results. In the name of consistent treebanks, we chose to remove treebanks with a large number of non-projective trees. Another motivation was that our parser can not handle these types of trees especially well, and the results are thus unreliable when comparing across languages. Is is quite possible, and even probable, that there are many similar factors playing a role in the discussed results. In future work, we should reproduce these results with alternative models and look for any similarities or differences that might strengthen our claims or explain some of the peculiarities we have seen in this work.

# Conclusion

In this paper we have presented experiments that suggest that languages with many function dependency relations are easier to parse than languages with richer morphology, given current parser models. We have motivated the necessity for new evaluation metrics that take these considerations into account from a typological perspective, while also referring to research that motivates this from human judgment standards. We suggested two new evaluation metrics that raise the importance of content dependency relations with some initial experiments indicating their usefulness.

# Acknowledgements

We thank Jörg Tiedemann for providing his parsing output on UD 1.0 for initial experiment development.

\section*{References}

pandoc --latex-engine="xelatex" \
       --template="default.latex" \
       proposal.md \
       -o "proposal.pdf" \
       --bibliography="bibliography.bib" \
       --variable="geometry:margin=3cm" \
       --variable="geometry:a4paper" \
       --csl="association-for-computational-linguistics.csl" \
       && echo "Compiled to proposal.pdf"

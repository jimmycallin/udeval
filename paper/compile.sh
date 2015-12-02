export TEXINPUTS=$(pwd)/templates/:$TEXINPUTS
pandoc --latex-engine="pdflatex" \
       --template="templates/acl2012.tex" \
       --bibliography="bibliography.bib" \
       --csl="templates/acl.csl" \
       paper.md -o paper.pdf

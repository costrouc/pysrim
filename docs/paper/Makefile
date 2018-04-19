# A simplified makefile

input	  := paper.md
output	  := paper.pdf
docoutput := paper.docx
bib	  := paper.bib

pdf: $(output)
doc: $(docoutput)

$(output): $(input) $(bib) Makefile
	pandoc \
	-o $(output) \
	--pdf-engine=xelatex \
	--filter pandoc-citeproc $(input)


$(docoutput): $(input) $(bib) Makefile
	pandoc \
	-o $(docoutput) \
	--filter pandoc-citeproc $(input)


autorefresh:;
	((ls $(input) $(bib) | entr make $(output)) &)

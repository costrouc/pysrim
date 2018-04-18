# A simplified makefile

input	:= paper.md
output	:= paper.pdf
bib	:= paper.bib


$(output): $(input) $(bib) Makefile
	pandoc \
	-o $(output) \
	--pdf-engine=xelatex \
	--filter pandoc-citeproc $(input)


autorefresh:;
	((ls $(input) $(bib) | entr make $(output)) &)

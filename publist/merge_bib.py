import sys
import os
if len(sys.argv) < 3:
    print("Usage: python {0} strat end".format(sys.argv[0]))
    exit(-1)
bib_file = open("publications.bib", "w", encoding="utf-8")
s_year = (int)(sys.argv[1])
e_year = (int)(sys.argv[2])
for year in range(s_year, e_year+1):
    f_name = "kgwg_publications_"+str(year)+"_full.bib"
    with open(f_name, "r", encoding="utf-8") as f:
        bib = f.read()
        bib_file.write(bib)
        print("File : {0} content:\n{1}".format(f_name, bib))
bib_file.close()

html_file = "publications.tex"
html_file_root = "publications"
with open(html_file, "w", encoding="utf-8") as text_file:
    text_file.write("\\documentclass{revtex4}\n")
    text_file.write("\\begin{document}\n")
    text_file.write("\\nocite{*}\n")
    text_file.write("\\newcommand{\\apjl}{Astrophys. J. Letter}\n")
    text_file.write("\\newcommand{\\aap}{Astron. \& Astrophys. J.}\n")
    text_file.write("\\newcommand{\\mnras}{Mon. Not. R. Astron. Soc.}\n")
    text_file.write("\\newcommand{\\nar}{New Astronomy Reviews}\n")
    text_file.write("\\newcommand{\\memsai}{Memorie della Societa Astronomica Italiana}\n")
    text_file.write("\\newcommand{\\grl}{Geophysical Research Letters}\n")
    text_file.write("\\newcommand{\\pasj}{Publications of the Astronomical Society of Japan}\n")
    text_file.write("\\newcommand{\\texttimes}{X}\n")
    text_file.write("{\\huge List of Publications}\n")
    text_file.write("\\bibliographystyle{unsrt}\n")
    text_file.write("\\bibliography{"+html_file_root+"}\n")
    text_file.write("\\end{document}\n")

os.system("pdflatex "+html_file)
os.system("bibtex "+html_file_root)
os.system("pdflatex "+html_file)
os.system("pdflatex "+html_file)

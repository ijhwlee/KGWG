import sys
import os
import requests
from datetime import datetime

MIN_AUTHORS_COLL = 100 

if len(sys.argv) > 1 and not sys.argv[1].isnumeric():
  print("Usage: python3 {0} yyyy [file_name]\n       Second argument should be a number(zero for the current year).".format(sys.argv[0]))
  exit(-1)

ads_key_file_name = ".ads_key.dat"
if os.path.exists(ads_key_file_name):
  pass
else:
  print("ERROR- ADS API key file {0} does not exist, please specify a correct file name.".format(ads_key_file_name))
  exit(-1)
with open(ads_key_file_name, "r") as key_file:
  lines = key_file.read()
  keys = lines.split('\n')
token = keys[0]
#print("[DEBUG-hwlee]token = {0}".format(token))

current_year = datetime.now().year
if len(sys.argv) > 1:
  current_year = int(sys.argv[1])
if current_year == 0:
  current_year = datetime.now().year
current_month = datetime.now().month
current_month_text = datetime.now().strftime('%h')
author_file_name = "kgwg_authors.dat"
if len(sys.argv) > 2:
  author_file_name = sys.argv[2]
if os.path.exists(author_file_name):
  pass
else:
  print("ERROR- Author list file {0} does not exist, please specify a correct file name.".format(author_file_name))
  exit(-1)

exclude_file_name = "kgwg_excl_journals.dat"
if os.path.exists(exclude_file_name):
  pass
else:
  exclude_file_name = ""
  print("WARNING- Exclude jouranl list file {0} does not exist, please specify a correct file name.\n      No journal will be excluded, so the list may include wrong ones".format(exclude_file_name))

exclude_bibcode_file_name = "kgwg_excl_bibcodes.dat"
if os.path.exists(exclude_bibcode_file_name):
  pass
else:
  exclude_bibcode_file_name = ""
  print("WARNING- Exclude bibcode list file {0} does not exist, please specify a correct file name.".format(exclude_bibcode_file_name))

exclude_title_word_file_name = "kgwg_excl_title_words.dat"
if os.path.exists(exclude_title_word_file_name):
  pass
else:
  exclude_title_word_file_name = ""
  print("WARNING- Exclude title word list file {0} does not exist, please specify a correct file name.".format(exclude_title_word_file_name))

filter_file_name = "kgwg_filter.dat"
if os.path.exists(filter_file_name):
  pass
else:
  filter_file_name = ""
  print("WARNING- Extra filter file {0} does not exist, please specify a correct file name.\n      No extra filter will be applied.".format(filter_file_name))

def get_extra_filter(file_name):
  exclude_journals = []
  if len(file_name) > 0:
    with open(file_name, "r") as author_file:
      lines = author_file.read()
      authors = lines.split('\n')
    exclude_journals = [author for author in authors if len(author)>0]
  return exclude_journals

def get_exclude_title_words(file_name):
  exclude_journals = []
  if len(file_name) > 0:
    with open(file_name, "r") as author_file:
      lines = author_file.read()
      authors = lines.split('\n')
    exclude_journals = [author for author in authors if len(author)>0]
  return exclude_journals

def get_exclude_journals(file_name):
  exclude_journals = []
  if len(file_name) > 0:
    with open(file_name, "r") as author_file:
      lines = author_file.read()
      authors = lines.split('\n')
    exclude_journals = [author for author in authors if len(author)>0]
  return exclude_journals

def get_exclude_bibcodes(file_name):
  exclude_journals = []
  if len(file_name) > 0:
    with open(file_name, "r") as author_file:
      lines = author_file.read()
      authors = lines.split('\n')
    exclude_journals = [author for author in authors if len(author)>0]
  return exclude_journals

def get_title(bibitem):
  lines = bibitem.split('\n')
  for line in lines:
    if 'title' in line:
      start = line.find('"{')
      end = line.find('}",$')
      title = line[start+2: end-2]
      #print("Title = {0}".format(line))
      #print("Extracted = {0}".format(title))
      return title

def get_author(bibitem):
  lines = bibitem.split('\n')
  for line in lines:
    if 'author' in line:
      start = line.find('= {')
      end = line.find('},$')
      title = line[start+3: end-1]
      #print("Author before : {0}".format(title))
      title = title[1:]
      title = title.replace(" {", " ")
      title = title.replace("},", ",")
      title = title.strip()
      #print("Author after : {0}".format(title))
      return title

def get_volume(bibitem):
  title = ""
  lines = bibitem.split('\n')
  for line in lines:
    if 'volume' in line:
      start = line.find('= {')
      end = line.find('},$')
      title = line[start+3: end-1]
      #print("Volume : {0}".format(title))
      return title
  return title; # not exist volume PROCEEDINGS case

def get_adsurl(bibitem):
  title = ""
  lines = bibitem.split('\n')
  for line in lines:
    if 'adsurl' in line:
      start = line.find('= {')
      end = line.find('},$')
      #print("adsurl : {0}".format(line))
      title = line[start+3: end-1]
      #print("adsurl extracted : {0}".format(title))
      return title
  return title; # not exist volume PROCEEDINGS case

def get_year(bibitem):
  title = ""
  lines = bibitem.split('\n')
  for line in lines:
    if 'year' in line:
      start = line.find('= ')
      end = line.find(',$')
      title = line[start+2: end]
      #print("Year : {0}".format(title))
      return title
  return title; # not exist year not proper bibitem

def get_pages(bibitem):
  title = ""
  lines = bibitem.split('\n')
  for line in lines:
    if 'pages' in line:
      start = line.find('= {')
      end = line.find('},$')
      #print("Pages : {0}".format(line))
      title = line[start+3: end-1]
      #print("Pages extracted : {0}".format(title))
      return title
  return title; # not exist pages

def convert_journal(journal):
  if '\\prd' in journal:
    return "Phys. Rev. D"
  elif '\\prl' in journal:
    return "Phys. Rev. Lett."
  elif '\\prx' in journal:
    return "Phys. Rev. X"
  elif '\\pra' in journal:
    return "Phys. Rev. A"
  elif '\\prb' in journal:
    return "Phys. Rev. B"
  elif '\\apj' in journal:
    return "Astro. Phys. J."
  elif '\\apjl' in journal:
    return "Astro. Phys. J. Lett."
  elif '\\apjs' in journal:
    return "Astro. Phys. J. Supp."
  elif '\\aap' in journal:
    return "Astro. Astrophys."
  elif '\\mnras' in journal:
    return "Mon. Not. Roy. Astro. Soc."
  elif '\\nar' in journal:
    return "New Astronomy Reviews"
  elif '\\memsai' in journal:
    return "Memorie della Societa Astronomica Italiana"
  else:
    return journal

def get_journal(bibitem):
  lines = bibitem.split('\n')
  ref_type = ""
  for line in lines:
    if 'ARTICLE' in line:
      ref_type = 'ARTICLE'
    elif 'BOOK' in line:
      ref_type = 'BOOK'
    elif 'INPROCEEDINGS' in line:
      ref_type = 'INPROCEEDINGS'
    elif 'PROCEEDINGS' in line:
      ref_type = 'PROCEEDINGS'

    if ref_type=='ARTICLE' and 'journal' in line:
      start = line.find('= {')
      end = line.find('},$')
      title = line[start+3: end-1]
      title = convert_journal(title)
      return title
    if ref_type=='BOOK' and 'title' in line:
      start = line.find('"{')
      end = line.find('}",$')
      title = line[start+2: end-2]
      return title
    if ref_type=='INPROCEEDINGS' and 'booktitle' in line:
      start = line.find('= {')
      end = line.find('},$')
      title = line[start+3: end-1]
      return title
    if ref_type=='PROCEEDINGS' and 'booktitle' in line:
      start = line.find('= {')
      end = line.find('},$')
      title = line[start+3: end-1]
      return title
  return "NO TITLE"

def generate_list_item(text_file, bibitem, bibcode):
  text_file.write("<li>")
  #text_file.write("<a href='https://ui.adsabs.harvard.edu/#abs/{0}/abstract' target='_blank'>{1}</a>\n".format(bibcode, get_title(bibitem)))
  adsurl = get_adsurl(bibitem)
  if adsurl == "":
    text_file.write("<a href='https://ui.adsabs.harvard.edu/#abs/{0}/abstract' target='_blank'>{1}</a>\n".format(bibcode, get_title(bibitem)))
  else:
    text_file.write("<a href='{0}' target='_blank'>{1}</a>\n".format(adsurl, mk_link_string(bibitem, True)))
  text_file.write("</li>\n")

def generate_ol(year, bibitems, bibcodes):
  html_file = "kgwg_publications_"+str(year)+"_ol.html"
  with open(html_file, "w") as text_file:
    text_file.write("<ol>\n")
    for idx in range(len(bibitems)):
      generate_list_item(text_file, bibitems[idx], bibcodes[idx])
    text_file.write("</ol>\n")

def generate_full(year, bibitems, bibcodes):
  html_file = "kgwg_publications_"+str(year)+"_full.html"
  if len(bibitems) > 0:
    with open(html_file, "w") as text_file:
      text_file.write("<ol>\n")
      for idx in range(len(bibitems)):
        generate_list_item(text_file, bibitems[idx], bibcodes[idx])
      text_file.write("</ol>\n")
  else:
    with open(html_file, "w") as text_file:
      text_file.write("<p>\n")
      text_file.write("No publications found.</p>\n")

def generate_short(year, bibitems, bibcodes):
  html_file = "kgwg_publications_"+str(year)+"_short.html"
  if len(bibitems) > 0:
    with open(html_file, "w") as text_file:
      text_file.write("<ol>\n")
      for idx in range(len(bibitems)):
        generate_list_item(text_file, bibitems[idx], bibcodes[idx])
      text_file.write("</ol>\n")
  else:
    with open(html_file, "w") as text_file:
      text_file.write("<p>\n")
      text_file.write("No publications found.</p>\n")

#def generate_html(year, bibitems, bibcodes):
def generate_html(year, bibitems_full, bibcodes_full, bibitems_short, bibcodes_short):
  html_file = "kgwg_publications_"+str(year)+".html"
  ol_file = "kgwg_publications_"+str(year)+"_ol.html"
  with open(html_file, "w") as text_file:
    text_file.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n<title>Year {0}: List of Publications for KGWG</title></head>\n".format(year))
    # writing script
    text_file.write("<script type=\"text/javascript\" src=\"./includeHtml.js\"></script>\n")
    text_file.write("</head>\n")
    text_file.write("<body>\n<h1>List of Publications for KGWG in year {0}</h1>\n".format(year))
    #text_file.write("<ol>\n")
    #for idx in range(len(bibitems)):
    #  generate_list_item(text_file, bibitems[idx], bibcodes[idx])
    #text_file.write("</ol>\n")
    text_file.write("<div w3-include-html=\"./{0}\"></div>\n".format(ol_file))
    text_file.write("<script>includeHTML();</script>\n")
    text_file.write("</body>\n")
  #generate_ol(year, bibitems, bibcodes)
  generate_full(year, bibitems_full, bibcodes_full)
  generate_short(year, bibitems_short, bibcodes_short)

def get_bibitem_list(bibitems):
  #bibitems1 = bibitems.split('@')
  bibitems1 = []
  bib_lines = bibitems.split('\n')
  bibitem = ""
  for idx in range(len(bib_lines)):
    this_line = bib_lines[idx]
    if this_line.startswith('@'):
      if bibitem.startswith('@'):
        bibitem += "\n"
        bibitems1.append(bibitem)
      bibitem = this_line
    elif len(this_line)>0:
      bibitem += "\n"+this_line
  if bibitem.startswith('@'):
    bibitem += "\n"
    bibitems1.append(bibitem)
  return bibitems1

def get_bibcodes(author, year):
  extra_filter = get_extra_filter(filter_file_name)
  if len(extra_filter) == 0: # use default author and year query
    #print("Using standard query using authors and year.")
    url = "https://api.adsabs.harvard.edu/v1/search/query?q=(%3Dauthor%3A%22"+author+"%22%20AND%20year%3A"+str(year)+")&fl=bibcode&rows=200&sort=date%20desc%2C%20bibcode%20desc"
  else: # use extra filter
    #print("Using standard query with extra filter.")
    extra_filter[0] = extra_filter[0].replace(":", "%3A")
    extra_filter[0] = extra_filter[0].replace("\"", "%22")
    url = "https://api.adsabs.harvard.edu/v1/search/query?q=(%3Dauthor%3A%22"+author+"%22%20AND%20year%3A"+str(year)+"%20AND%20"+extra_filter[0]+")&fl=bibcode&rows=200&sort=date%20desc%2C%20bibcode%20desc"
  #query is https://api.adsabs.harvard.edu/v1/search/query?q=((=author:"Lee, H.M." or =author:"Lee, Hyung Mok") and year:2022)&fl=bibcode&rows=200&sort=date+desc,bibcode+desc

  # the query parameters can be included as part of the URL
  r = requests.get(url, headers={'Authorization': 'Bearer ' + token})
  #print(r.json())
  response = r.json()['response']
  docs = response['docs']
  numbers = response['numFound']
  bibcodes = []
  for idx in range(len(docs)):
    bibcodes.append(docs[idx]['bibcode'])
  return bibcodes

def get_authors(file_name):
  with open(file_name, "r") as author_file:
    lines = author_file.read()
    authors = lines.split('\n')
  authors0 = [author for author in authors if len(author)>0]
  return authors0

def count_authors(author):
  authors = author.split('and')
  count = len(authors)
  return count

def mk_short_list(author):
  authors = author.split('and')
  short_list = ""
  for idx in range(4):
    short_list += authors[idx] + " and "
  short_list += "et al."
  return short_list

def is_full_author(bibitem):
  is_full = False
  author = get_author(bibitem)
  if author is None:
    author = "No Author"
    count = 0
  else:
    #print("bibitem = {0}, author = {1}".format(bibitem, author))
    count = count_authors(author)
  if 'et al.' in author or count > MIN_AUTHORS_COLL:
    is_full = True
  #print("Author = {0}, Full_author = {1}, Count = {2}".format(author, is_full, count))
  return is_full

def get_full_short_authors(bibitems, bibcodes):
  bibitem_short = []
  bibitem_full = []
  bibcodes_short = []
  bibcodes_full = []
  if len(bibitems) != len(bibcodes) :
    print("ERROR: len(bibitems) = {0} is not equal to len(bibcodes) = {1} in get_full_short_authors().".format(len(bibitems), len(bibcodesa)))
    return bibitem_full, bibcodes_full, bibitem_short, bibcodes_short
    
  for idx in range(len(bibitems)):
    if is_full_author(bibitems[idx]):
      bibitem_full.append(bibitems[idx])
      bibcodes_full.append(bibcodes[idx])
    else:
      bibitem_short.append(bibitems[idx])
      bibcodes_short.append(bibcodes[idx])
  return bibitem_full, bibcodes_full, bibitem_short, bibcodes_short

def mk_link_string(bibitem, add_title):
  link_string = ""
  author = get_author(bibitem)
  if author is None:
    author = "No Author"
    count = 0
  else:
    #print("bibitem = {0}, author = {1}".format(bibitem, author))
    count = count_authors(author)
  if count > MIN_AUTHORS_COLL:
    author = mk_short_list(author)
  journal = get_journal(bibitem)
  volume = get_volume(bibitem)
  pages = get_pages(bibitem)
  year = get_year(bibitem)
  link_string = author
  if len(journal) > 0:
    link_string += ", <span style=\"color: green;\">"+journal
  else:
    link_string += ", <span style=\"color: green;\">"
  if len(volume) > 0:
    link_string += " "+volume
  if len(pages) > 0:
    link_string += ", "+pages
  if len(year) > 0:
    link_string += "("+year+")"
  link_string += "</span>"
  if add_title:
    title = get_title(bibitem)
    if len(title) > 0:
      link_string += ", <span style=\"color: black;\">\""+title+"\"</span>"
  return link_string

def exclude_journals(bibitems, bibcodes, journals):
  bibitems_new = []
  bibcodes_new = []
  for idx in range(len(bibitems)):
    journal = get_journal(bibitems[idx]).upper()
    exclude = False
    for idx1 in range(len(journals)):
      journal1 = journals[idx1].upper()
      #print("journal = {0}, journal1 = {1}".format(journal, journal1))
      if journal1 in journal:
        exclude = True
        break
    #print("journal = {0}, Exclude = {1}".format(journal, exclude))
    if not exclude:
      bibitems_new.append(bibitems[idx])
      bibcodes_new.append(bibcodes[idx])
  return bibitems_new, bibcodes_new

def exclude_title_words(bibitems, bibcodes, journals):
  bibitems_new = []
  bibcodes_new = []
  for idx in range(len(bibitems)):
    journal = get_title(bibitems[idx]).upper()
    exclude = False
    for idx1 in range(len(journals)):
      journal1 = journals[idx1].upper()
      #print("journal = {0}, journal1 = {1}".format(journal, journal1))
      if journal1 in journal:
        exclude = True
        break
    #print("journal = {0}, Exclude = {1}".format(journal, exclude))
    if not exclude:
      bibitems_new.append(bibitems[idx])
      bibcodes_new.append(bibcodes[idx])
  return bibitems_new, bibcodes_new

def exclude_bibcodes(bibitems, bibcodes, excludes):
  bibitems_new = []
  bibcodes_new = []
  for idx in range(len(bibitems)):
    bibcode = bibcodes[idx]
    exclude = False
    for idx1 in range(len(excludes)):
      if excludes[idx1] in bibcode:
        exclude = True
        break
    if not exclude:
      bibitems_new.append(bibitems[idx])
      bibcodes_new.append(bibcodes[idx])
  return bibitems_new, bibcodes_new

def get_bibitems_year(file_name, year):
  #url = "https://api.adsabs.harvard.edu/v1/search/query?q=((%3Dauthor%3A%22Lee,H.M.%22%20or%20%3Dauthor%3A%22Lee,Hyung%20Mok%22)%20AND%20year%3A"+str(year)+")&fl=bibcode&rows=200&sort=date%20desc%2C%20bibcode%20desc"
  #query is https://api.adsabs.harvard.edu/v1/search/query?q=((=author:"Lee, H.M." or =author:"Lee, Hyung Mok") and year:2022)&fl=bibcode&rows=200&sort=date+desc,bibcode+desc
  bibtex_url = "https://api.adsabs.harvard.edu/v1/export/bibtex"

  # the query parameters can be included as part of the URL
  #r = requests.get(url, headers={'Authorization': 'Bearer ' + token})
  #response = r.json()['response']
  #docs = response['docs']
  #numbers = response['numFound']
  #bibcodes = []
  #for idx in range(len(docs)):
  #  bibcodes.append(docs[idx]['bibcode'])
  authors = get_authors(file_name)
  print("authors = {0}".format(authors))
  bibcodes = []
  for idx in range(len(authors)):
    bibcodes0 = get_bibcodes(authors[idx], year)
    bibcodes = list(set(bibcodes) | set(bibcodes0)) #exclude the same bibcode

  excl_journals = get_exclude_journals(exclude_file_name)
  if len(excl_journals) > 0:
    print("Following jounrals will be excluded from the list : {0}".format(excl_journals))

  excl_bibcodes = get_exclude_bibcodes(exclude_bibcode_file_name)
  if len(excl_bibcodes) > 0:
    print("Following bibcodes will be excluded from the list : {0}".format(excl_bibcodes))

  excl_title_words = get_exclude_title_words(exclude_title_word_file_name)
  if len(excl_title_words) > 0:
    print("Papers with the following wrods included in title will be excluded from the list : {0}".format(excl_title_words))

  if len(bibcodes) > 0:
    exports = {'bibcode':bibcodes , 'sort':'no sort', 'maxauthor':3}
    bibtex = requests.post(bibtex_url,  headers={'Authorization': 'Bearer ' + token, 'Content-Type':'application/json'}, json=exports)
    print(bibtex.json())
    total_papers = len(bibcodes)
    bibitems = bibtex.json()['export']
    #bibitems1 = bibitems.split('@')
    bibitems1 = get_bibitem_list(bibitems)
    bibitems2 = [bibitem for bibitem in bibitems1 if len(bibitem) > 0]
    print("len(bibitems) = {0}, len(bibitems) = {1}, len(bibitems2) = {2}, len(bibcodes) = {3}".format(len(bibitems), len(bibitems1), len(bibitems2), len(bibcodes)))
    bibitems2, bibcodes = exclude_journals(bibitems2, bibcodes, excl_journals)
    bibitems2, bibcodes = exclude_bibcodes(bibitems2, bibcodes, excl_bibcodes)
    bibitems2, bibcodes = exclude_title_words(bibitems2, bibcodes, excl_title_words)
    print("len(bibitems2) = {0}, len(bibcodes) = {1} after some journals excluded.".format(len(bibitems2), len(bibcodes)))
    bibitem_full, bibcodes_full, bibitem_short, bibcodes_short = get_full_short_authors(bibitems2, bibcodes)
    print("len(bibitem_full) = {0}, len(bibcodes_full) = {1}, len(bibitem_short) = {2}, len(bibcodes_short) = {3}".format(len(bibitem_full), len(bibcodes_full), len(bibitem_short), len(bibcodes_short)))
    print("=====================================================================================================")
    print("     Total {0} bibitems for year {1}, excluded {2} papers".format(len(bibcodes), year, (total_papers - len(bibcodes))))
    print("=====================================================================================================")
    #print("==== Bibitems ==========\n")
    #for idx in range(len(bibitems2)):
    #  print("bibitems2[{0}] :{1}\n".format(idx, bibitems2[idx]))
    #print("==== Bibcodes ==========\n")
    #for idx in range(len(bibcodes)):
    #  print("bibcodes[{0}] :{1}\n".format(idx, bibcodes[idx]))
    file_name = "kgwg_publications_"+str(year)+"_"+current_month_text+".bib"
    with open(file_name, "w") as text_file:
      text_file.write("{0}".format(bibitems))
    #generate_html(year, bibitems2, bibcodes)
    generate_html(year, bibitem_full, bibcodes_full, bibitem_short, bibcodes_short)
  else: # no data found
    generate_html(year, [], [], [], [])

for year in range(current_year - 2, current_year+1):
  get_bibitems_year(author_file_name, year)


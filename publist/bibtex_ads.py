#!/usr/env python3

print(__import__('sys').version)

import shlex, subprocess
import urllib, re

#url = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST&db_key=PHY&qform=AST&sim_query=YES&ned_query=YES&adsobj_query=YES&aut_req=YES&aut_logic=AND&obj_logic=OR&author=Weinstein%2C+A.%0D%0AOh%2C+J.%0D%0AOh%2C+S.%0D%0ALee%2C+H.%0D%0AKang%2C+G.&object=&start_mon=&start_year=2010&end_mon=&end_year=&ttl_logic=OR&title=&txt_req=YES&txt_logic=BOOL&text=Gravitational+%28Wave+or+Radiation%29&nr_to_return=200&start_nr=1&jou_pick=ALL&ref_stems=&data_and=ALL&group_and=ALL&start_entry_day=&start_entry_mon=&start_entry_year=&end_entry_day=&end_entry_mon=&end_entry_year=&min_score=&sort=SCORE&data_type=BIBTEX&aut_syn=YES&ttl_syn=YES&txt_syn=YES&aut_wt=1.0&obj_wt=1.0&ttl_wt=0.3&txt_wt=3.0&aut_wgt=YES&obj_wgt=YES&ttl_wgt=YES&txt_wgt=YES&ttl_sco=YES&txt_sco=YES&version=1"
url = "https://ui.adsabs.harvard.edu/search/p_=0&q=%20author%3A%22H.M.%20Lee%22&sort=date%20desc%2C%20bibcode%20desc"

response = urllib.request.urlopen(url)
source = response.read()
print(source)
source1 = source.decode('utf-8')
print(source1)


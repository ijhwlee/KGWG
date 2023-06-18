#!/bin/bash

#cd /home/hwlee/projects/publist/html
cd /usr/share/nginx/kgwg.org/publications/

python3 /home/hwlee/projects/publist/bibtex_hwlee.py 0 kgwg_authors.dat > /dev/null
#python3 /home/hwlee/projects/publist/bibtex_hwlee.py 0 kgwg_authors.dat > mk_pub_list.log



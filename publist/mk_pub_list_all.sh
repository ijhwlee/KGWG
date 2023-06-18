#!/bin/bash

c_year=`date +'%Y'`

#cd /home/hwlee/projects/publist/html
cd /usr/share/nginx/kgwg.org/publications/

#python3 /home/hwlee/projects/publist/bibtex_hwlee.py 0 kgwg_authors.dat > /dev/null
echo "=======================================================================" > mk_pub_list_all.log
echo "Making publication list for $c_year" >> mk_pub_list_all.log
date >> mk_pub_list_all.log
echo "=======================================================================" >> mk_pub_list_all.log
for year in $(eval echo "{2012..$c_year..3}")
do
  #echo "Year is $year"
  python3 /home/hwlee/projects/publist/bibtex_hwlee.py $year kgwg_authors.dat >> mk_pub_list_all.log
done
python3 /home/hwlee/projects/publist/bibtex_hwlee.py 0 kgwg_authors.dat >> mk_pub_list_all.log

#python3 /home/hwlee/projects/publist/bibtex_hwlee.py 2023 kgwg_authors.dat > mk_pub_list_all.log
#python3 /home/hwlee/projects/publist/bibtex_hwlee.py 2020 kgwg_authors.dat >> mk_pub_list_all.log
#python3 /home/hwlee/projects/publist/bibtex_hwlee.py 2017 kgwg_authors.dat >> mk_pub_list_all.log
#python3 /home/hwlee/projects/publist/bibtex_hwlee.py 2014 kgwg_authors.dat >> mk_pub_list_all.log
#python3 /home/hwlee/projects/publist/bibtex_hwlee.py 2012 kgwg_authors.dat >> mk_pub_list_all.log



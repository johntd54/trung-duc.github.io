#! /usr/local/bin/python

import datetime
import subprocess
import sys

current_time = datetime.datetime.now()

if (sys.version_info > (3, 0)):
    r_title = input("Title: ")
    categories = input("Categories (separated by ', '): ")
else:
    r_title = raw_input("Title: ")
    categories = raw_input("Categories (separated by ', '): ")


title = "{} - {}".format(current_time.strftime("%y%m%d"), r_title)
filename = "{}-{}.markdown".format(current_time.strftime("%Y-%m-%d"),
    r_title.replace(' ', '-').lower())

with open(filename, 'w') as f:
    f.write('---\n')
    f.write('layout: post\n')
    f.write('title: "{}"\n'.format(title))
    f.write('date: {}\n'.format(current_time.strftime("%Y-%m-%d %H:%M:%S")))
    f.write('categories: {}\n'.format(categories))
    f.write('---\n')

subprocess.call(["sublime", filename])
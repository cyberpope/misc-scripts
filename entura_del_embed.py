#!/bin/python
import pyperclip
import re

# Regex
embed_regex = re.compile(r'(https:/|http:/)(/.*?/)(embed/)?(.*)')
embed_check_regex = re.compile(r'(https:/|http:/)(/.*?/)(embed/)(.*)')
uploadedTo_ref_regex = re.compile(r'(https://|http://)([^?^\n]*)')
uploadedTo_ref_check_regex = re.compile(r'(https:/|http:/)(/.*?)(\?ref=\d*)')
site_name_regex = re.compile(r'(https://|http://)(www.)?(.*?)/')

# Clipbord matches check + link clearing
text = str(pyperclip.paste())

matches = []

site_name = site_name_regex.search(text).group(3)
# site_name = site_name_regex.findall(text)
# for groups in site_name_regex.findall(text):
#     site_name = ''.join([groups[1]])
#     print(site_name)

if embed_check_regex.findall(text):
    for groups in embed_regex.findall(text):
        clear_link = ''.join([groups[0], groups[1], groups[3]])
        matches.append(clear_link)
    if len(matches) > 0:
        pyperclip.copy('\n'.join(matches))
        print('Done, embed links found for %s, total count: %s ' % (site_name, len(matches)))
elif uploadedTo_ref_check_regex.findall(text):
    for groups in uploadedTo_ref_regex.findall(text):
        print(groups)
        clear_link = ''.join([groups[0], groups[1]])
        print(clear_link)
        matches.append(clear_link)
    if len(matches) > 0:
        pyperclip.copy('\n'.join(matches))
        print('Done, uploadedTo ref links found for %s, total count: %s ' % (site_name, len(matches)))
else:
    print('No convertable links found for %s' % site_name)


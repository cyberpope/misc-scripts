#!/bin/python
import pyperclip
import re

# Regex
links_regex = re.compile(r'(https:/|http:/)(/.*?/)(embed/)?(.*)')
embed_regex = re.compile(r'(https:/|http:/)(/.*?/)(embed/)(.*)')

# Clipbord matches check + link clearing
text = str(pyperclip.paste())

matches = []
for groups in links_regex.findall(text):
#    print(groups)
    clear_link = ''.join([groups[0], groups[1], groups[3]])
#    print(clear_link)
    matches.append(clear_link)
if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Done master, total links count: %s ' % len(matches))
#   print('\n'.join(matches))
else:
    print('No links found')


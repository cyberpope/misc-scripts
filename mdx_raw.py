import re
import lxml
import mechanicalsoup
import os

# Make use of functions - ?? - Read some tutorials for clarification

# Soup config
url = 'https://myunihub-1.mdx.ac.uk/cas-web/login?service=https%3A%2F%2Fmyunihub.mdx.ac.uk%2Fc%2Fportal%2Flogin'
browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
)
print(' \n Please provide your username')
username = input()
print(' \n Thank you, password now')
password = input()
# Open webiste + login
print('Loginning in')
browser.open(url)
browser.select_form()
browser['username'] = username
browser['password'] = password
browser.submit_selected(btnName='submit_form')

print('Opening resources website mdx.mrooms.net')
# Open moodle
browser.follow_link(link='mdx.mrooms.net')
# Download page as bs4 element
page = browser.get_current_page()
# Links to subject page
print('Finding subject links and titles')
sub_links = page.find_all('li', {'class': ['r1', 'r0']})
a = 0
# List containing links and subject names
results = []
for i in sub_links:
    matches = sub_links[a].find('a')['href']
    results.append(matches)
    matches_1 = sub_links[a].find('a')['title']
    results.append(matches_1)
    a = a + 1

# Two new list for links and titles
clear_sub_links = []
clear_sub_names = []
for i in results[::2]:
    clear_sub_links.append(i)
    a = a + 1
a = 0
for i in results[1::2]:
    clear_sub_names.append(i)
    a = a + 1

# Regex for subject name - each start with year date e.g. 2017-2018
results_reg = re.compile(r'\d\d\d\d-\d\d')
a = 0
sub_names = []
sub_links = []
# Loop through list and create new to avoid problems during del
for i in clear_sub_names:
    if results_reg.search(clear_sub_names[a]):
        sub_names.append(clear_sub_names[a])
        sub_links.append(clear_sub_links[a])
        a = a + 1
    else:
        a = a + 1

print(sub_names)
# Regular expression to scrape subject IDs
sub_id_reg = re.compile(r'(.*)(\d\d\d\d\d)')
# Extract subject ID from href link to follow links through ID, whole links doesnt work
a = 0
short_results = []
for i in sub_links:
    sub_id = sub_id_reg.search(sub_links[a])
    if a == len(results):
        break
# WIERD ^^
    sub_id = sub_id.group(2)
    short_results.append(sub_id)
    a = a + 1

a = 0
for i in sub_names:
    print('%s' % sub_names[a])
    a = a + 1

# Regex for files
res_link_reg = re.compile(r'https://mdx.mrooms.net/mod/resource/view.php\?id=(.*)')
folder_link_reg = re.compile(r'https://mdx.mrooms.net/mod/folder/view.php\?id=(.*)')
i_folder_link_reg = re.compile(r'https://mdx.mrooms.net/pluginfile.php/(.*?)/')
excel_reg = re.compile(r'Excel')
word_reg = re.compile(r'Word')
pdf_reg = re.compile(r'PDF')
powerpoint_reg = re.compile(r'Powerpoint')
zip_reg = re.compile(r'ZIP')
escape_char_reg = re.compile(r'(.*)(/)+(.*)')
File_reg = re.compile(r'(.*?)(File)')
video_reg = re.compile(r'Video')

ext_in_file = re.compile(r'(.*).(/d/d/d(/d)*)')

# LOOP
# Through all links to download all resources
# Directories for each subject needs to be created manually according to sub_names list
print('Scraping folders and resources')

a = 0
for i in short_results:
    c = 0
    print(short_results[a])
    browser.follow_link(link='mdx.mrooms.net')
    browser.follow_link(link='%s' % short_results[a])
    print(sub_names[a])
    # Create subject folder
    if not os.path.exists(sub_names[a]):
        os.mkdir(sub_names[a], exist_ok=True)
    # Get current page
    page = browser.get_current_page()
    print(browser.get_url())
    # Find resources on a subject main page
    res_links = page.find_all('li', class_='activity resource modtype_resource')
    # Find directory links on a subject main page
    folder_links = page.find_all('li', class_='activity folder modtype_folder')
    if page.find_all('li', class_='activity folder modtype_folder'):
        print('Scraping from sub folders')
        for j in folder_links:
            if folder_links[c].find('a', attrs={'href': re.compile('https://')}):
                folder = folder_links[c].find('a', attrs={'href': re.compile('https://')})
                folder = folder_link_reg.search(folder.get('href'))
                folder_id = folder.group(1)
                browser.follow_link(link='%s' % folder_id)
                # Prints directory number derivered from link
                print('Folder %s' % (folder_id))
                page = browser.get_current_page()
                if page.find('div', class_='box generalbox foldertree py-3'):
                    folder_tree = page.find('div', class_='box generalbox foldertree py-3')
                    i_folder_res = folder_tree.find_all('a', attrs={'href': re.compile('https://')})
                    print('Files in folder: %s' % len(i_folder_res))
                    if len(i_folder_res) == 1:
                        name = i_folder_res[0].find('span', class_='fp-filename').get_text()
                        i_res_link = i_folder_res[0].get('href')
                        i_res_link = i_folder_link_reg.search(i_res_link)
                        i_res_id = i_res_link.group(1)
                        browser.download_link(link='%s' % i_res_id, file='%s/%s' % (sub_names[a], name))
                    else:
                        d = 0
                        for k in i_folder_res:
                            name = i_folder_res[d].find('span', class_='fp-filename').get_text()
                            i_res_link = i_folder_res[d].get('href')
                            i_res_link = i_folder_link_reg.search(i_res_link)
                            i_res_id = i_res_link.group(1)
                            browser.download_link(link='%s' % i_res_id, file='%s/%s' % (sub_names[a], name))
                    browser.follow_link(link='%s' % short_results[a])
            c = c + 1
    else:
        print('No sub folders found')
    print(browser.get_url())
    page = browser.get_current_page()
    # Loop through tags to extract filename and format and link
    if page.find_all('li', class_='activity resource modtype_resource'):
        print('Scraping main folder')
        b = 0
        for j in res_links:
            if res_links[b].find('a', attrs={'href': re.compile('^https://')}):
                name = res_links[b].find('span', class_='instancename').get_text()
                if res_links[b].find('span', class_='resourcelinkdetails'):
                    ext = res_links[b].find('span', class_='resourcelinkdetails').get_text()
                    link = res_links[b].find('a', attrs={'href': re.compile('^https://')})
                    link = link.get('href')
                    link = res_link_reg.search(link)
                    link = link.group(1)
                    if File_reg.search(name):
                        name = File_reg.search(name)
                        name = name.group(1)
                    if escape_char_reg.search(name):
                        for groups in escape_char_reg.findall(name):
                            name = ''.join([groups[0], groups[2]])
                    if word_reg.search(ext):
                        print(link)
                        browser.download_link(link='%s' % link, file='%s/%s.doc' % (sub_names[a], name))
                    elif pdf_reg.search(ext):
                        print(link)
                        browser.download_link(link='%s' % link, file='%s/%s.pdf' % (sub_names[a], name))
                    elif powerpoint_reg.search(ext):
                        print(link)
                        browser.download_link(link='%s' % link, file='%s/%s.pptx' % (sub_names[a], name))
                    elif zip_reg.search(ext):
                        print(link)
                        browser.download_link(link='%s' % link, file='%s/%s.zip' % (sub_names[a], name))
                    elif video_reg.search(ext):
                        print(link)
                        browser.download_link(link='%s' % link, file='%s/%s.avi' % (sub_names[a], name))
                else:
                    link = res_links[b].find('a', attrs={'href': re.compile('^https://')})
                    link = link.get('href')
                    link = res_link_reg.search(link)
                    link = link.group(1)
                    if File_reg.search(name):
                        name = File_reg.search(name)
                        name = name.group(1)
                    if escape_char_reg.search(name):
                        for groups in escape_char_reg.findall(name):
                            name = ''.join([groups[0], groups[2]])
                    print(link)
                    browser.download_link(link='%s' % link, file='%s/%s' % (sub_names[a], name))

            b = b + 1
    else:
        print('Main folder empty')
    # End of a loop redirection to main page
    browser.follow_link(link='mdx.mrooms.net')
    # Url check just for safety
    print(browser.get_url())
    a = a + 1

print('Done')

import os
import re

def run():
    #delete gems.js and gems.css if exists
    if os.path.exists('gems.js'):
        os.remove('gems.js')
        
    if os.path.exists('gems.css'):
        os.remove('gems.css')
    if os.path.exists('gems.min.css'):
        os.remove('gems.min.css')

    css_files = os.listdir('modules/css')
    css_copiled = ''

    css_copiled += open('modules/css/root.css').read() #first root.css
    for css_file in css_files:
        if css_file != 'root.css' and css_file != 'rules.css':
            css_copiled += open('modules/css/' + css_file).read()
    css_copiled += open('modules/css/rules.css').read()

    #write gems.css
    open('gems.css', 'w').write(css_copiled)

    css_copiled = remove_comments(css_copiled)
    css_copiled = css_copiled.replace(' ', '')
    css_copiled = css_copiled.replace('\n', '')

    #write gems.min.css
    open('gems.min.css', 'w').write(css_copiled)

    js_files = os.listdir('modules/js')
    js_copiled = ''

    js_copiled += open('modules/js/root.js').read() #first root.js
    for js_file in js_files:
        if js_file != 'root.js':
            js_copiled += open('modules/js/' + js_file).read()
    
    #write gems.js
    open('gems.js', 'w').write(js_copiled)

    js_copiled = remove_comments(js_copiled)
    js_copiled = js_copiled.replace('\n', ';')
    #remove if more caracteres ; if more than 1
    js_copiled = re.sub(r';+', ';', js_copiled)

    #write gems.min.js
    open('gems.min.js', 'w').write(js_copiled)


def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

if __name__ == '__main__':
    run()
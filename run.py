import os
import re
import jsmin
from csscompressor import compress
import argparse

__version__ = '0.0.1'
version_gems = ''

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
    css_copiled = compress(css_copiled)

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

    js_copiled = jsmin.jsmin(js_copiled)
    js_copiled = js_copiled.replace('\n', ';')

    #write gems.min.js
    open('gems.min.js', 'w').write(js_copiled)

def new_version():
    #get version/version.txt
    version = open('version/version.txt').read()
    #split version
    version = version.split('.')
    #increment version
    version[3] = str(int(version[3]) + 1)
    #join version
    version = '.'.join(version)
    #write version
    open('version/version.txt', 'w').write(version)
    print('New version: ' + version)
    
    base_dir = "version"
    version_dir = os.path.join(base_dir, version)

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    if not os.path.exists(version_dir):
        os.makedirs(version_dir)
        print(f"Criada a pasta da versão {version}.")
    else:
        print(f"A pasta da versão {version} já existe.")
    version_gems = version
    
def gerateNewVersion():
    #get version/version.txt
    version = open('version/version.txt').read()
    #get files to version paste
    if os.name == 'posix':
        files = os.listdir('version/' + version_gems)
    elif os.name == 'nt':
        files = os.listdir('version/' + version_gems)
    #paste files to version folder
    for file in files:
        if os.name == 'posix':
            os.rename('version/' + version_gems + '/' + file, 'version/' + version + '/' + file)
        elif os.name == 'nt':
            os.rename('version\\' + version_gems + '\\' + file, 'version\\' + version + '\\' + file)
    

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
    version_enable = False
    print('')
    #get if argparse '-n' or '--new-version' is set if not set run()
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new-version', action='store_true')
    #get if argparse '-v' or '--version' is set if set print version
    parser.add_argument('-v', '--version', action='store_true')
    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit()
    if args.new_version:
        print('GENERATING NEW VERSION')
        new_version()
        version_enable = True
    print('\nCOPILE - START')
    run()
    print('COPILE - DONE')
    if version_enable:
        print('\nSAVE VERSION - START')
        #gerateNewVersion()
        #NO USE gerateNewVersion() - USE MANUALLY
        print('SAVE VERSION - DONE')

    print('\nRUN.PY - END - THANKS FOR USE GEMS')
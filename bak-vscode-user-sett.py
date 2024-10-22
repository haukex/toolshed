#!/usr/bin/env python
from pathlib import Path
import subprocess
import sys
import re

if sys.platform.startswith('win32'):
    sett_json = Path.home()/'AppData'/'Roaming'/'Code'/'User'/'settings.json'
elif sys.platform.startswith('linux'):
    sett_json = Path.home()/'.config'/'Code'/'User'/'settings.json'
else:
    raise NotImplementedError()
bak_file = Path(__file__).parent/'notes'/'vscode-user-settings.bak.jsonc'

with sett_json.open(encoding='UTF-8') as fh:
    json = fh.read()

# replacements are kind of ugly, but I haven't yet found a well-supported JSON5/JSONC module that preserves comments
json = re.sub(r'(^\s*"remote.SSH.remotePlatform":\s+\{)[^}]+(\},\n)',
              lambda m: m.group(1)+' /* (content removed in backup) */ '+m.group(2), json, flags=re.S|re.M) \

with bak_file.open('w', encoding='UTF-8', newline='\n') as fh:
    fh.write(f"// This is a backup of my VSCode user settings.json\n")
    fh.write(json)

subprocess.run(['git','diff','--color-words','--ignore-all-space',sett_json,bak_file], check=False)

#!/usr/bin/env python3
from pathlib import Path
import subprocess
import re

sett_json = Path.home()/'AppData'/'Roaming'/'Code'/'User'/'settings.json'
bak_file = Path(__file__).parent/'notes'/'vscode-user-settings-win.bak.jsonc'

with sett_json.open(encoding='UTF-8') as fh:
    json = fh.read()

# replacements are kind of ugly, but I haven't yet found a well-supported
# JSON5/JSONC module that preserves comments
json = re.sub(r'(^\s*"remote.SSH.remotePlatform":\s+\{)[^}]+(\},\n)',
              lambda m: m.group(1)+' /* (content removed in backup) */ '+m.group(2), json, flags=re.S|re.M) \
    .replace(Path.home().as_posix(), "~").replace(str(Path.home()), "~")

with bak_file.open('w', encoding='UTF-8', newline='\n') as fh:
    fh.write(f"// This is a backup of my ~/{sett_json.relative_to(Path.home()).as_posix()}\n")
    fh.write('// NOTE that the user home directory was replaced with "~", but this must be an absolute path in the actual config!\n')
    fh.write(json)

subprocess.run(['git','diff','--color-words','--ignore-all-space',sett_json,bak_file], check=False)

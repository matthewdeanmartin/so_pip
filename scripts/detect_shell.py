from typing import Tuple, List

import os

import psutil

SHELL_NAMES = {
    'sh', 'bash', 'dash', 'ash',    # Bourne.
    'csh', 'tcsh',                  # C.
    'ksh', 'zsh', 'fish',           # Common alternatives.
    'cmd', 'powershell', 'pwsh',    # Microsoft.
    'elvish', 'xonsh',              # More exotic.
}

def find_shell_for_windows() -> Tuple[str,str]:
    names_paths:List[Tuple[str,str]]=[]
    current_process = psutil.Process(os.getppid())
    process_name, process_path = current_process.name(), current_process.exe()
    names_paths.append((process_name, process_path))
    for parent in current_process.parents():
        names_paths.append((parent.name(), parent.exe()))
    for n,p in names_paths:
        if n.lower() in SHELL_NAMES or n.lower().replace(".exe","") in SHELL_NAMES:
            return n,p
    return ["",""]

if __name__ == '__main__':
    print(find_shell_for_windows())

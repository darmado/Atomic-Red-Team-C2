from blackbot.core.utils import get_path_in_package
import subprocess
import os

class ARTIC2Wrapper:
    def __init__(self):
        self.name = 'ps1'
        self.tool = 'powershell.sh'
        self.target_directory = '/var/www/html/'
        self.tools_path = get_path_in_package('core/obfuscate/src/powershell/')

    def obfuscate(self, filename):
        selected_tool = '{}/{}'.format(self.tools_path, self.tool)
        selected_stager = '{}/{}'.format(self.target_directory, filename)

        subprocess.run([f'{selected_tool} -f {selected_stager} -l 2 -v -c -t -o /var/www/html/{filename.split(".")[0]}_obfuscated.ps1'], shell=True, stdout=None, stderr=None,)






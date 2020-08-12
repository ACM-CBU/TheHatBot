import os
from pathlib import Path
import pip


class MaintenanceHelper:

    @staticmethod
    def install(package):
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            pip._internal.main(['install', package])

    @staticmethod
    def install_requirements():
        cwd = Path.home().joinpath('TheHatBot')
        os.chdir(cwd.absolute())
        if hasattr(pip, 'main'):
            pip.main(['install', '-r', 'requirements.txt'])
        else:
            pip._internal.main(['install', '-r', 'requirements.txt'])
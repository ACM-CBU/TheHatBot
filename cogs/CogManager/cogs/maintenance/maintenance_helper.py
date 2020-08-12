import os
from pathlib import Path
import pip


class MaintenanceHelper:
    PIP_FLAG_TO_REINSTALL = "--force-reinstall"
    PIP_FLAG_TO_UPGRADE = "--upgrade"

    @staticmethod
    def install_package(package):
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            pip._internal.main(['install', package])

    @classmethod
    def force_reinstall_package(cls, package):
        if hasattr(pip, 'main'):
            pip.main(['install', cls.PIP_FLAG_TO_REINSTALL, package])
        else:
            pip._internal.main(['install', package])

    @classmethod
    def upgrade_package(cls, package):
        if hasattr(pip, 'main'):
            pip.main(['install', cls.PIP_FLAG_TO_UPGRADE, package])
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
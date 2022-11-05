from jija.config.base import Base

from pathlib import Path as Path
import sys


class StructureConfig(Base):
    PROJECT_PATH = None
    CORE_PATH = None
    APPS_PATH = None
    PYTHON_PATH = None

    def __init__(self, *, project_path=None, core_dir='core', apps_dir='apps', python_path=None, **kwargs):
        StructureConfig.PROJECT_PATH = self.__get_project_path(project_path)
        StructureConfig.CORE_PATH = StructureConfig.PROJECT_PATH.joinpath(core_dir)
        StructureConfig.APPS_PATH = StructureConfig.PROJECT_PATH.joinpath(apps_dir)
        StructureConfig.PYTHON_PATH = python_path or sys.executable

        super().__init__(**kwargs)

    @staticmethod
    def __get_project_path(project_path):
        if isinstance(project_path, Path):
            if not project_path.is_absolute():
                return project_path.absolute()

            return project_path

        path = Path(project_path) if project_path else Path()
        return path.absolute()

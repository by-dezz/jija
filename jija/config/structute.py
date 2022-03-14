from jija.utils.path import Path


class StructureConfig:
    project_path = None
    core_path = 'core'
    apps_path = 'apps'

    def __init__(self, *, project_dir=None, core_dir='core', apps_dir='apps'):
        StructureConfig.project_path = self.__get_project_path(project_dir)
        StructureConfig.core_path = StructureConfig.project_path + core_dir
        StructureConfig.apps_path = StructureConfig.project_path + apps_dir

    @staticmethod
    def __get_project_path(project_dir):
        if isinstance(project_dir, Path):
            return project_dir

        return Path('' if project_dir is None else project_dir)

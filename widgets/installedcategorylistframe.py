from .categorylistframe import categorylistFrame
from appstore import Parser, Store_handler

class installedcategorylistFrame(categorylistFrame):
    def __init__(self,parent,controller,framework, packages):
        super().__init__(parent, controller, framework, packages)

    def get_current_packages(self):
        pkgs = self.appstore_handler.get_packages(silent = True)
        if pkgs:
            self.packages =  [Parser.get_package(pkg) for pkg in pkgs]

            packages = self.search_packages(self.current_search)
            if self.sort_type:
                packages = self.sort_packages(packages, self.sort_type)
            return packages
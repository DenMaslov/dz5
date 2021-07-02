import os
from concurrent.futures import ThreadPoolExecutor

from manager import FileManager


class Utility:


    def __init__(self, threads: int, src: str) -> None:
        self.file_manager = FileManager(self.parse_file_exten(src))
        self.executor = self._create_pool(threads)


    def do_operation(self, operation: str, src: str, to: str) -> None:
        if operation == 'move':
            self.file_manager.move(src, to, self.executor)
            while len([name for name in os.listdir(src)]): # remove empty dirs
                self.file_manager.remove_empty_dirs(src)
        elif operation == 'copy':
            self.file_manager.copy(src, to, self.executor)
            self.file_manager.remove_empty_dirs(to)


    def _create_pool(self, number_threads: int) -> ThreadPoolExecutor:
        if number_threads:
            return ThreadPoolExecutor(max_workers=number_threads)
        else:
            return ThreadPoolExecutor(max_workers=1)

    
    def parse_file_exten(self, src: str) -> str:
        """Returns file extensions"""
        start_at = src.find("*.")
        if start_at == -1:
            return ""
        start_at += 1
        return src[start_at : ]


    def pure_path(self, src: str) -> str:
        """Returns pure path without extensions"""
        start_at = src.find("*.")
        if start_at == -1:
            return src
        return src[ : start_at ]

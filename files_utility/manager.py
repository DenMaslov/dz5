import shutil, os
import stat
import logging as log
import threading


rootLog = log.getLogger()
rootLog.setLevel(log.INFO)
log.basicConfig(format='%(message)s',
                handlers=[log.StreamHandler()])


class FileManager:
    """Base functionality of copying/moving files"""


    def __init__(self, special_end = "") -> None:
        self.special_end = special_end


    def copy(self, source_dir: str, dst_dir: str, pool) -> None:
        self._remove_intersection(source_dir,dst_dir)
        for src_dir, dirs, files in os.walk(source_dir):
            res_dst_dir = src_dir.replace(source_dir, dst_dir, 1)
            if not os.path.exists(res_dst_dir):
                os.makedirs(res_dst_dir)
            for el in files:
                source_file = os.path.join(src_dir, el)
                try:
                    pool.submit(self.copy_files, source_file, res_dst_dir)
                except shutil.Error as err:
                    log.error(err.args[0])


    def move(self, source_dir: str, dst_dir: str, pool) -> None:
        self._remove_intersection(source_dir,dst_dir)
        for src_dir, dirs, files in os.walk(source_dir):
            res_dst_dir = src_dir.replace(source_dir, dst_dir, 1)
            if not os.path.exists(res_dst_dir):
                os.makedirs(res_dst_dir)
            for el in files:
                source_file = os.path.join(src_dir, el)
                try:
                    pool.submit(self.move_files, source_file, res_dst_dir)
                except shutil.Error as err:
                    log.error(err.args[0])
        self.remove_empty_dirs(source_dir)


    def _adjust_rights(self, dst: str) -> None:
        """Needs for getting read-only files"""
        for root, dirs, files in os.walk(dst):  
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)


    def _remove_intersection(self, src: str, dst: str) -> None:
        """Removes similar files, provides 'replace' mode """
        files_to_delete = self._get_intersection(src, dst)
        self._adjust_rights(dst)
        for el in files_to_delete:
            try:
                if os.path.isdir(dst + '/' + el):
                    log.info(f"Replacing old dir {dst + '/' + el} ")
                    shutil.rmtree(dst + '/' + el)
                else:
                    os.remove(dst + '/' + el)
            except shutil.Error as err:
                log.error(err.args[0])


    def copy_files(self, source_file: str, res_dst_dir: str):
        """Base copy func, runs in thread pool"""
        if source_file.endswith(self.special_end):
            log.info(f"Copying file {source_file} "
                    f" in thread {threading.get_ident()} ..."        
            )
            shutil.copy(source_file, res_dst_dir)


    def move_files(self, source_file: str, res_dst_dir: str):
        """Base move func, runs in thread pool"""
        if source_file.endswith(self.special_end):
            log.info(f"Moving files {source_file}"
                    f" in thread {threading.get_ident()} ..."        
            )
            shutil.move(source_file, res_dst_dir)


    def _get_intersection(self, src: str, dst: str) -> list:
        """Returns dirs and files with same name, for 'replace' mode """
        src_list = os.listdir(src)
        dst_list = os.listdir(dst)
        return list(set(src_list) & set(dst_list))


    def remove_empty_dirs(self, path) -> None:
        """Removes empty dirs"""
        for dir in os.listdir(path):
            el = os.path.join(path, dir)
            if os.path.isdir(el):
                self.remove_empty_dirs(el)
                if not os.listdir(el):
                    os.rmdir(el)

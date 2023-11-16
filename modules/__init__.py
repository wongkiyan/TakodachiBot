from os.path import dirname, basename, isfile, join
import glob

# 使用 glob 模組獲取在與此 __init__.py 檔案相同目錄中的所有 Python 檔案的清單
modules = glob.glob(join(dirname(__file__), "*.py"))

# 通過刪除目錄路徑和檔案擴展名，建立模組名稱的清單
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
            and not f.endswith('__init__.py')]
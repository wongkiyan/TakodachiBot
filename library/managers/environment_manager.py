from ctypes import windll

class EnvironmentManager():
    @classmethod
    def is_admin(self):
        try:
            return windll.shell32.IsUserAnAdmin()
        except:
            return False
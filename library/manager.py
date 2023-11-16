from ctypes import windll

class EnvironmentManager():
    def is_admin(self):
        try:
            return windll.shell32.IsUserAnAdmin()
        except:
            return False
        
environment_manager = EnvironmentManager()
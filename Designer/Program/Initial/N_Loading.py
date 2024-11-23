################################################################################################################################
#Loading
################################################################################################################################
import time
import _thread
import inspect

class Loading:
    def __init__(self, Global):
        try:
            self.Global = Global
            self.Enabled = False
            #Frame
            Fixture = self.Global['GUI'].Locate(25, 15, 73.5, 82.5)
            self.Frame = self.Global['Gluonix'].Frame(self.Global['GUI'])
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='white', Border_Size=1, Display=False)
            self.Frame.Create()
            self.Global['Widget'].append(self.Frame)
                #Image
            Fixture = self.Frame.Locate(20, 96, 7, 2)
            self.Image = self.Global['Gluonix'].Image(self.Frame)
            self.Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Image.Config(Path=self.Global['Image']('Loading'), Border_Size=0)
            self.Image.Create()
                #Label
            Fixture = self.Frame.Locate(67, 96, 31, 2)
            self.Label = self.Global['Gluonix'].Label(self.Frame)
            self.Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label.Config(Foreground='black', Value="Loading Please Wait...", Font_Size=10, Font_Weight='normal', Align='center', Border_Size=0)
            self.Label.Create()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))

    def Show(self):
        try:
            self.Enabled = True
            _thread.start_new_thread(self.Load, ())
            self.Frame.Show()
            self.Global['GUI'].Bind(Cursor_Loading=True)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Hide(self, Delay=False):
        try:
            if Delay:
                self.Global['GUI'].After(Delay*1000, lambda: self.Hide(Delay=False))
            else:
                self.Enabled = False
                self.Frame.Hide()
            self.Global['GUI'].Bind(Cursor_Arrow=True)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
                    
    def Load(self):
        while True:
            try:
                if self.Enabled:
                    try:
                        self.Image.Rotate(-5)
                        time.sleep(0.05)
                    except Exception as E:
                        time.sleep(1)
                        self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
                else:
                    break
            except Exception:
                break
                        
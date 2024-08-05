# -------------------------------------------------------------------------------------------------------------------------------
# Gluonix Runtime
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
from Nucleon.Runner import * ###!REQUIRED ------- Any Script Before This Won't Effect GUI Elements
#################################################################################################################################
#################################################################################################################################
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming Start
# -------------------------------------------------------------------------------------------------------------------------------

class Slider():

    def __init__(self, Bar, Frame, Callback=False):
        self._Bar = Bar
        self._Frame = Frame
        self._Callback = Callback
        self._Bar.Set(0)
        self._Frame.Bind(On_Click=lambda E: self.Progress_Start(E), On_Drag=lambda E: self.Progress(E), On_Release=lambda E: self.Callback())
        Bar_Data = self._Bar.Config_Get('Left', 'Width')
        Minimum = Bar_Data['Left']
        self._Frame.Config(Left=Minimum)
        self._Frame.Show()
        
    def Callback(self):
        self._Callback()
        
    def Get(self):
        return self._Bar.Get()
        
    def Set(self, Value):
        self._Bar.Set(Value)
        Bar_Data = self._Bar.Config_Get('Left', 'Width')
        Frame_Data = self._Frame.Config_Get('Left', 'Width')
        Minimum = Bar_Data['Left']
        Maximum = Bar_Data['Left']+Bar_Data['Width']-Frame_Data['Width']
        Frame_Left = Frame_Data['Left']+((Maximum-Minimum)*(Value/100))
        self._Frame.Config(Left=Frame_Left)

    def Progress_Start(self, E):
        self._Start = E.x

    def Progress(self, E):
        Frame_Data = self._Frame.Config_Get('Left', 'Width')
        Frame_Left = Frame_Data['Left'] + E.x - self._Start
        Bar_Data = self._Bar.Config_Get('Left', 'Width')
        Minimum = Bar_Data['Left']
        Maximum = Bar_Data['Left']+Bar_Data['Width']-Frame_Data['Width']
        Frame_Left = max(Minimum, min(Frame_Left, Maximum))
        Bar_Progress = (Frame_Left-Bar_Data['Left'])/(Maximum-Minimum)*100
        self._Bar.Set(Bar_Progress)
        self._Frame.Config(Left=Frame_Left)
        
def Output():
    print(Slider1.Get())
    
Slider1 = Slider(Root.Bar, Root.Frame, Output)
    
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################
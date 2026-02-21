# IMPORT LIBRARIES
from .N_GUI import GUI
from .N_Frame import Frame

class Line(Frame):

    def __init__(self, Main, *Args, **Kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Line"
            try:
                super().__init__(Main, *Args, **Kwargs)
                self._Type = "Line"
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Line[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Line[]"
                
    def Config(self, **Input):
        try:
            Run = False
            for Each in self._Config:
                if Each in Input:
                    if Each=='Border_Size':
                        setattr(self, "_"+Each, 0)
                    else:
                        Value = Input[Each]
                        setattr(self, "_"+Each, Value)
                    Run = True
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
                for Each in self._Widget:
                    try:
                        if Each._Background_Main:
                            Each.Config(Background=False)
                        if hasattr(Each, '_Radius'):
                            if Each._Radius>0:
                                Each.Config(Radius=Each._Radius)
                    except Exception:
                        self.Nothing = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
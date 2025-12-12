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
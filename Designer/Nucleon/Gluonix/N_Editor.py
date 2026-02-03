import math
import time
from .N_GUI import GUI

class Editor:

    def __init__(self, Canvas, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Editor"
            try:
                self._Canvas = Canvas
                self._Display = True
                self._Rectangles = {}
                self._Circles = {}
                self._Quadrilaterals = {}
                self._Lines = {}
                self._Polylines = {}
                self._Polygons = {}
                self._Rect_Transparent = {}
                self._Circle_Transparent = {}
                self._Quad_Transparent = {}
                self._Polygon_Transparent = {}
                self._Rect_ID_Next = 1
                self._Circle_ID_Next = 1
                self._Quad_ID_Next = 1
                self._Line_ID_Next = 1
                self._Polyline_ID_Next = 1
                self._Polygon_ID_Next = 1
                self._Selected_Rect_ID = None
                self._Selected_Circle_ID = None
                self._Selected_Quad_ID = None
                self._Selected_Line_ID = None
                self._Selected_Polyline_ID = None
                self._Selected_Polygon_ID = None
                self._Resize_Info = None
                self._Drag_Start_Pos = None
                self._Last_Click_Time = 0.0
                self._Last_Click_Pos = None
                self._Double_Click_Threshold = 0.35
                self._Rect_Handles = {}
                self._Quad_Handles = {}
                self._Circle_Handles = {}
                self._Rect_Disabled = {}
                self._Circle_Disabled = {}
                self._Quad_Disabled = {}
                self._Line_Disabled = {}
                self._Polyline_Disabled = {}
                self._Polygon_Disabled = {}
                self._Rect_Disable_Rotation = {}
                self._Drag_Last_X = 0
                self._Drag_Last_Y = 0
                self._Drag_Mode = "none"
                self._Click_Target = None
                self._Canvas._Item.append(self)
                self._Callback = None
                self._Callback_Mode = "Continuous"
                self.Bind()
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return f"Nucleon_Glunoix_Editor[]"

    def __repr__(self):
        return f"Nucleon_Glunoix_Editor[]"

    def __del__(self):
        try:
            self.Close()
        except:
            pass

    def Close(self):
        try:
            self.Clear()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Close -> {E}")

    def Delete(self):
        try:
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Bind(self):
        try:
            self._Canvas.Bind(On_Click=self.Drag_Start, On_Drag=self.Drag, On_Release=self.Release, On_Resize=self.Resize, On_Motion=self.Motion)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")

    def Canvas_Width(self):
        try:
            return self._Canvas._Frame.winfo_width()
        except:
            return 800

    def Canvas_Height(self):
        try:
            return self._Canvas._Frame.winfo_height()
        except:
            return 600

    def Edge_Tolerance(self):
        return 14.0

    def Normalize_Angle(self, A):
        try:
            return A % 360.0
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Normalize_Angle -> {E}")

    def Callback(self, Function, Mode="Continuous"):
        try:
            self._Callback = Function
            if Mode in ["Release", "Continuous"]:
                self._Callback_Mode = Mode
            else:
                self._Callback_Mode = "Continuous"
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Callback -> {E}")

    def Get_Current(self):
        try:
            if getattr(self, "_Selected_Rect_ID", None) is not None:
                ID = self._Selected_Rect_ID
                return {"Type": "Rectangle", "ID": ID, "Data": self.Get_Rectangle(ID=ID)}
            if getattr(self, "_Selected_Circle_ID", None) is not None:
                ID = self._Selected_Circle_ID
                return {"Type": "Circle", "ID": ID, "Data": self.Get_Circle(ID=ID)}
            if getattr(self, "_Selected_Quad_ID", None) is not None:
                ID = self._Selected_Quad_ID
                return {"Type": "Quadrilateral", "ID": ID, "Data": self.Get_Quadrilateral(ID=ID)}
            if getattr(self, "_Selected_Line_ID", None) is not None:
                ID = self._Selected_Line_ID
                return {"Type": "Line", "ID": ID, "Data": self.Get_Line(ID=ID)}
            if getattr(self, "_Selected_Polyline_ID", None) is not None:
                ID = self._Selected_Polyline_ID
                return {"Type": "Polyline", "ID": ID, "Data": self.Get_Polyline(ID=ID)}
            if getattr(self, "_Selected_Polygon_ID", None) is not None:
                ID = self._Selected_Polygon_ID
                return {"Type": "Polygon", "ID": ID, "Data": self.Get_Polygon(ID=ID)}
            return None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Current -> {E}")
            return None

    def Render(self):
        try:
            for ID in list(self._Rectangles.keys()):
                self.Rect_Draw(ID)
            for ID in list(self._Circles.keys()):
                self.Circle_Draw(ID)
            for ID in list(self._Quadrilaterals.keys()):
                self.Quad_Draw(ID)
            for ID in list(self._Lines.keys()):
                self.Line_Draw(ID)
            for ID in list(self._Polylines.keys()):
                self.Polyline_Draw(ID)
            for ID in list(self._Polygons.keys()):
                self.Polygon_Draw(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Render -> {E}")

    def Resize(self, Event):
        try:
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")

    def Clear(self):
        try:
            self.Remove_Rectangle(ID="all")
            self.Remove_Circle(ID="all")
            self.Remove_Quadrilateral(ID="all")
            self.Remove_Line(ID="all")
            self.Remove_Polyline(ID="all")
            self.Remove_Polygon(ID="all")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def _Callback_Invoke(self, Type, ID=None, Event="Update"):
        try:
            CB = getattr(self, "_Callback", None)
            if CB is None or not callable(CB):
                return
            Data = None
            if ID is not None:
                if Type == "Rectangle":
                    Data = self.Get_Rectangle(ID=ID)
                elif Type == "Circle":
                    Data = self.Get_Circle(ID=ID)
                elif Type == "Quadrilateral":
                    Data = self.Get_Quadrilateral(ID=ID)
                elif Type == "Line":
                    Data = self.Get_Line(ID=ID)
                elif Type == "Polyline":
                    Data = self.Get_Polyline(ID=ID)
                elif Type == "Polygon":
                    Data = self.Get_Polygon(ID=ID)
            Info = {"Type": str(Type), "Event": str(Event)}
            if ID is not None:
                Info["ID"] = ID
            if Data is not None:
                Info["Data"] = Data
            CB(Info)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Callback_Invoke -> {E}")

    def _Point_Handle_Radius(self):
        try:
            return 4.0
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Point_Handle_Radius -> {E}")
            return 4.0

    def _Clear_Handles(self, Handles):
        try:
            if Handles:
                for Item in list(Handles):
                    try:
                        self._Canvas.Delete_Item(Item)
                    except:
                        try:
                            self._Canvas._Frame.delete(Item)
                        except:
                            pass
            return []
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Clear_Handles -> {E}")
            return []

    def _Draw_Point_Handles(self, Points, Color, Existing_Handles=None):
        try:
            Handles = self._Clear_Handles(Existing_Handles)
            R = self._Point_Handle_Radius()
            for X, Y in Points:
                Item = self._Canvas._Frame.create_oval(X - R, Y - R, X + R, Y + R, outline=Color, fill=Color, width=1)
                self._Canvas._Frame.tag_raise(Item)
                Handles.append(Item)
            return Handles
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Draw_Point_Handles -> {E}")
            return Existing_Handles if Existing_Handles else []

    def _Distance_Point_To_Segment(self, X, Y, X1, Y1, X2, Y2):
        try:
            Dx = X2 - X1
            Dy = Y2 - Y1
            Den = Dx * Dx + Dy * Dy
            if Den <= 1e-12:
                return math.hypot(X - X1, Y - Y1), 0.0
            T = ((X - X1) * Dx + (Y - Y1) * Dy) / Den
            T = max(0.0, min(1.0, T))
            Px = X1 + T * Dx
            Py = Y1 + T * Dy
            return math.hypot(X - Px, Y - Py), T
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Distance_Point_To_Segment -> {E}")
            return 1e9, 0.0

    def _Closest_Segment_Index(self, Points, X, Y):
        try:
            if not Points or len(Points) < 2:
                return None, None, None
            Best_I = None
            Best_D = None
            Best_T = None
            for I in range(len(Points) - 1):
                X1, Y1 = Points[I]
                X2, Y2 = Points[I + 1]
                D, T = self._Distance_Point_To_Segment(X, Y, X1, Y1, X2, Y2)
                if Best_D is None or D < Best_D:
                    Best_D = D
                    Best_I = I
                    Best_T = T
            return Best_I, Best_D, Best_T
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Closest_Segment_Index -> {E}")
            return None, None, None

    def _Closest_Edge_Index(self, Points, X, Y):
        try:
            if not Points or len(Points) < 2:
                return None, None, None
            Best_I = None
            Best_D = None
            Best_T = None
            N = len(Points)
            for I in range(N):
                X1, Y1 = Points[I]
                X2, Y2 = Points[(I + 1) % N]
                D, T = self._Distance_Point_To_Segment(X, Y, X1, Y1, X2, Y2)
                if Best_D is None or D < Best_D:
                    Best_D = D
                    Best_I = I
                    Best_T = T
            return Best_I, Best_D, Best_T
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Closest_Edge_Index -> {E}")
            return None, None, None

    def _Rotate_Points(self, Points, Center, Delta_A_CW):
        try:
            Cx, Cy = Center
            Rad = -Delta_A_CW * math.pi / 180.0
            CosA = math.cos(Rad)
            SinA = math.sin(Rad)
            Out = []
            for X, Y in Points:
                Dx = X - Cx
                Dy = Y - Cy
                Rx = Dx * CosA - Dy * SinA
                Ry = Dx * SinA + Dy * CosA
                Out.append((Cx + Rx, Cy + Ry))
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Rotate_Points -> {E}")
            return Points

    def Rect_Corners(self, Rect):
        try:
            Cx, Cy, Width, Height, Angle, Thickness, Color, Fill, Item = Rect
            Rad = -Angle * math.pi / 180.0
            CosA = math.cos(Rad)
            SinA = math.sin(Rad)
            HW = Width / 2.0
            HH = Height / 2.0
            P = [(-HW, -HH), (HW, -HH), (HW, HH), (-HW, HH)]
            Out = []
            for Px, Py in P:
                X = Cx + Px * CosA - Py * SinA
                Y = Cy + Px * SinA + Py * CosA
                Out.append((X, Y))
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rect_Corners -> {E}")

    def Point_In_Rect(self, ID, X, Y):
        try:
            if ID not in self._Rectangles:
                return False
            Cx, Cy, Width, Height, Angle, Thickness, Color, Fill, Item = self._Rectangles[ID]
            Rad = -Angle * math.pi / 180.0
            CosA = math.cos(Rad)
            SinA = math.sin(Rad)
            Dx = X - Cx
            Dy = Y - Cy
            RX = Dx * CosA + Dy * SinA
            RY = -Dx * SinA + Dy * CosA
            return abs(RX) <= Width / 2.0 and abs(RY) <= Height / 2.0
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Point_In_Rect -> {E}")

    def Rect_Edge_Hit(self, ID, X, Y, Tol):
        try:
            Cx, Cy, Width, Height, Angle, Thickness, Color, Fill, Item = self._Rectangles[ID]
            Rad = -Angle * math.pi / 180.0
            CosA = math.cos(Rad)
            SinA = math.sin(Rad)
            Dx = X - Cx
            Dy = Y - Cy
            U = Dx * CosA + Dy * SinA
            V = -Dx * SinA + Dy * CosA
            HW = Width / 2.0
            HH = Height / 2.0
            dL = math.hypot(U + HW, max(0.0, abs(V) - HH))
            dR = math.hypot(U - HW, max(0.0, abs(V) - HH))
            dT = math.hypot(V + HH, max(0.0, abs(U) - HW))
            dB = math.hypot(V - HH, max(0.0, abs(U) - HW))
            m = min(dL, dR, dT, dB)
            if m > Tol * 1.5:
                return None, None, None
            if m == dL:
                return "left", (U + HW, V), m
            if m == dR:
                return "right", (U - HW, V), m
            if m == dT:
                return "top", (U, V + HH), m
            return "bottom", (U, V - HH), m
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rect_Edge_Hit -> {E}")

    def Rect_Grip_Hit(self, ID, X, Y, Tol):
        try:
            if ID not in self._Rectangles:
                return None, None, None
            Cx, Cy, Width, Height, Angle, Thickness, Color, Fill, Item = self._Rectangles[ID]
            Rad = -Angle * math.pi / 180.0
            CosA = math.cos(Rad)
            SinA = math.sin(Rad)
            Dx = X - Cx
            Dy = Y - Cy
            U = Dx * CosA + Dy * SinA
            V = -Dx * SinA + Dy * CosA
            HW = Width / 2.0
            HH = Height / 2.0
            Corners = [("top_left", -HW, -HH), ("top_right", HW, -HH), ("bottom_right", HW, HH), ("bottom_left", -HW, HH)]
            Best_Corner = None
            Best_Corner_D = None
            for Name, Cu, Cv in Corners:
                D = math.hypot(U - Cu, V - Cv)
                if Best_Corner_D is None or D < Best_Corner_D:
                    Best_Corner_D = D
                    Best_Corner = Name
            if Best_Corner_D is not None and Best_Corner_D <= Tol * 1.15:
                return Best_Corner, (U, V), Best_Corner_D
            Edge, Local, Dist = self.Rect_Edge_Hit(ID, X, Y, Tol)
            if Edge:
                return Edge, (U, V), Dist
            return None, (U, V), None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rect_Grip_Hit -> {E}")
            return None, None, None

    def Rect_Draw(self, ID):
        try:
            if ID not in self._Rectangles:
                return
            Rect = self._Rectangles[ID]
            Corners = self.Rect_Corners(Rect)
            Screen = []
            for X, Y in Corners:
                Screen.append(X)
                Screen.append(Y)
            Cx, Cy, Width, Height, Angle, Thickness, Color, Fill, Item = Rect
            Transparent = bool(self._Rect_Transparent.get(ID, False))
            Width_Draw = Thickness * (2 if self._Selected_Rect_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_polygon(*Screen, outline=Color, fill=Fill, width=Width_Draw)
                self._Rectangles[ID] = (Cx, Cy, Width, Height, Angle, Thickness, Color, Fill, Item)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(Item, outline=Color, fill=Fill, width=Width_Draw, state="normal")
            self._Canvas._Frame.itemconfigure(Item, stipple=("gray25" if Transparent else ""))
            self._Canvas._Frame.tag_raise(Item)
            if not hasattr(self, "_Rect_Handles"):
                self._Rect_Handles = {}
            Handles = self._Rect_Handles.get(ID, [])
            if self._Selected_Rect_ID == ID:
                Handles = self._Draw_Point_Handles(Corners, Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Rect_Handles[ID] = Handles
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rect_Draw -> {E}")

    def Add_Rectangle(self, X=None, Y=None, Width=None, Height=None, Angle=0, Thickness=2, Color="#4F8EF7", Fill="#dc7633", Transparent=False):
        try:
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            if X is None:
                X = CW / 2.0
            if Y is None:
                Y = CH / 2.0
            if Width is None:
                Width = CW * 0.2
            if Height is None:
                Height = CH * 0.15
            ID = self._Rect_ID_Next
            self._Rect_ID_Next += 1
            self._Rectangles[ID] = (float(X), float(Y), float(Width), float(Height), float(Angle), float(Thickness), str(Color), str(Fill), None)
            self._Rect_Transparent[ID] = bool(Transparent)
            self.Render()
            self._Callback_Invoke("Rectangle", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Rectangle -> {E}")

    def Update_Rectangle(self, ID=None, X=None, Y=None, Width=None, Height=None, Angle=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None, Disable_Rotation=None):
        try:
            if ID is None:
                if not self._Rectangles:
                    return
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            C0x, C0y, W0, H0, A0, T0, OCol0, FCol0, Item0 = self._Rectangles[ID]
            X = X if X is not None else C0x
            Y = Y if Y is not None else C0y
            Width = max(2.0, Width if Width is not None else W0)
            Height = max(2.0, Height if Height is not None else H0)
            Angle = self.Normalize_Angle(Angle if Angle is not None else A0)
            Thickness = Thickness if Thickness is not None else T0
            Color = Color if Color is not None else OCol0
            Fill = Fill if Fill is not None else FCol0
            self._Rectangles[ID] = (float(X), float(Y), float(Width), float(Height), float(Angle), float(Thickness), str(Color), str(Fill), Item0)
            if Transparent is not None:
                self._Rect_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Rect_Disabled[ID] = bool(Disabled)
            if Disable_Rotation is not None:
                self._Rect_Disable_Rotation[ID] = bool(Disable_Rotation)
            self.Rect_Draw(ID)
            self._Callback_Invoke("Rectangle", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Rectangle -> {E}")

    def Get_Rectangle(self, ID=None):
        try:
            if not self._Rectangles:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Rectangles.keys()):
                    X, Y, Width, Height, Angle, Thickness, Color, Fill, Item = self._Rectangles[Each_ID]
                    Out_List.append({"ID": Each_ID, "X": X, "Y": Y, "Width": Width, "Height": Height, "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Rect_Transparent.get(Each_ID, False))})
                return Out_List
            if ID is None:
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return None
            X, Y, Width, Height, Angle, Thickness, Color, Fill, Item = self._Rectangles[ID]
            return {"X": X, "Y": Y, "Width": Width, "Height": Height, "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Rect_Transparent.get(ID, False))}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Rectangle -> {E}")

    def Remove_Rectangle(self, ID=None):
        try:
            if not self._Rectangles:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Rectangles.items()):
                    self._Callback_Invoke("Rectangle", ID=Each_ID, Event="Remove")
                    Item = Data[8]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Rect_Handles"):
                        Handles = self._Rect_Handles.pop(Each_ID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                    if Each_ID in self._Rect_Transparent:
                        del self._Rect_Transparent[Each_ID]
                self._Rectangles.clear()
                self._Selected_Rect_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            self._Callback_Invoke("Rectangle", ID=ID, Event="Remove")
            Item = self._Rectangles[ID][8]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Rect_Handles"):
                Handles = self._Rect_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)
            del self._Rectangles[ID]
            if ID in self._Rect_Transparent:
                del self._Rect_Transparent[ID]
            if self._Selected_Rect_ID == ID:
                self._Selected_Rect_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Rectangle -> {E}")

    def Enable_Rectangle(self, ID=None):
        try:
            if ID is None:
                if not self._Rectangles:
                    return
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            self._Rect_Disabled[ID] = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Enable_Rectangle -> {E}")

    def Disable_Rectangle(self, ID=None):
        try:
            if ID is None:
                if not self._Rectangles:
                    return
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            self._Rect_Disabled[ID] = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Disable_Rectangle -> {E}")

    def Point_In_Circle(self, ID, X, Y):
        try:
            if ID not in self._Circles:
                return False
            Cx, Cy, Radius, Thickness, Color, Fill, Item = self._Circles[ID]
            Dx = X - Cx
            Dy = Y - Cy
            return Dx * Dx + Dy * Dy <= Radius * Radius
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Point_In_Circle -> {E}")

    def _Circle_Unit_Points(self, Steps):
        try:
            Steps = int(max(8, Steps))
            if not hasattr(self, "_Circle_Unit_Cache"):
                self._Circle_Unit_Cache = {}
            Cached = self._Circle_Unit_Cache.get(Steps, None)
            if Cached is not None:
                return Cached
            Out = []
            Step = 2.0 * math.pi / float(Steps)
            A = 0.0
            for _ in range(Steps):
                Out.append((math.cos(A), math.sin(A)))
                A += Step
            self._Circle_Unit_Cache[Steps] = Out
            return Out
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Circle_Unit_Points -> {E}")
            return [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]
            
    def _Circle_Steps_For_Radius(self, Radius):
        try:
            Target_Edge_Px = 7.0
            Steps = int((2.0 * math.pi * float(max(1.0, Radius))) / Target_Edge_Px)
            Steps = max(16, min(96, Steps))
            Steps = int(round(Steps / 8.0) * 8)
            Steps = max(16, min(96, Steps))
            return Steps
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Circle_Steps_For_Radius -> {E}")
            return 48

    def Circle_Draw(self, ID):
        try:
            if ID not in self._Circles:
                return
            Cx, Cy, Radius, Thickness, Color, Fill, Item = self._Circles[ID]
            Transparent = bool(self._Circle_Transparent.get(ID, False))
            Mode = getattr(self, "_Circle_Render_Mode", "auto")
            UsePoly = True if Mode == "polygon" else (False if Mode == "oval" else Transparent)
            Width_Draw = Thickness * (2 if self._Selected_Circle_ID == ID else 1)
            Stipple = ("gray25" if Transparent else "")
            if UsePoly:
                Steps = self._Circle_Steps_For_Radius(Radius)
                Unit = self._Circle_Unit_Points(Steps)
                Screen = []
                for Ux, Uy in Unit:
                    Screen.append(Cx + Radius * Ux)
                    Screen.append(Cy + Radius * Uy)
                if Item:
                    try:
                        if self._Canvas._Frame.type(Item) != "polygon":
                            self._Canvas.Delete_Item(Item)
                            Item = None
                    except:
                        pass
                if not Item:
                    Item = self._Canvas._Frame.create_polygon(Screen, outline=Color, fill=Fill, stipple=Stipple, width=Width_Draw, smooth=True)
                    self._Circles[ID] = (Cx, Cy, Radius, Thickness, Color, Fill, Item)
                else:
                    self._Canvas._Frame.coords(Item, Screen)
                    self._Canvas._Frame.itemconfigure(Item, outline=Color, fill=Fill, stipple=Stipple, width=Width_Draw, state="normal")
            else:
                X1 = Cx - Radius
                Y1 = Cy - Radius
                X2 = Cx + Radius
                Y2 = Cy + Radius
                if Item:
                    try:
                        if self._Canvas._Frame.type(Item) != "oval":
                            self._Canvas.Delete_Item(Item)
                            Item = None
                    except:
                        pass
                if not Item:
                    Item = self._Canvas._Frame.create_oval(X1, Y1, X2, Y2, outline=Color, fill=Fill, width=Width_Draw)
                    self._Circles[ID] = (Cx, Cy, Radius, Thickness, Color, Fill, Item)
                else:
                    self._Canvas._Frame.coords(Item, X1, Y1, X2, Y2)
                    self._Canvas._Frame.itemconfigure(Item, outline=Color, fill=Fill, width=Width_Draw, state="normal")
                self._Canvas._Frame.itemconfigure(Item, stipple=Stipple)
            self._Canvas._Frame.tag_raise(Item)
            if not hasattr(self, "_Circle_Handles"):
                self._Circle_Handles = {}
            Handles = self._Circle_Handles.get(ID, [])
            if self._Selected_Circle_ID == ID:
                Handles = self._Draw_Point_Handles([(Cx, Cy)], Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Circle_Handles[ID] = Handles
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Circle_Draw -> {E}")

    def Add_Circle(self, X=None, Y=None, Radius=None, Thickness=2, Color="#4F8EF7", Fill="#a569bd", Transparent=False):
        try:
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            if X is None:
                X = CW / 2.0
            if Y is None:
                Y = CH / 2.0
            if Radius is None:
                Radius = min(CW, CH) * 0.1
            ID = self._Circle_ID_Next
            self._Circle_ID_Next += 1
            self._Circles[ID] = (float(X), float(Y), float(Radius), float(Thickness), str(Color), str(Fill), None)
            self._Circle_Transparent[ID] = bool(Transparent)
            self.Render()
            self._Callback_Invoke("Circle", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Circle -> {E}")

    def Update_Circle(self, ID=None, X=None, Y=None, Radius=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None):
        try:
            if ID is None:
                if not self._Circles:
                    return
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            C0x, C0y, R0, T0, OCol0, FCol0, Item0 = self._Circles[ID]
            X = X if X is not None else C0x
            Y = Y if Y is not None else C0y
            Radius = max(1.0, Radius if Radius is not None else R0)
            Thickness = Thickness if Thickness is not None else T0
            Color = Color if Color is not None else OCol0
            Fill = Fill if Fill is not None else FCol0
            self._Circles[ID] = (float(X), float(Y), float(Radius), float(Thickness), str(Color), str(Fill), Item0)
            if Transparent is not None:
                self._Circle_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Circle_Disabled[ID] = bool(Disabled)
            self.Circle_Draw(ID)
            self._Callback_Invoke("Circle", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Circle -> {E}")

    def Get_Circle(self, ID=None):
        try:
            if not self._Circles:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Circles.keys()):
                    X, Y, Radius, Thickness, Color, Fill, Item = self._Circles[Each_ID]
                    Out_List.append({"ID": Each_ID, "X": X, "Y": Y, "Radius": Radius, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Circle_Transparent.get(Each_ID, False))})
                return Out_List
            if ID is None:
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return None
            X, Y, Radius, Thickness, Color, Fill, Item = self._Circles[ID]
            return {"X": X, "Y": Y, "Radius": Radius, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Circle_Transparent.get(ID, False))}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Circle -> {E}")

    def Remove_Circle(self, ID=None):
        try:
            if not self._Circles:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Circles.items()):
                    self._Callback_Invoke("Circle", ID=Each_ID, Event="Remove")
                    Item = Data[6]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Circle_Handles"):
                        Handles = self._Circle_Handles.pop(Each_ID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                    if Each_ID in self._Circle_Transparent:
                        del self._Circle_Transparent[Each_ID]
                self._Circles.clear()
                self._Selected_Circle_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            self._Callback_Invoke("Circle", ID=ID, Event="Remove")
            Item = self._Circles[ID][6]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Circle_Handles"):
                Handles = self._Circle_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)
            del self._Circles[ID]
            if ID in self._Circle_Transparent:
                del self._Circle_Transparent[ID]
            if self._Selected_Circle_ID == ID:
                self._Selected_Circle_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Circle -> {E}")

    def Enable_Circle(self, ID=None):
        try:
            if ID is None:
                if not self._Circles:
                    return
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            self._Circle_Disabled[ID] = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Enable_Circle -> {E}")

    def Disable_Circle(self, ID=None):
        try:
            if ID is None:
                if not self._Circles:
                    return
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            self._Circle_Disabled[ID] = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Disable_Circle -> {E}")

    def Quad_Center(self, Points):
        Cx = 0.0
        Cy = 0.0
        for X, Y in Points:
            Cx += X
            Cy += Y
        return (Cx / 4.0, Cy / 4.0)

    def Point_In_Quad(self, ID, X, Y):
        try:
            if ID not in self._Quadrilaterals:
                return False
            P1, P2, P3, P4, Angle, Thickness, Color, Fill, Item = self._Quadrilaterals[ID]
            Poly = [P1, P2, P3, P4]
            Inside = False
            J = 3
            for I in range(4):
                Xi, Yi = Poly[I]
                Xj, Yj = Poly[J]
                Intersect = ((Yi > Y) != (Yj > Y)) and (X < (Xj - Xi) * (Y - Yi) / max(1e-12, (Yj - Yi)) + Xi)
                if Intersect:
                    Inside = not Inside
                J = I
            return Inside
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Point_In_Quad -> {E}")
            return False

    def Quad_Corner_Hit(self, ID, X, Y, Tol):
        try:
            if ID not in self._Quadrilaterals:
                return None, None
            P1, P2, P3, P4, Angle, Thickness, Color, Fill, Item = self._Quadrilaterals[ID]
            Points = [P1, P2, P3, P4]
            Best_I = None
            Best_D = None
            for I, (Px, Py) in enumerate(Points):
                D = math.hypot(X - Px, Y - Py)
                if Best_D is None or D < Best_D:
                    Best_D = D
                    Best_I = I
            if Best_D is not None and Best_D <= Tol * 1.15:
                return Best_I, Best_D
            return None, None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Quad_Corner_Hit -> {E}")
            return None, None

    def Quad_Draw(self, ID):
        try:
            if ID not in self._Quadrilaterals:
                return
            P1, P2, P3, P4, Angle, Thickness, Color, Fill, Item = self._Quadrilaterals[ID]
            Transparent = bool(self._Quad_Transparent.get(ID, False))
            Points = [P1, P2, P3, P4]
            Screen = []
            for X, Y in Points:
                Screen.append(X)
                Screen.append(Y)
            Width_Draw = Thickness * (2 if self._Selected_Quad_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_polygon(*Screen, outline=Color, fill=Fill, width=Width_Draw)
                self._Quadrilaterals[ID] = (P1, P2, P3, P4, Angle, Thickness, Color, Fill, Item)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(Item, outline=Color, fill=Fill, width=Width_Draw, state="normal")
            self._Canvas._Frame.itemconfigure(Item, stipple=("gray25" if Transparent else ""))
            self._Canvas._Frame.tag_raise(Item)
            if not hasattr(self, "_Quad_Handles"):
                self._Quad_Handles = {}
            Handles = self._Quad_Handles.get(ID, [])
            if self._Selected_Quad_ID == ID:
                Handles = self._Draw_Point_Handles(Points, Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Quad_Handles[ID] = Handles
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Quad_Draw -> {E}")

    def Add_Quadrilateral(self, P1=None, P2=None, P3=None, P4=None, Angle=0, Thickness=2, Color="#4F8EF7", Fill="#45b39d", Transparent=False):
        try:
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            Center_X = CW / 2.0
            Center_Y = CH / 2.0
            Default_W = CW * 0.25
            Default_H = CH * 0.25
            Default_P1 = [Center_X - Default_W * 0.5, Center_Y - Default_H * 0.5]
            Default_P2 = [Center_X + Default_W * 0.5, Center_Y - Default_H * 0.5]
            Default_P3 = [Center_X + Default_W * 0.5, Center_Y + Default_H * 0.5]
            Default_P4 = [Center_X - Default_W * 0.5, Center_Y + Default_H * 0.5]
            if P1 is None:
                P1 = Default_P1
            if P2 is None:
                P2 = Default_P2
            if P3 is None:
                P3 = Default_P3
            if P4 is None:
                P4 = Default_P4
            P1 = [float(P1[0]), float(P1[1])]
            P2 = [float(P2[0]), float(P2[1])]
            P3 = [float(P3[0]), float(P3[1])]
            P4 = [float(P4[0]), float(P4[1])]
            ID = self._Quad_ID_Next
            self._Quad_ID_Next += 1
            self._Quadrilaterals[ID] = (P1, P2, P3, P4, float(Angle), float(Thickness), str(Color), str(Fill), None)
            self._Quad_Transparent[ID] = bool(Transparent)
            self.Render()
            self._Callback_Invoke("Quadrilateral", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Quadrilateral -> {E}")

    def Update_Quadrilateral(self, ID=None, P1=None, P2=None, P3=None, P4=None, Angle=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None):
        try:
            if ID is None:
                if not self._Quadrilaterals:
                    return
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            P10, P20, P30, P40, A0, T0, OCol0, FCol0, Item0 = self._Quadrilaterals[ID]
            if P1 is None:
                P1 = P10
            if P2 is None:
                P2 = P20
            if P3 is None:
                P3 = P30
            if P4 is None:
                P4 = P40
            P1 = [float(P1[0]), float(P1[1])]
            P2 = [float(P2[0]), float(P2[1])]
            P3 = [float(P3[0]), float(P3[1])]
            P4 = [float(P4[0]), float(P4[1])]
            Angle = float(Angle) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(OCol0)
            Fill = str(Fill) if Fill is not None else str(FCol0)
            self._Quadrilaterals[ID] = (P1, P2, P3, P4, Angle, Thickness, Color, Fill, Item0)
            if Transparent is not None:
                self._Quad_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Quad_Disabled[ID] = bool(Disabled)
            self.Quad_Draw(ID)
            self._Callback_Invoke("Quadrilateral", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Quadrilateral -> {E}")

    def Get_Quadrilateral(self, ID=None):
        try:
            if not self._Quadrilaterals:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Quadrilaterals.keys()):
                    P1, P2, P3, P4, Angle, Thickness, Color, Fill, Item = self._Quadrilaterals[Each_ID]
                    Out_List.append({"ID": Each_ID, "P1": [P1[0], P1[1]], "P2": [P2[0], P2[1]], "P3": [P3[0], P3[1]], "P4": [P4[0], P4[1]], "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Quad_Transparent.get(Each_ID, False))})
                return Out_List
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return None
            P1, P2, P3, P4, Angle, Thickness, Color, Fill, Item = self._Quadrilaterals[ID]
            return {"P1": [P1[0], P1[1]], "P2": [P2[0], P2[1]], "P3": [P3[0], P3[1]], "P4": [P4[0], P4[1]], "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Quad_Transparent.get(ID, False))}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Quadrilateral -> {E}")

    def Remove_Quadrilateral(self, ID=None):
        try:
            if not self._Quadrilaterals:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Quadrilaterals.items()):
                    self._Callback_Invoke("Quadrilateral", ID=Each_ID, Event="Remove")
                    Item = Data[8]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Quad_Handles"):
                        Handles = self._Quad_Handles.pop(Each_ID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                    if Each_ID in self._Quad_Transparent:
                        del self._Quad_Transparent[Each_ID]
                self._Quadrilaterals.clear()
                self._Selected_Quad_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            self._Callback_Invoke("Quadrilateral", ID=ID, Event="Remove")
            Item = self._Quadrilaterals[ID][8]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Quad_Handles"):
                Handles = self._Quad_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)
            del self._Quadrilaterals[ID]
            if ID in self._Quad_Transparent:
                del self._Quad_Transparent[ID]
            if self._Selected_Quad_ID == ID:
                self._Selected_Quad_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Quadrilateral -> {E}")

    def Enable_Quadrilateral(self, ID=None):
        try:
            if ID is None:
                if not self._Quadrilaterals:
                    return
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            self._Quad_Disabled[ID] = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Enable_Quadrilateral -> {E}")

    def Disable_Quadrilateral(self, ID=None):
        try:
            if ID is None:
                if not self._Quadrilaterals:
                    return
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            self._Quad_Disabled[ID] = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Disable_Quadrilateral -> {E}")

    def _Line_Endpoint_Hit(self, ID, X, Y, Tol):
        try:
            if ID not in self._Lines:
                return None, None
            Points, Angle, Thickness, Color, Item, Handles = self._Lines[ID]
            if not Points or len(Points) < 2:
                return None, None
            Best_I = None
            Best_D = None
            for I, (Px, Py) in enumerate(Points[:2]):
                D = math.hypot(X - Px, Y - Py)
                if Best_D is None or D < Best_D:
                    Best_D = D
                    Best_I = I
            if Best_D is not None and Best_D <= Tol * 1.15:
                return Best_I, Best_D
            return None, None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Line_Endpoint_Hit -> {E}")
            return None, None

    def Point_On_Line(self, ID, X, Y, Tol):
        try:
            if ID not in self._Lines:
                return False
            Points, Angle, Thickness, Color, Item, Handles = self._Lines[ID]
            if not Points or len(Points) < 2:
                return False
            (X1, Y1), (X2, Y2) = Points[:2]
            D, _ = self._Distance_Point_To_Segment(X, Y, X1, Y1, X2, Y2)
            return D <= Tol * 1.5
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Point_On_Line -> {E}")
            return False

    def _Line_Center(self, Points):
        try:
            (X1, Y1), (X2, Y2) = Points[:2]
            return ((X1 + X2) * 0.5, (Y1 + Y2) * 0.5)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Line_Center -> {E}")
            return (0.0, 0.0)

    def Line_Draw(self, ID):
        try:
            if ID not in self._Lines:
                return
            Points, Angle, Thickness, Color, Item, Handles = self._Lines[ID]
            if not Points or len(Points) < 2:
                return
            X1, Y1 = Points[0]
            X2, Y2 = Points[1]
            Width_Draw = Thickness * (2 if self._Selected_Line_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_line(X1, Y1, X2, Y2, fill=Color, width=Width_Draw)
            else:
                self._Canvas._Frame.coords(Item, X1, Y1, X2, Y2)
                self._Canvas._Frame.itemconfigure(Item, fill=Color, width=Width_Draw, state="normal")
                self._Canvas._Frame.tag_raise(Item)
            if self._Selected_Line_ID == ID:
                Handles = self._Draw_Point_Handles([(Points[0][0], Points[0][1]), (Points[1][0], Points[1][1])], Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Lines[ID] = (Points, Angle, Thickness, Color, Item, Handles)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Line_Draw -> {E}")

    def Add_Line(self, Points=None, Angle=0, Thickness=2, Color="#ec7063"):
        try:
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            Center_X = CW / 2.0
            Center_Y = CH / 2.0
            Default_L = min(CW, CH) * 0.35
            X1 = Center_X - 0.5 * Default_L
            Y1 = Center_Y
            X2 = Center_X + 0.5 * Default_L
            Y2 = Center_Y
            if Points is None:
                Points = [[X1, Y1], [X2, Y2]]
            if not isinstance(Points, (list, tuple)) or len(Points) < 2:
                return None
            P0 = (float(Points[0][0]), float(Points[0][1]))
            P1p = (float(Points[1][0]), float(Points[1][1]))
            ID = self._Line_ID_Next
            self._Line_ID_Next += 1
            self._Lines[ID] = ([P0, P1p], float(Angle), float(Thickness), str(Color), None, [])
            self.Render()
            self._Callback_Invoke("Line", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Line -> {E}")

    def Update_Line(self, ID=None, Points=None, Angle=None, Thickness=None, Color=None, Disabled=None):
        try:
            if ID is None:
                if not self._Lines:
                    return
                ID = sorted(self._Lines.keys())[0]
            if ID not in self._Lines:
                return
            P0, A0, T0, C0, Item0, Handles0 = self._Lines[ID]
            if Points is None:
                Points = P0
            if not isinstance(Points, (list, tuple)) or len(Points) < 2:
                return
            Points_Out = [(float(Points[0][0]), float(Points[0][1])), (float(Points[1][0]), float(Points[1][1]))]
            Angle = float(Angle) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(C0)
            self._Lines[ID] = (Points_Out, Angle, Thickness, Color, Item0, Handles0)
            if Disabled is not None:
                self._Line_Disabled[ID] = bool(Disabled)
            self.Line_Draw(ID)
            self._Callback_Invoke("Line", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Line -> {E}")

    def Get_Line(self, ID=None):
        try:
            if not self._Lines:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Lines.keys()):
                    Points, Angle, Thickness, Color, Item, Handles = self._Lines[Each_ID]
                    Out_List.append({"ID": Each_ID, "Points": [[Points[0][0], Points[0][1]], [Points[1][0], Points[1][1]]], "Angle": Angle, "Thickness": Thickness, "Color": Color})
                return Out_List
            if ID is None:
                ID = sorted(self._Lines.keys())[0]
            if ID not in self._Lines:
                return None
            Points, Angle, Thickness, Color, Item, Handles = self._Lines[ID]
            return {"Points": [[Points[0][0], Points[0][1]], [Points[1][0], Points[1][1]]], "Angle": Angle, "Thickness": Thickness, "Color": Color}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Line -> {E}")

    def Remove_Line(self, ID=None):
        try:
            if not self._Lines:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Lines.items()):
                    self._Callback_Invoke("Line", ID=Each_ID, Event="Remove")
                    Item = Data[4]
                    Handles = Data[5]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    self._Clear_Handles(Handles)
                self._Lines.clear()
                self._Selected_Line_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Lines.keys())[0]
            if ID not in self._Lines:
                return
            self._Callback_Invoke("Line", ID=ID, Event="Remove")
            Item = self._Lines[ID][4]
            Handles = self._Lines[ID][5]
            if Item:
                self._Canvas.Delete_Item(Item)
            self._Clear_Handles(Handles)
            del self._Lines[ID]
            if self._Selected_Line_ID == ID:
                self._Selected_Line_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Line -> {E}")

    def Enable_Line(self, ID=None):
        try:
            if ID is None:
                if not self._Lines:
                    return
                ID = sorted(self._Lines.keys())[0]
            if ID not in self._Lines:
                return
            self._Line_Disabled[ID] = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Enable_Line -> {E}")

    def Disable_Line(self, ID=None):
        try:
            if ID is None:
                if not self._Lines:
                    return
                ID = sorted(self._Lines.keys())[0]
            if ID not in self._Lines:
                return
            self._Line_Disabled[ID] = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Disable_Line -> {E}")

    def _Point_On_Polyline(self, Points, X, Y, Tol):
        try:
            I, D, T = self._Closest_Segment_Index(Points, X, Y)
            if D is None:
                return False
            return D <= Tol * 1.5
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Point_On_Polyline -> {E}")
            return False

    def Polyline_Draw(self, ID):
        try:
            if ID not in self._Polylines:
                return
            Points, Angle, Thickness, Color, Item, Handles = self._Polylines[ID]
            if not Points or len(Points) < 2:
                return
            Screen = []
            for X, Y in Points:
                Screen.append(X)
                Screen.append(Y)
            Width_Draw = Thickness * (2 if self._Selected_Polyline_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_line(*Screen, fill=Color, width=Width_Draw)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(Item, fill=Color, width=Width_Draw, state="normal")
                self._Canvas._Frame.tag_raise(Item)
            if self._Selected_Polyline_ID == ID:
                Handles = self._Draw_Point_Handles(Points, Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Polylines[ID] = (Points, Angle, Thickness, Color, Item, Handles)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polyline_Draw -> {E}")

    def Add_Polyline(self, Points=None, Angle=0, Thickness=2, Color="#5d6d7e"):
        try:
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            Center_X = CW / 2.0
            Center_Y = CH / 2.0
            D = min(CW, CH) * 0.18
            Default = [(Center_X - D, Center_Y - D), (Center_X, Center_Y), (Center_X + D, Center_Y - D)]
            if Points is None:
                Points = Default
            if not isinstance(Points, (list, tuple)) or len(Points) < 3:
                return None
            Points_Out = [(float(P[0]), float(P[1])) for P in Points]
            ID = self._Polyline_ID_Next
            self._Polyline_ID_Next += 1
            self._Polylines[ID] = (Points_Out, float(Angle), float(Thickness), str(Color), None, [])
            self.Render()
            self._Callback_Invoke("Polyline", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Polyline -> {E}")

    def Update_Polyline(self, ID=None, Points=None, Angle=None, Thickness=None, Color=None, Disabled=None):
        try:
            if ID is None:
                if not self._Polylines:
                    return
                ID = sorted(self._Polylines.keys())[0]
            if ID not in self._Polylines:
                return
            P0, A0, T0, C0, Item0, Handles0 = self._Polylines[ID]
            if Points is None:
                Points = P0
            if not isinstance(Points, (list, tuple)) or len(Points) < 3:
                return
            Points_Out = [(float(P[0]), float(P[1])) for P in Points]
            Angle = float(Angle) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(C0)
            self._Polylines[ID] = (Points_Out, Angle, Thickness, Color, Item0, Handles0)
            if Disabled is not None:
                self._Polyline_Disabled[ID] = bool(Disabled)
            self.Polyline_Draw(ID)
            self._Callback_Invoke("Polyline", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Polyline -> {E}")

    def Get_Polyline(self, ID=None):
        try:
            if not self._Polylines:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Polylines.keys()):
                    Points, Angle, Thickness, Color, Item, Handles = self._Polylines[Each_ID]
                    Out_List.append({"ID": Each_ID, "Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color})
                return Out_List
            if ID is None:
                ID = sorted(self._Polylines.keys())[0]
            if ID not in self._Polylines:
                return None
            Points, Angle, Thickness, Color, Item, Handles = self._Polylines[ID]
            return {"Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Polyline -> {E}")

    def Remove_Polyline(self, ID=None):
        try:
            if not self._Polylines:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Polylines.items()):
                    self._Callback_Invoke("Polyline", ID=Each_ID, Event="Remove")
                    Item = Data[4]
                    Handles = Data[5]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    self._Clear_Handles(Handles)
                self._Polylines.clear()
                self._Selected_Polyline_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Polylines.keys())[0]
            if ID not in self._Polylines:
                return
            self._Callback_Invoke("Polyline", ID=ID, Event="Remove")
            Item = self._Polylines[ID][4]
            Handles = self._Polylines[ID][5]
            if Item:
                self._Canvas.Delete_Item(Item)
            self._Clear_Handles(Handles)
            del self._Polylines[ID]
            if self._Selected_Polyline_ID == ID:
                self._Selected_Polyline_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Polyline -> {E}")

    def _Insert_Point_In_Polyline(self, ID, X, Y):
        try:
            if ID not in self._Polylines:
                return
            Points, Angle, Thickness, Color, Item, Handles = self._Polylines[ID]
            I, D, T = self._Closest_Segment_Index(Points, X, Y)
            if I is None:
                return
            Points2 = list(Points)
            Points2.insert(I + 1, (float(X), float(Y)))
            self._Polylines[ID] = (Points2, Angle, Thickness, Color, Item, Handles)
            self.Polyline_Draw(ID)
            self._Callback_Invoke("Polyline", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Insert_Point_In_Polyline -> {E}")

    def Enable_Polyline(self, ID=None):
        try:
            if ID is None:
                if not self._Polylines:
                    return
                ID = sorted(self._Polylines.keys())[0]
            if ID not in self._Polylines:
                return
            self._Polyline_Disabled[ID] = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Enable_Polyline -> {E}")

    def Disable_Polyline(self, ID=None):
        try:
            if ID is None:
                if not self._Polylines:
                    return
                ID = sorted(self._Polylines.keys())[0]
            if ID not in self._Polylines:
                return
            self._Polyline_Disabled[ID] = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Disable_Polyline -> {E}")

    def _Poly_Center(self, Points):
        try:
            if not Points:
                return (0.0, 0.0)
            Cx = 0.0
            Cy = 0.0
            for X, Y in Points:
                Cx += X
                Cy += Y
            N = float(len(Points))
            return (Cx / N, Cy / N)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Poly_Center -> {E}")
            return (0.0, 0.0)

    def _Poly_Point_Hit(self, Points, X, Y, Tol):
        try:
            if not Points:
                return None, None
            Best_I = None
            Best_D = None
            for I, (Px, Py) in enumerate(Points):
                D = math.hypot(X - Px, Y - Py)
                if Best_D is None or D < Best_D:
                    Best_D = D
                    Best_I = I
            if Best_D is not None and Best_D <= Tol * 1.15:
                return Best_I, Best_D
            return None, None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Poly_Point_Hit -> {E}")
            return None, None

    def _Point_In_Polygon(self, Points, X, Y):
        try:
            if not Points or len(Points) < 3:
                return False
            Inside = False
            J = len(Points) - 1
            for I in range(len(Points)):
                Xi, Yi = Points[I]
                Xj, Yj = Points[J]
                Intersect = ((Yi > Y) != (Yj > Y)) and (X < (Xj - Xi) * (Y - Yi) / max(1e-12, (Yj - Yi)) + Xi)
                if Intersect:
                    Inside = not Inside
                J = I
            return Inside
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Point_In_Polygon -> {E}")
            return False

    def _Point_On_Polygon_Edge(self, Points, X, Y, Tol):
        try:
            I, D, T = self._Closest_Edge_Index(Points, X, Y)
            if D is None:
                return False
            return D <= Tol * 1.5
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Point_On_Polygon_Edge -> {E}")
            return False

    def Polygon_Draw(self, ID):
        try:
            if ID not in self._Polygons:
                return
            Points, Angle, Thickness, Color, Fill, Item, Handles = self._Polygons[ID]
            if not Points or len(Points) < 3:
                return
            Transparent = bool(self._Polygon_Transparent.get(ID, False))
            Screen = []
            for X, Y in Points:
                Screen.append(X)
                Screen.append(Y)
            Width_Draw = Thickness * (2 if self._Selected_Polygon_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_polygon(*Screen, outline=Color, fill=Fill, width=Width_Draw)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(Item, outline=Color, fill=Fill, width=Width_Draw, state="normal")
            self._Canvas._Frame.itemconfigure(Item, stipple=("gray25" if Transparent else ""))
            self._Canvas._Frame.tag_raise(Item)
            if self._Selected_Polygon_ID == ID:
                Handles = self._Draw_Point_Handles(Points, Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Polygons[ID] = (Points, Angle, Thickness, Color, Fill, Item, Handles)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polygon_Draw -> {E}")

    def Add_Polygon(self, Points=None, Angle=0, Thickness=2, Color="#4F8EF7", Fill="#5499c7", Transparent=False):
        try:
            CW = self.Canvas_Width()
            CH = self.Canvas_Height()
            Center_X = CW / 2.0
            Center_Y = CH / 2.0
            D = min(CW, CH) * 0.20
            Default = [(Center_X, Center_Y - D), (Center_X + D, Center_Y + D), (Center_X - D, Center_Y + D)]
            if Points is None:
                Points = Default
            if not isinstance(Points, (list, tuple)) or len(Points) < 3:
                return None
            Points_Out = [(float(P[0]), float(P[1])) for P in Points]
            ID = self._Polygon_ID_Next
            self._Polygon_ID_Next += 1
            self._Polygons[ID] = (Points_Out, float(Angle), float(Thickness), str(Color), str(Fill), None, [])
            self._Polygon_Transparent[ID] = bool(Transparent)
            self.Render()
            self._Callback_Invoke("Polygon", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Polygon -> {E}")

    def Update_Polygon(self, ID=None, Points=None, Angle=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None):
        try:
            if ID is None:
                if not self._Polygons:
                    return
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return
            P0, A0, T0, OC0, FC0, Item0, Handles0 = self._Polygons[ID]
            if Points is None:
                Points = P0
            if not isinstance(Points, (list, tuple)) or len(Points) < 3:
                return
            Points_Out = [(float(P[0]), float(P[1])) for P in Points]
            Angle = float(Angle) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(OC0)
            Fill = str(Fill) if Fill is not None else str(FC0)
            self._Polygons[ID] = (Points_Out, Angle, Thickness, Color, Fill, Item0, Handles0)
            if Transparent is not None:
                self._Polygon_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Polygon_Disabled[ID] = bool(Disabled)
            self.Polygon_Draw(ID)
            self._Callback_Invoke("Polygon", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Polygon -> {E}")

    def Get_Polygon(self, ID=None):
        try:
            if not self._Polygons:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Polygons.keys()):
                    Points, Angle, Thickness, Color, Fill, Item, Handles = self._Polygons[Each_ID]
                    Out_List.append({"ID": Each_ID, "Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Polygon_Transparent.get(Each_ID, False))})
                return Out_List
            if ID is None:
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return None
            Points, Angle, Thickness, Color, Fill, Item, Handles = self._Polygons[ID]
            return {"Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": Fill, "Transparent": bool(self._Polygon_Transparent.get(ID, False))}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Polygon -> {E}")

    def Remove_Polygon(self, ID=None):
        try:
            if not self._Polygons:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Polygons.items()):
                    self._Callback_Invoke("Polygon", ID=Each_ID, Event="Remove")
                    Item = Data[5]
                    Handles = Data[6]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    self._Clear_Handles(Handles)
                    if Each_ID in self._Polygon_Transparent:
                        del self._Polygon_Transparent[Each_ID]
                self._Polygons.clear()
                self._Selected_Polygon_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return
            self._Callback_Invoke("Polygon", ID=ID, Event="Remove")
            Item = self._Polygons[ID][5]
            Handles = self._Polygons[ID][6]
            if Item:
                self._Canvas.Delete_Item(Item)
            self._Clear_Handles(Handles)
            del self._Polygons[ID]
            if ID in self._Polygon_Transparent:
                del self._Polygon_Transparent[ID]
            if self._Selected_Polygon_ID == ID:
                self._Selected_Polygon_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Polygon -> {E}")

    def _Insert_Point_In_Polygon(self, ID, X, Y):
        try:
            if ID not in self._Polygons:
                return
            Points, Angle, Thickness, Color, Fill, Item, Handles = self._Polygons[ID]
            I, D, T = self._Closest_Edge_Index(Points, X, Y)
            if I is None:
                return
            Points2 = list(Points)
            Points2.insert(I + 1, (float(X), float(Y)))
            self._Polygons[ID] = (Points2, Angle, Thickness, Color, Fill, Item, Handles)
            self.Polygon_Draw(ID)
            self._Callback_Invoke("Polygon", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Insert_Point_In_Polygon -> {E}")

    def Enable_Polygon(self, ID=None):
        try:
            if ID is None:
                if not self._Polygons:
                    return
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return
            self._Polygon_Disabled[ID] = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Enable_Polygon -> {E}")

    def Disable_Polygon(self, ID=None):
        try:
            if ID is None:
                if not self._Polygons:
                    return
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return
            self._Polygon_Disabled[ID] = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Disable_Polygon -> {E}")

    def Pick_Shape(self, X, Y):
        try:
            Tol = self.Edge_Tolerance()
            for ID in reversed(list(self._Rectangles.keys())):
                if self._Rect_Disabled.get(ID, False):
                    continue
                if self.Point_In_Rect(ID, X, Y):
                    return ("rect", ID)
            for ID in reversed(list(self._Circles.keys())):
                if self._Circle_Disabled.get(ID, False):
                    continue
                if self.Point_In_Circle(ID, X, Y):
                    return ("circle", ID)
            for ID in reversed(list(self._Quadrilaterals.keys())):
                if self._Quad_Disabled.get(ID, False):
                    continue
                if self.Point_In_Quad(ID, X, Y):
                    return ("quad", ID)
            for ID in reversed(list(self._Polygons.keys())):
                if self._Polygon_Disabled.get(ID, False):
                    continue
                Points, Angle, Thickness, Color, Fill, Item, Handles = self._Polygons[ID]
                if self._Point_In_Polygon(Points, X, Y) or self._Point_On_Polygon_Edge(Points, X, Y, Tol):
                    return ("polygon", ID)
            for ID in reversed(list(self._Polylines.keys())):
                if self._Polyline_Disabled.get(ID, False):
                    continue
                Points, Angle, Thickness, Color, Item, Handles = self._Polylines[ID]
                if self._Point_On_Polyline(Points, X, Y, Tol):
                    return ("polyline", ID)
            for ID in reversed(list(self._Lines.keys())):
                if self._Line_Disabled.get(ID, False):
                    continue
                if self.Point_On_Line(ID, X, Y, Tol):
                    return ("line", ID)
            return (None, None)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pick_Shape -> {E}")
            return (None, None)

    def Motion(self, Event):
        try:
            CX = self._Canvas._Frame.canvasx(Event.x)
            CY = self._Canvas._Frame.canvasy(Event.y)
            Tol = self.Edge_Tolerance()
            if self._Selected_Rect_ID and not self._Rect_Disabled.get(self._Selected_Rect_ID, False):
                Grip, _, _ = self.Rect_Grip_Hit(self._Selected_Rect_ID, CX, CY, Tol)
                if Grip:
                    self._Canvas._Frame.config(cursor="sizing")
                    return
                if self.Point_In_Rect(self._Selected_Rect_ID, CX, CY):
                    self._Canvas._Frame.config(cursor="fleur")
                    return
                self._Canvas._Frame.config(cursor="exchange")
                return
            if self._Selected_Circle_ID and not self._Circle_Disabled.get(self._Selected_Circle_ID, False):
                Cx, Cy, Radius, Thickness, Color, Fill, Item = self._Circles[self._Selected_Circle_ID]
                D = math.hypot(CX - Cx, CY - Cy)
                if abs(D - Radius) <= Tol * 1.5:
                    self._Canvas._Frame.config(cursor="sizing")
                    return
                if self.Point_In_Circle(self._Selected_Circle_ID, CX, CY):
                    self._Canvas._Frame.config(cursor="fleur")
                    return
                self._Canvas._Frame.config(cursor="exchange")
                return
            if self._Selected_Quad_ID and not self._Quad_Disabled.get(self._Selected_Quad_ID, False):
                Corner_I, _ = self.Quad_Corner_Hit(self._Selected_Quad_ID, CX, CY, Tol)
                if Corner_I is not None:
                    self._Canvas._Frame.config(cursor="sizing")
                    return
                if self.Point_In_Quad(self._Selected_Quad_ID, CX, CY):
                    self._Canvas._Frame.config(cursor="fleur")
                    return
                self._Canvas._Frame.config(cursor="exchange")
                return
            if self._Selected_Line_ID and not self._Line_Disabled.get(self._Selected_Line_ID, False):
                End_I, _ = self._Line_Endpoint_Hit(self._Selected_Line_ID, CX, CY, Tol)
                if End_I is not None:
                    self._Canvas._Frame.config(cursor="sizing")
                    return
                if self.Point_On_Line(self._Selected_Line_ID, CX, CY, Tol):
                    self._Canvas._Frame.config(cursor="fleur")
                    return
                self._Canvas._Frame.config(cursor="exchange")
                return
            if self._Selected_Polyline_ID and not self._Polyline_Disabled.get(self._Selected_Polyline_ID, False):
                Points, Angle, Thickness, Color, Item, Handles = self._Polylines[self._Selected_Polyline_ID]
                Pi, _ = self._Poly_Point_Hit(Points, CX, CY, Tol)
                if Pi is not None:
                    self._Canvas._Frame.config(cursor="sizing")
                    return
                if self._Point_On_Polyline(Points, CX, CY, Tol):
                    self._Canvas._Frame.config(cursor="fleur")
                    return
                self._Canvas._Frame.config(cursor="exchange")
                return
            if self._Selected_Polygon_ID and not self._Polygon_Disabled.get(self._Selected_Polygon_ID, False):
                Points, Angle, Thickness, Color, Fill, Item, Handles = self._Polygons[self._Selected_Polygon_ID]
                Pi, _ = self._Poly_Point_Hit(Points, CX, CY, Tol)
                if Pi is not None:
                    self._Canvas._Frame.config(cursor="sizing")
                    return
                if self._Point_In_Polygon(Points, CX, CY) or self._Point_On_Polygon_Edge(Points, CX, CY, Tol):
                    self._Canvas._Frame.config(cursor="fleur")
                    return
                self._Canvas._Frame.config(cursor="exchange")
                return
            self._Canvas._Frame.config(cursor="arrow")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Motion -> {E}")

    def Release(self, Event):
        try:
            CX = self._Canvas._Frame.canvasx(Event.x)
            CY = self._Canvas._Frame.canvasy(Event.y)
            Moved = False
            if self._Drag_Start_Pos is not None:
                SX, SY = self._Drag_Start_Pos
                if math.hypot(CX - SX, CY - SY) > 2.0:
                    Moved = True
            if not Moved and self._Click_Target == ("empty", None):
                self._Selected_Rect_ID = None
                self._Selected_Circle_ID = None
                self._Selected_Quad_ID = None
                self._Selected_Line_ID = None
                self._Selected_Polyline_ID = None
                self._Selected_Polygon_ID = None
                self._Drag_Mode = "none"
                self._Drag_Start_Pos = None
                self._Resize_Info = None
                self._Click_Target = None
                self.Render()
                return
            Callback_Needed = False
            Callback_Type = None
            Callback_ID = None
            if self._Resize_Info:
                ID = self._Resize_Info.get("ID")
                Type = self._Resize_Info.get("Type", "")
                if "rect" in Type:
                    Callback_Type = "Rectangle"
                    Callback_ID = ID
                    Callback_Needed = True
                elif "circle" in Type:
                    Callback_Type = "Circle"
                    Callback_ID = ID
                    Callback_Needed = True
                elif "quad" in Type:
                    Callback_Type = "Quadrilateral"
                    Callback_ID = ID
                    Callback_Needed = True
                elif "polyline" in Type:
                    Callback_Type = "Polyline"
                    Callback_ID = ID
                    Callback_Needed = True
                elif "line" in Type:
                    Callback_Type = "Line"
                    Callback_ID = ID
                    Callback_Needed = True
                elif "polygon" in Type:
                    Callback_Type = "Polygon"
                    Callback_ID = ID
                    Callback_Needed = True
            elif self._Drag_Mode != "none":
                if self._Drag_Mode == "rect" and self._Selected_Rect_ID:
                    Callback_Type = "Rectangle"
                    Callback_ID = self._Selected_Rect_ID
                    Callback_Needed = True
                elif self._Drag_Mode == "circle" and self._Selected_Circle_ID:
                    Callback_Type = "Circle"
                    Callback_ID = self._Selected_Circle_ID
                    Callback_Needed = True
                elif self._Drag_Mode == "quad" and self._Selected_Quad_ID:
                    Callback_Type = "Quadrilateral"
                    Callback_ID = self._Selected_Quad_ID
                    Callback_Needed = True
                elif self._Drag_Mode == "line" and self._Selected_Line_ID:
                    Callback_Type = "Line"
                    Callback_ID = self._Selected_Line_ID
                    Callback_Needed = True
                elif self._Drag_Mode == "polyline" and self._Selected_Polyline_ID:
                    Callback_Type = "Polyline"
                    Callback_ID = self._Selected_Polyline_ID
                    Callback_Needed = True
                elif self._Drag_Mode == "polygon" and self._Selected_Polygon_ID:
                    Callback_Type = "Polygon"
                    Callback_ID = self._Selected_Polygon_ID
                    Callback_Needed = True
            if Callback_Needed and self._Callback_Mode == "Release":
                self._Callback_Invoke(Callback_Type, ID=Callback_ID, Event="Update")
            self._Drag_Mode = "none"
            self._Drag_Start_Pos = None
            self._Resize_Info = None
            self._Click_Target = None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Release -> {E}")
        
    def Drag_Start(self, Event):
        try:
            CX = self._Canvas._Frame.canvasx(Event.x)
            CY = self._Canvas._Frame.canvasy(Event.y)
            self._Drag_Last_X = CX
            self._Drag_Last_Y = CY
            X = CX
            Y = CY
            Now = time.time()
            Is_Double = False
            if self._Last_Click_Pos is not None:
                Last_X, Last_Y = self._Last_Click_Pos
                Time_Diff = Now - self._Last_Click_Time
                Dist = math.hypot(X - Last_X, Y - Last_Y)
                if Time_Diff < self._Double_Click_Threshold and Dist < 10:
                    Is_Double = True
            self._Last_Click_Time = Now
            self._Last_Click_Pos = (X, Y)
            if Is_Double:
                if self._Selected_Polyline_ID and not self._Polyline_Disabled.get(self._Selected_Polyline_ID, False):
                    Points, Angle, Thickness, Color, Item, Handles = self._Polylines[self._Selected_Polyline_ID]
                    if not self._Point_On_Polyline(Points, X, Y, self.Edge_Tolerance()):
                        return
                    self._Insert_Point_In_Polyline(self._Selected_Polyline_ID, X, Y)
                    return
                if self._Selected_Polygon_ID and not self._Polygon_Disabled.get(self._Selected_Polygon_ID, False):
                    Points, Angle, Thickness, Color, Fill, Item, Handles = self._Polygons[self._Selected_Polygon_ID]
                    if not self._Point_On_Polygon_Edge(Points, X, Y, self.Edge_Tolerance()):
                        return
                    self._Insert_Point_In_Polygon(self._Selected_Polygon_ID, X, Y)
                    return
                return
            self._Drag_Start_Pos = (X, Y)
            Tol = self.Edge_Tolerance()
            if self._Selected_Rect_ID and not self._Rect_Disabled.get(self._Selected_Rect_ID, False):
                Grip, Local, _ = self.Rect_Grip_Hit(self._Selected_Rect_ID, X, Y, Tol)
                if Grip:
                    ID = self._Selected_Rect_ID
                    Cx, Cy, W, H, A, T, OCol, FCol, Item = self._Rectangles[ID]
                    if Grip in ("top_left", "top_right", "bottom_right", "bottom_left"):
                        Rad = -A * math.pi / 180.0
                        CosA = math.cos(Rad)
                        SinA = math.sin(Rad)
                        HW = W / 2.0
                        HH = H / 2.0
                        if Grip == "top_left":
                            OppU, OppV = (HW, HH)
                        elif Grip == "top_right":
                            OppU, OppV = (-HW, HH)
                        elif Grip == "bottom_right":
                            OppU, OppV = (-HW, -HH)
                        else:
                            OppU, OppV = (HW, -HH)
                        Anchor_X = Cx + OppU * CosA - OppV * SinA
                        Anchor_Y = Cy + OppU * SinA + OppV * CosA
                        self._Resize_Info = {"ID": ID, "Type": "rect", "Mode": "corner", "Grip": Grip, "Init": (Cx, Cy, W, H, A), "Anchor": (Anchor_X, Anchor_Y)}
                    else:
                        Edge = Grip
                        if Edge == "right":
                            Opp = (-W / 2.0, 0.0)
                        elif Edge == "left":
                            Opp = (W / 2.0, 0.0)
                        elif Edge == "bottom":
                            Opp = (0.0, -H / 2.0)
                        else:
                            Opp = (0.0, H / 2.0)
                        self._Resize_Info = {"ID": ID, "Type": "rect", "Mode": "edge", "Edge": Edge, "Init": (Cx, Cy, W, H, A), "Opp": Opp}
                    self._Drag_Mode = "rect_resize"
                    return
            if self._Selected_Quad_ID and not self._Quad_Disabled.get(self._Selected_Quad_ID, False):
                Corner_I, _ = self.Quad_Corner_Hit(self._Selected_Quad_ID, X, Y, Tol)
                if Corner_I is not None:
                    ID = self._Selected_Quad_ID
                    P1, P2, P3, P4, A0, T0, OC0, FC0, Item0 = self._Quadrilaterals[ID]
                    self._Resize_Info = {"ID": ID, "Type": "quad_corner", "Corner_Index": int(Corner_I), "Init_Points": [P1, P2, P3, P4], "Init_Angle": A0}
                    self._Drag_Mode = "quad_resize"
                    return
            if self._Selected_Circle_ID and not self._Circle_Disabled.get(self._Selected_Circle_ID, False):
                Cx, Cy, R, T, OCol, FCol, Item = self._Circles[self._Selected_Circle_ID]
                D = math.hypot(X - Cx, Y - Cy)
                Diff = abs(D - R)
                if Diff <= Tol * 1.5:
                    Dist0 = math.hypot(X - Cx, Y - Cy)
                    if Dist0 < 1e-9:
                        Ux, Uy = 1.0, 0.0
                    else:
                        Ux = (X - Cx) / Dist0
                        Uy = (Y - Cy) / Dist0
                    self._Resize_Info = {"ID": self._Selected_Circle_ID, "Type": "circle", "Init_R": R, "Start_Dist": Dist0, "Init_Center": (Cx, Cy), "Dir": (Ux, Uy)}
                    self._Drag_Mode = "circle_resize"
                    return
            if self._Selected_Line_ID and not self._Line_Disabled.get(self._Selected_Line_ID, False):
                End_I, _ = self._Line_Endpoint_Hit(self._Selected_Line_ID, X, Y, Tol)
                if End_I is not None:
                    ID = self._Selected_Line_ID
                    Points, A0, T0, C0, Item0, Handles0 = self._Lines[ID]
                    Center = self._Line_Center(Points)
                    self._Resize_Info = {"ID": ID, "Type": "line_endpoint", "Point_Index": int(End_I), "Init_Points": list(Points), "Center": Center, "Init_Angle": A0}
                    self._Drag_Mode = "line_resize"
                    return
                if self.Point_On_Line(self._Selected_Line_ID, X, Y, Tol):
                    self._Click_Target = ("line", self._Selected_Line_ID)
                    self._Drag_Mode = "line"
                    return
            if self._Selected_Polyline_ID and not self._Polyline_Disabled.get(self._Selected_Polyline_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[self._Selected_Polyline_ID]
                Pi, _ = self._Poly_Point_Hit(Points, X, Y, Tol)
                if Pi is not None:
                    Center = self._Poly_Center(Points)
                    self._Resize_Info = {"ID": self._Selected_Polyline_ID, "Type": "polyline_point", "Point_Index": int(Pi), "Init_Points": list(Points), "Center": Center, "Init_Angle": A0}
                    self._Drag_Mode = "polyline_point"
                    return
                if self._Point_On_Polyline(Points, X, Y, Tol):
                    self._Click_Target = ("polyline", self._Selected_Polyline_ID)
                    self._Drag_Mode = "polyline"
                    return
            if self._Selected_Polygon_ID and not self._Polygon_Disabled.get(self._Selected_Polygon_ID, False):
                Points, A0, T0, OC0, FC0, Item0, Handles0 = self._Polygons[self._Selected_Polygon_ID]
                Pi, _ = self._Poly_Point_Hit(Points, X, Y, Tol)
                if Pi is not None:
                    Center = self._Poly_Center(Points)
                    self._Resize_Info = {"ID": self._Selected_Polygon_ID, "Type": "polygon_point", "Point_Index": int(Pi), "Init_Points": list(Points), "Center": Center, "Init_Angle": A0}
                    self._Drag_Mode = "polygon_point"
                    return
                if self._Point_In_Polygon(Points, X, Y) or self._Point_On_Polygon_Edge(Points, X, Y, Tol):
                    self._Click_Target = ("polygon", self._Selected_Polygon_ID)
                    self._Drag_Mode = "polygon"
                    return
            Best = None
            Best_D = None
            for ID in self._Rectangles:
                if self._Rect_Disabled.get(ID, False):
                    continue
                Grip, Local, Dist = self.Rect_Grip_Hit(ID, X, Y, Tol)
                if Grip:
                    if Best_D is None or Dist < Best_D:
                        Best = ("rect", ID, Grip)
                        Best_D = Dist
            for ID in self._Quadrilaterals:
                if self._Quad_Disabled.get(ID, False):
                    continue
                Corner_I, Dist = self.Quad_Corner_Hit(ID, X, Y, Tol)
                if Corner_I is not None:
                    if Best_D is None or Dist < Best_D:
                        Best = ("quad_corner", ID, int(Corner_I))
                        Best_D = Dist
            for ID, (Cx, Cy, R, T, OCol, FCol, Item) in self._Circles.items():
                if self._Circle_Disabled.get(ID, False):
                    continue
                D = math.hypot(X - Cx, Y - Cy)
                Diff = abs(D - R)
                if Diff <= Tol * 1.5:
                    if Best_D is None or Diff < Best_D:
                        Best = ("circle_resize", ID, None)
                        Best_D = Diff
            for ID, Data in self._Lines.items():
                if self._Line_Disabled.get(ID, False):
                    continue
                End_I, Dist = self._Line_Endpoint_Hit(ID, X, Y, Tol)
                if End_I is not None:
                    if Best_D is None or Dist < Best_D:
                        Best = ("line_endpoint", ID, int(End_I))
                        Best_D = Dist
            for ID, Data in self._Polylines.items():
                if self._Polyline_Disabled.get(ID, False):
                    continue
                Points, A0, T0, C0, Item0, Handles0 = Data
                Pi, Dist = self._Poly_Point_Hit(Points, X, Y, Tol)
                if Pi is not None:
                    if Best_D is None or Dist < Best_D:
                        Best = ("polyline_point", ID, int(Pi))
                        Best_D = Dist
            for ID, Data in self._Polygons.items():
                if self._Polygon_Disabled.get(ID, False):
                    continue
                Points, A0, T0, OC0, FC0, Item0, Handles0 = Data
                Pi, Dist = self._Poly_Point_Hit(Points, X, Y, Tol)
                if Pi is not None:
                    if Best_D is None or Dist < Best_D:
                        Best = ("polygon_point", ID, int(Pi))
                        Best_D = Dist
            if Best:
                Kind, ID, Hit = Best
                if Kind == "rect":
                    self._Selected_Rect_ID = ID
                    self._Selected_Circle_ID = None
                    self._Selected_Quad_ID = None
                    self._Selected_Line_ID = None
                    self._Selected_Polyline_ID = None
                    self._Selected_Polygon_ID = None
                    Cx, Cy, W, H, A, T, OCol, FCol, Item = self._Rectangles[ID]
                    Grip = Hit
                    if Grip in ("top_left", "top_right", "bottom_right", "bottom_left"):
                        Rad = -A * math.pi / 180.0
                        CosA = math.cos(Rad)
                        SinA = math.sin(Rad)
                        HW = W / 2.0
                        HH = H / 2.0
                        if Grip == "top_left":
                            OppU, OppV = (HW, HH)
                        elif Grip == "top_right":
                            OppU, OppV = (-HW, HH)
                        elif Grip == "bottom_right":
                            OppU, OppV = (-HW, -HH)
                        else:
                            OppU, OppV = (HW, -HH)
                        Anchor_X = Cx + OppU * CosA - OppV * SinA
                        Anchor_Y = Cy + OppU * SinA + OppV * CosA
                        self._Resize_Info = {"ID": ID, "Type": "rect", "Mode": "corner", "Grip": Grip, "Init": (Cx, Cy, W, H, A), "Anchor": (Anchor_X, Anchor_Y)}
                    else:
                        Edge = Grip
                        if Edge == "right":
                            Opp = (-W / 2.0, 0.0)
                        elif Edge == "left":
                            Opp = (W / 2.0, 0.0)
                        elif Edge == "bottom":
                            Opp = (0.0, -H / 2.0)
                        else:
                            Opp = (0.0, H / 2.0)
                        self._Resize_Info = {"ID": ID, "Type": "rect", "Mode": "edge", "Edge": Edge, "Init": (Cx, Cy, W, H, A), "Opp": Opp}
                    self._Drag_Mode = "rect_resize"
                    self.Render()
                    return
                if Kind == "quad_corner":
                    self._Selected_Quad_ID = ID
                    self._Selected_Rect_ID = None
                    self._Selected_Circle_ID = None
                    self._Selected_Line_ID = None
                    self._Selected_Polyline_ID = None
                    self._Selected_Polygon_ID = None
                    P1, P2, P3, P4, A0, T0, OC0, FC0, Item0 = self._Quadrilaterals[ID]
                    self._Resize_Info = {"ID": ID, "Type": "quad_corner", "Corner_Index": int(Hit), "Init_Points": [P1, P2, P3, P4], "Init_Angle": A0}
                    self._Drag_Mode = "quad_resize"
                    self.Render()
                    return
                if Kind == "circle_resize":
                    self._Selected_Circle_ID = ID
                    self._Selected_Rect_ID = None
                    self._Selected_Quad_ID = None
                    self._Selected_Line_ID = None
                    self._Selected_Polyline_ID = None
                    self._Selected_Polygon_ID = None
                    Cx, Cy, R, T, OCol, FCol, Item = self._Circles[ID]
                    Dist0 = math.hypot(X - Cx, Y - Cy)
                    if Dist0 < 1e-9:
                        Ux, Uy = 1.0, 0.0
                    else:
                        Ux = (X - Cx) / Dist0
                        Uy = (Y - Cy) / Dist0
                    self._Resize_Info = {"ID": ID, "Type": "circle", "Init_R": R, "Start_Dist": Dist0, "Init_Center": (Cx, Cy), "Dir": (Ux, Uy)}
                    self._Drag_Mode = "circle_resize"
                    self.Render()
                    return
                if Kind == "line_endpoint":
                    self._Selected_Line_ID = ID
                    self._Selected_Rect_ID = None
                    self._Selected_Circle_ID = None
                    self._Selected_Quad_ID = None
                    self._Selected_Polyline_ID = None
                    self._Selected_Polygon_ID = None
                    Points, A0, T0, C0, Item0, Handles0 = self._Lines[ID]
                    Center = self._Line_Center(Points)
                    self._Resize_Info = {"ID": ID, "Type": "line_endpoint", "Point_Index": int(Hit), "Init_Points": list(Points), "Center": Center, "Init_Angle": A0}
                    self._Drag_Mode = "line_resize"
                    self.Render()
                    return
                if Kind == "polyline_point":
                    self._Selected_Polyline_ID = ID
                    self._Selected_Rect_ID = None
                    self._Selected_Circle_ID = None
                    self._Selected_Quad_ID = None
                    self._Selected_Line_ID = None
                    self._Selected_Polygon_ID = None
                    Points, A0, T0, C0, Item0, Handles0 = self._Polylines[ID]
                    Center = self._Poly_Center(Points)
                    self._Resize_Info = {"ID": ID, "Type": "polyline_point", "Point_Index": int(Hit), "Init_Points": list(Points), "Center": Center, "Init_Angle": A0}
                    self._Drag_Mode = "polyline_point"
                    self.Render()
                    return
                if Kind == "polygon_point":
                    self._Selected_Polygon_ID = ID
                    self._Selected_Rect_ID = None
                    self._Selected_Circle_ID = None
                    self._Selected_Quad_ID = None
                    self._Selected_Line_ID = None
                    self._Selected_Polyline_ID = None
                    Points, A0, T0, OC0, FC0, Item0, Handles0 = self._Polygons[ID]
                    Center = self._Poly_Center(Points)
                    self._Resize_Info = {"ID": ID, "Type": "polygon_point", "Point_Index": int(Hit), "Init_Points": list(Points), "Center": Center, "Init_Angle": A0}
                    self._Drag_Mode = "polygon_point"
                    self.Render()
                    return
            Mode, ID = self.Pick_Shape(X, Y)
            if Mode == "rect" and not self._Rect_Disabled.get(ID, False):
                self._Selected_Rect_ID = ID
                self._Selected_Circle_ID = None
                self._Selected_Quad_ID = None
                self._Selected_Line_ID = None
                self._Selected_Polyline_ID = None
                self._Selected_Polygon_ID = None
                self._Click_Target = ("rect", ID)
                self._Drag_Mode = "rect"
                self.Render()
                return
            if Mode == "circle" and not self._Circle_Disabled.get(ID, False):
                self._Selected_Circle_ID = ID
                self._Selected_Rect_ID = None
                self._Selected_Quad_ID = None
                self._Selected_Line_ID = None
                self._Selected_Polyline_ID = None
                self._Selected_Polygon_ID = None
                self._Click_Target = ("circle", ID)
                self._Drag_Mode = "circle"
                self.Render()
                return
            if Mode == "quad" and not self._Quad_Disabled.get(ID, False):
                self._Selected_Quad_ID = ID
                self._Selected_Rect_ID = None
                self._Selected_Circle_ID = None
                self._Selected_Line_ID = None
                self._Selected_Polyline_ID = None
                self._Selected_Polygon_ID = None
                self._Click_Target = ("quad", ID)
                self._Drag_Mode = "quad"
                self.Render()
                return
            if Mode == "line" and not self._Line_Disabled.get(ID, False):
                self._Selected_Line_ID = ID
                self._Selected_Rect_ID = None
                self._Selected_Circle_ID = None
                self._Selected_Quad_ID = None
                self._Selected_Polyline_ID = None
                self._Selected_Polygon_ID = None
                self._Click_Target = ("line", ID)
                self._Drag_Mode = "line"
                self.Render()
                return
            if Mode == "polyline" and not self._Polyline_Disabled.get(ID, False):
                self._Selected_Polyline_ID = ID
                self._Selected_Rect_ID = None
                self._Selected_Circle_ID = None
                self._Selected_Quad_ID = None
                self._Selected_Line_ID = None
                self._Selected_Polygon_ID = None
                self._Click_Target = ("polyline", ID)
                self._Drag_Mode = "polyline"
                self.Render()
                return
            if Mode == "polygon" and not self._Polygon_Disabled.get(ID, False):
                self._Selected_Polygon_ID = ID
                self._Selected_Rect_ID = None
                self._Selected_Circle_ID = None
                self._Selected_Quad_ID = None
                self._Selected_Line_ID = None
                self._Selected_Polyline_ID = None
                self._Click_Target = ("polygon", ID)
                self._Drag_Mode = "polygon"
                self.Render()
                return
            if self._Selected_Rect_ID and not self._Rect_Disabled.get(self._Selected_Rect_ID, False) and not self._Rect_Disable_Rotation.get(self._Selected_Rect_ID, False):
                Cx, Cy, W, H, A, T, OCol, FCol, Item = self._Rectangles[self._Selected_Rect_ID]
                self._Resize_Info = {"ID": self._Selected_Rect_ID, "Type": "rect_rotate", "Init_Angle": A, "Start_Vector": (X - Cx, Y - Cy)}
                self._Drag_Mode = "rect_rotate"
                self._Click_Target = ("empty", None)
                return
            if self._Selected_Quad_ID and not self._Quad_Disabled.get(self._Selected_Quad_ID, False):
                P1, P2, P3, P4, A0, T0, OC0, FC0, Item0 = self._Quadrilaterals[self._Selected_Quad_ID]
                Points0 = [P1, P2, P3, P4]
                Center = self.Quad_Center(Points0)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Quad_ID, "Type": "quad_rotate", "Init_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": Points0, "Center": Center}
                self._Drag_Mode = "quad_rotate"
                self._Click_Target = ("empty", None)
                return
            if self._Selected_Line_ID and not self._Line_Disabled.get(self._Selected_Line_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Lines[self._Selected_Line_ID]
                Center = self._Line_Center(Points)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Line_ID, "Type": "line_rotate", "Init_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": list(Points), "Center": Center}
                self._Drag_Mode = "line_rotate"
                self._Click_Target = ("empty", None)
                return
            if self._Selected_Polyline_ID and not self._Polyline_Disabled.get(self._Selected_Polyline_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[self._Selected_Polyline_ID]
                Center = self._Poly_Center(Points)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Polyline_ID, "Type": "polyline_rotate", "Init_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": list(Points), "Center": Center}
                self._Drag_Mode = "polyline_rotate"
                self._Click_Target = ("empty", None)
                return
            if self._Selected_Polygon_ID and not self._Polygon_Disabled.get(self._Selected_Polygon_ID, False):
                Points, A0, T0, OC0, FC0, Item0, Handles0 = self._Polygons[self._Selected_Polygon_ID]
                Center = self._Poly_Center(Points)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Polygon_ID, "Type": "polygon_rotate", "Init_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": list(Points), "Center": Center}
                self._Drag_Mode = "polygon_rotate"
                self._Click_Target = ("empty", None)
                return
            self._Click_Target = ("empty", None)
            self._Drag_Mode = "none"
            return
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag_Start -> {E}")

    def Drag(self, Event):
        try:
            CX = self._Canvas._Frame.canvasx(Event.x)
            CY = self._Canvas._Frame.canvasy(Event.y)
            DX = CX - self._Drag_Last_X
            DY = CY - self._Drag_Last_Y
            self._Drag_Last_X = CX
            self._Drag_Last_Y = CY
            if self._Drag_Mode == "rect" and self._Selected_Rect_ID and not self._Rect_Disabled.get(self._Selected_Rect_ID, False):
                Cx, Cy, W, H, A, T, OCol, FCol, Item = self._Rectangles[self._Selected_Rect_ID]
                Cx += DX
                Cy += DY
                self._Rectangles[self._Selected_Rect_ID] = (Cx, Cy, W, H, A, T, OCol, FCol, Item)
                self.Rect_Draw(self._Selected_Rect_ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Rectangle", ID=self._Selected_Rect_ID, Event="Update")
                return
            if self._Drag_Mode == "rect_resize" and self._Resize_Info and not self._Rect_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Cx_Init, Cy_Init, W_Init, H_Init, A_Init = self._Resize_Info["Init"]
                Mode = self._Resize_Info["Mode"]
                if Mode == "corner":
                    Anchor_X, Anchor_Y = self._Resize_Info["Anchor"]
                    Dx = CX - Anchor_X
                    Dy = CY - Anchor_Y
                    Rad = -A_Init * math.pi / 180.0
                    CosA = math.cos(Rad)
                    SinA = math.sin(Rad)
                    U = Dx * CosA + Dy * SinA
                    V = -Dx * SinA + Dy * CosA
                    New_W = abs(U)
                    New_H = abs(V)
                    New_W = max(2.0, New_W)
                    New_H = max(2.0, New_H)
                    Sign_U = 1.0 if U >= 0 else -1.0
                    Sign_V = 1.0 if V >= 0 else -1.0
                    New_Cx = Anchor_X + (New_W / 2.0 * Sign_U) * CosA - (New_H / 2.0 * Sign_V) * SinA
                    New_Cy = Anchor_Y + (New_W / 2.0 * Sign_U) * SinA + (New_H / 2.0 * Sign_V) * CosA
                    _, _, _, _, _, T_Curr, OCol_Curr, FCol_Curr, Item_Curr = self._Rectangles[ID]
                    self._Rectangles[ID] = (New_Cx, New_Cy, New_W, New_H, A_Init, T_Curr, OCol_Curr, FCol_Curr, Item_Curr)
                    self.Rect_Draw(ID)
                elif Mode == "edge":
                    Edge = self._Resize_Info["Edge"]
                    Opp = self._Resize_Info["Opp"]
                    Dx = CX - Cx_Init
                    Dy = CY - Cy_Init
                    Rad = -A_Init * math.pi / 180.0
                    CosA = math.cos(Rad)
                    SinA = math.sin(Rad)
                    U = Dx * CosA + Dy * SinA
                    V = -Dx * SinA + Dy * CosA
                    if Edge == "right":
                        New_W = abs(U - Opp[0])
                        New_H = H_Init
                        Mid_U = (U + Opp[0]) / 2.0
                        Mid_V = 0.0
                    elif Edge == "left":
                        New_W = abs(U - Opp[0])
                        New_H = H_Init
                        Mid_U = (U + Opp[0]) / 2.0
                        Mid_V = 0.0
                    elif Edge == "bottom":
                        New_W = W_Init
                        New_H = abs(V - Opp[1])
                        Mid_U = 0.0
                        Mid_V = (V + Opp[1]) / 2.0
                    else:
                        New_W = W_Init
                        New_H = abs(V - Opp[1])
                        Mid_U = 0.0
                        Mid_V = (V + Opp[1]) / 2.0
                    New_W = max(2.0, New_W)
                    New_H = max(2.0, New_H)
                    New_Cx = Cx_Init + Mid_U * CosA - Mid_V * SinA
                    New_Cy = Cy_Init + Mid_U * SinA + Mid_V * CosA
                    _, _, _, _, _, T_Curr, OCol_Curr, FCol_Curr, Item_Curr = self._Rectangles[ID]
                    self._Rectangles[ID] = (New_Cx, New_Cy, New_W, New_H, A_Init, T_Curr, OCol_Curr, FCol_Curr, Item_Curr)
                    self.Rect_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Rectangle", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "rect_rotate" and self._Resize_Info and not self._Rect_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Cx, Cy, W, H, _, T, OCol, FCol, Item = self._Rectangles[ID]
                A_Init = self._Resize_Info["Init_Angle"]
                Start_Vec = self._Resize_Info["Start_Vector"]
                Start_Vx, Start_Vy = Start_Vec
                Current_Vx = CX - Cx
                Current_Vy = CY - Cy
                Start_Angle = math.atan2(Start_Vy, Start_Vx) * 180.0 / math.pi
                Current_Angle = math.atan2(Current_Vy, Current_Vx) * 180.0 / math.pi
                Delta = Current_Angle - Start_Angle
                New_Angle = self.Normalize_Angle(A_Init - Delta)
                self._Rectangles[ID] = (Cx, Cy, W, H, New_Angle, T, OCol, FCol, Item)
                self.Rect_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Rectangle", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "circle" and self._Selected_Circle_ID and not self._Circle_Disabled.get(self._Selected_Circle_ID, False):
                Cx, Cy, R, T, OCol, FCol, Item = self._Circles[self._Selected_Circle_ID]
                Cx += DX
                Cy += DY
                self._Circles[self._Selected_Circle_ID] = (Cx, Cy, R, T, OCol, FCol, Item)
                self.Circle_Draw(self._Selected_Circle_ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Circle", ID=self._Selected_Circle_ID, Event="Update")
                return
            if self._Drag_Mode == "circle_resize" and self._Resize_Info and not self._Circle_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Init_Center = self._Resize_Info["Init_Center"]
                Cx, Cy = Init_Center
                Dist_Current = math.hypot(CX - Cx, CY - Cy)
                New_R = max(1.0, Dist_Current)
                _, _, _, T_Curr, OCol_Curr, FCol_Curr, Item_Curr = self._Circles[ID]
                self._Circles[ID] = (Cx, Cy, New_R, T_Curr, OCol_Curr, FCol_Curr, Item_Curr)
                self.Circle_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Circle", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "quad" and self._Selected_Quad_ID and not self._Quad_Disabled.get(self._Selected_Quad_ID, False):
                P1, P2, P3, P4, A, T, OCol, FCol, Item = self._Quadrilaterals[self._Selected_Quad_ID]
                P1 = [P1[0] + DX, P1[1] + DY]
                P2 = [P2[0] + DX, P2[1] + DY]
                P3 = [P3[0] + DX, P3[1] + DY]
                P4 = [P4[0] + DX, P4[1] + DY]
                self._Quadrilaterals[self._Selected_Quad_ID] = (P1, P2, P3, P4, A, T, OCol, FCol, Item)
                self.Quad_Draw(self._Selected_Quad_ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Quadrilateral", ID=self._Selected_Quad_ID, Event="Update")
                return
            if self._Drag_Mode == "quad_resize" and self._Resize_Info and not self._Quad_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Corner_Index = self._Resize_Info["Corner_Index"]
                Init_Points = self._Resize_Info["Init_Points"]
                New_Points = list(Init_Points)
                New_Points[Corner_Index] = [CX, CY]
                _, _, _, _, A0, T0, OC0, FC0, Item0 = self._Quadrilaterals[ID]
                self._Quadrilaterals[ID] = (New_Points[0], New_Points[1], New_Points[2], New_Points[3], A0, T0, OC0, FC0, Item0)
                self.Quad_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Quadrilateral", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "quad_rotate" and self._Resize_Info and not self._Quad_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Init_Points = self._Resize_Info["Init_Points"]
                Center = self._Resize_Info["Center"]
                A_Init = self._Resize_Info["Init_Angle"]
                Cx, Cy = Center
                Start_Vec = self._Resize_Info["Start_Vector"]
                Start_Vx, Start_Vy = Start_Vec
                Current_Vx = CX - Cx
                Current_Vy = CY - Cy
                Start_Angle = math.atan2(Start_Vy, Start_Vx) * 180.0 / math.pi
                Current_Angle = math.atan2(Current_Vy, Current_Vx) * 180.0 / math.pi
                Delta = Current_Angle - Start_Angle
                New_Points = self._Rotate_Points(Init_Points, Center, -Delta)
                _, _, _, _, _, T0, OC0, FC0, Item0 = self._Quadrilaterals[ID]
                New_Angle = self.Normalize_Angle(A_Init - Delta)
                self._Quadrilaterals[ID] = (New_Points[0], New_Points[1], New_Points[2], New_Points[3], New_Angle, T0, OC0, FC0, Item0)
                self.Quad_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Quadrilateral", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "line" and self._Selected_Line_ID and not self._Line_Disabled.get(self._Selected_Line_ID, False):
                Points, A, T, C, Item, Handles = self._Lines[self._Selected_Line_ID]
                New_Points = [(Points[0][0] + DX, Points[0][1] + DY), (Points[1][0] + DX, Points[1][1] + DY)]
                self._Lines[self._Selected_Line_ID] = (New_Points, A, T, C, Item, Handles)
                self.Line_Draw(self._Selected_Line_ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Line", ID=self._Selected_Line_ID, Event="Update")
                return
            if self._Drag_Mode == "line_resize" and self._Resize_Info and not self._Line_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Point_Index = self._Resize_Info["Point_Index"]
                Init_Points = self._Resize_Info["Init_Points"]
                New_Points = list(Init_Points)
                New_Points[Point_Index] = (CX, CY)
                _, A0, T0, C0, Item0, Handles0 = self._Lines[ID]
                self._Lines[ID] = (New_Points, A0, T0, C0, Item0, Handles0)
                self.Line_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Line", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "line_rotate" and self._Resize_Info and not self._Line_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Init_Points = self._Resize_Info["Init_Points"]
                Center = self._Resize_Info["Center"]
                A_Init = self._Resize_Info["Init_Angle"]
                Cx, Cy = Center
                Start_Vec = self._Resize_Info["Start_Vector"]
                Start_Vx, Start_Vy = Start_Vec
                Current_Vx = CX - Cx
                Current_Vy = CY - Cy
                Start_Angle = math.atan2(Start_Vy, Start_Vx) * 180.0 / math.pi
                Current_Angle = math.atan2(Current_Vy, Current_Vx) * 180.0 / math.pi
                Delta = Current_Angle - Start_Angle
                New_Points = self._Rotate_Points(Init_Points, Center, -Delta)
                _, _, T0, C0, Item0, Handles0 = self._Lines[ID]
                New_Angle = self.Normalize_Angle(A_Init - Delta)
                self._Lines[ID] = (New_Points, New_Angle, T0, C0, Item0, Handles0)
                self.Line_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Line", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "polyline" and self._Selected_Polyline_ID and not self._Polyline_Disabled.get(self._Selected_Polyline_ID, False):
                Points, A, T, C, Item, Handles = self._Polylines[self._Selected_Polyline_ID]
                New_Points = [(X + DX, Y + DY) for (X, Y) in Points]
                self._Polylines[self._Selected_Polyline_ID] = (New_Points, A, T, C, Item, Handles)
                self.Polyline_Draw(self._Selected_Polyline_ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Polyline", ID=self._Selected_Polyline_ID, Event="Update")
                return
            if self._Drag_Mode == "polyline_point" and self._Resize_Info and not self._Polyline_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Point_Index = self._Resize_Info["Point_Index"]
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[ID]
                New_Points = list(Points)
                New_Points[Point_Index] = (CX, CY)
                self._Polylines[ID] = (New_Points, A0, T0, C0, Item0, Handles0)
                self.Polyline_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Polyline", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "polyline_rotate" and self._Resize_Info and not self._Polyline_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Init_Points = self._Resize_Info["Init_Points"]
                Center = self._Resize_Info["Center"]
                A_Init = self._Resize_Info["Init_Angle"]
                Cx, Cy = Center
                Start_Vec = self._Resize_Info["Start_Vector"]
                Start_Vx, Start_Vy = Start_Vec
                Current_Vx = CX - Cx
                Current_Vy = CY - Cy
                Start_Angle = math.atan2(Start_Vy, Start_Vx) * 180.0 / math.pi
                Current_Angle = math.atan2(Current_Vy, Current_Vx) * 180.0 / math.pi
                Delta = Current_Angle - Start_Angle
                New_Points = self._Rotate_Points(Init_Points, Center, -Delta)
                _, _, T0, C0, Item0, Handles0 = self._Polylines[ID]
                New_Angle = self.Normalize_Angle(A_Init - Delta)
                self._Polylines[ID] = (New_Points, New_Angle, T0, C0, Item0, Handles0)
                self.Polyline_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Polyline", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "polygon" and self._Selected_Polygon_ID and not self._Polygon_Disabled.get(self._Selected_Polygon_ID, False):
                Points, A, T, OC, FC, Item, Handles = self._Polygons[self._Selected_Polygon_ID]
                New_Points = [(X + DX, Y + DY) for (X, Y) in Points]
                self._Polygons[self._Selected_Polygon_ID] = (New_Points, A, T, OC, FC, Item, Handles)
                self.Polygon_Draw(self._Selected_Polygon_ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Polygon", ID=self._Selected_Polygon_ID, Event="Update")
                return
            if self._Drag_Mode == "polygon_point" and self._Resize_Info and not self._Polygon_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Point_Index = self._Resize_Info["Point_Index"]
                Points, A0, T0, OC0, FC0, Item0, Handles0 = self._Polygons[ID]
                New_Points = list(Points)
                New_Points[Point_Index] = (CX, CY)
                self._Polygons[ID] = (New_Points, A0, T0, OC0, FC0, Item0, Handles0)
                self.Polygon_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Polygon", ID=ID, Event="Update")
                return
            if self._Drag_Mode == "polygon_rotate" and self._Resize_Info and not self._Polygon_Disabled.get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Init_Points = self._Resize_Info["Init_Points"]
                Center = self._Resize_Info["Center"]
                A_Init = self._Resize_Info["Init_Angle"]
                Cx, Cy = Center
                Start_Vec = self._Resize_Info["Start_Vector"]
                Start_Vx, Start_Vy = Start_Vec
                Current_Vx = CX - Cx
                Current_Vy = CY - Cy
                Start_Angle = math.atan2(Start_Vy, Start_Vx) * 180.0 / math.pi
                Current_Angle = math.atan2(Current_Vy, Current_Vx) * 180.0 / math.pi
                Delta = Current_Angle - Start_Angle
                New_Points = self._Rotate_Points(Init_Points, Center, -Delta)
                _, _, T0, OC0, FC0, Item0, Handles0 = self._Polygons[ID]
                New_Angle = self.Normalize_Angle(A_Init - Delta)
                self._Polygons[ID] = (New_Points, New_Angle, T0, OC0, FC0, Item0, Handles0)
                self.Polygon_Draw(ID)
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Polygon", ID=ID, Event="Update")
                return
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag -> {E}")
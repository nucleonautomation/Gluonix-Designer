from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
import math
import time
from .N_GUI import GUI

PIL_Image.MAX_IMAGE_PIXELS = None

class Editor:

    def __init__(self, Canvas, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Editor"
            try:
                self._Type = Editor
                self._Canvas = Canvas
                self._Display = True
                self._Frame = False
                self._Image = False
                self._Image_Window = False
                self._Zoom_Scale = 1.0
                self._Zoom_Center = None
                self._Drag_Last_X = 0
                self._Drag_Last_Y = 0
                self._Drag_Mode = "image"
                self._Render_Info = None
                self._Rectangles = {}
                self._Circles = {}
                self._Quadrilaterals = {}
                self._Lines = {}
                self._Polylines = {}
                self._Polygons = {}
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
                self._Circle_Center_Handles = {}
                self._Canvas._Item.append(self)
                self.Callback = None
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
            if self._Image:
                self._Image.close()
            if self._Image_Window:
                self._Canvas.Delete_Item(self._Image_Window)
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
            self._Canvas.Bind(On_Click=self.Drag_Start, On_Drag=self.Drag, On_Release=self.Release, On_Mouse_Wheel=self.Zoom, On_Right_Click=self.Reset, On_Resize=self.Resize, On_Motion=self.On_Motion)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")

    def Inner_Padding(self):
        try:
            return max(0, getattr(self._Canvas, "_Border_Size", 0)) + max(0, getattr(self._Canvas, "_Shadow_Size", 0)) + max(0, getattr(self._Canvas, "_Radius", 0))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Inner_Padding -> {E}")

    def Normalize_Angle(self, A):
        try:
            return A % 360.0
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Normalize_Angle -> {E}")

    def Edge_Tolerance(self):
        try:
            S = self._Render_Info["Scale"] if self._Render_Info else 1.0
            return 14.0 / max(1e-9, S)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Edge_Tolerance -> {E}")


    def _Callback_Invoke(self, Type, ID=None, Event="Update"):
        try:
            CB = getattr(self, "Callback", None)
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
            if not self._Render_Info:
                return Handles
            R = self._Point_Handle_Radius()
            for X, Y in Points:
                P = self.Image_To_Canvas(X, Y)
                if not P:
                    continue
                Xc, Yc = P
                Item = self._Canvas._Frame.create_oval(Xc - R, Yc - R, Xc + R, Yc + R, outline=Color, fill=Color, width=1)
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

    def _Poly_Area(self, Points):
        try:
            if not Points or len(Points) < 3:
                return 0.0
            A = 0.0
            N = len(Points)
            for I in range(N):
                X1, Y1 = Points[I]
                X2, Y2 = Points[(I + 1) % N]
                A += X1 * Y2 - X2 * Y1
            return abs(A) * 0.5
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Poly_Area -> {E}")
            return 0.0

    def _Polyline_Length(self, Points):
        try:
            if not Points or len(Points) < 2:
                return 0.0
            L = 0.0
            for I in range(len(Points) - 1):
                X1, Y1 = Points[I]
                X2, Y2 = Points[I + 1]
                L += math.hypot(X2 - X1, Y2 - Y1)
            return L
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Polyline_Length -> {E}")
            return 0.0

    def Load(self, Frame=None):
        try:
            Old_Image_Width = float(getattr(self, "_Image_Width", 0) or 0)
            Old_Image_Height = float(getattr(self, "_Image_Height", 0) or 0)
            Old_Zoom_Center = getattr(self, "_Zoom_Center", None)
            Old_Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            Source_Obj = Frame
            if Source_Obj is None and getattr(self, "_Frame", False) is not False:
                Source_Obj = self._Frame
            Image_Obj = None
            if hasattr(Source_Obj, "__class__") and getattr(type(Source_Obj), "__module__", "").startswith("numpy"):
                self._Frame = Source_Obj
                if self._Image:
                    try:
                        self._Image.close()
                    except:
                        pass
                Image_Obj = PIL_Image.fromarray(Source_Obj)
            elif isinstance(Source_Obj, PIL_Image.Image):
                self._Frame = False
                if self._Image:
                    try:
                        self._Image.close()
                    except:
                        pass
                Pil_Obj = Source_Obj
                try:
                    if getattr(Pil_Obj, "is_animated", False):
                        Pil_Obj.seek(0)
                except:
                    pass
                Image_Obj = Pil_Obj.copy()
            else:
                try:
                    Pil_From_Tk = PIL_ImageTk.getimage(Source_Obj)
                    if isinstance(Pil_From_Tk, PIL_Image.Image):
                        self._Frame = False
                        if self._Image:
                            try:
                                self._Image.close()
                            except:
                                pass
                        Image_Obj = Pil_From_Tk.copy()
                except:
                    Image_Obj = None
            if Image_Obj is None:
                from io import BytesIO as _BytesIO
                import os as _Os
                import urllib.parse as _Url_Parse
                import urllib.request as _Url_Request
                Data = None
                if isinstance(Source_Obj, (bytes, bytearray, memoryview)):
                    Data = bytes(Source_Obj)
                elif isinstance(Source_Obj, str):
                    Parsed_Obj = _Url_Parse.urlparse(Source_Obj)
                    if Parsed_Obj.scheme in ("http", "https"):
                        with _Url_Request.urlopen(Source_Obj) as Response:
                            Data = Response.read()
                    elif _Os.path.exists(Source_Obj):
                        with open(Source_Obj, "rb") as File_Handle:
                            Data = File_Handle.read()
                    else:
                        return
                else:
                    return
                with PIL_Image.open(_BytesIO(Data)) as Pil_Obj:
                    try:
                        if getattr(Pil_Obj, "is_animated", False):
                            Pil_Obj.seek(0)
                    except:
                        pass
                    Image_Obj = Pil_Obj.copy()
                self._Frame = False
                if self._Image:
                    try:
                        self._Image.close()
                    except:
                        pass
            if not Image_Obj:
                return
            self._Image = Image_Obj
            self._Image_Width, self._Image_Height = self._Image.size
            New_Image_Width = float(self._Image_Width or 0)
            New_Image_Height = float(self._Image_Height or 0)
            if not hasattr(self, "_Zoom_Scale") or self._Zoom_Scale is None:
                self._Zoom_Scale = 1.0
            self._Zoom_Scale = float(self._Zoom_Scale or 1.0)
            Max_Zoom_Scale = max(1.0, min(New_Image_Width, New_Image_Height))
            self._Zoom_Scale = max(1.0, min(float(self._Zoom_Scale), float(Max_Zoom_Scale)))
            if Old_Zoom_Center is not None and Old_Image_Width > 0 and Old_Image_Height > 0 and New_Image_Width > 0 and New_Image_Height > 0:
                Old_Center_X, Old_Center_Y = Old_Zoom_Center
                Center_Ratio_X = float(Old_Center_X) / float(Old_Image_Width)
                Center_Ratio_Y = float(Old_Center_Y) / float(Old_Image_Height)
                New_Center_X = Center_Ratio_X * float(New_Image_Width)
                New_Center_Y = Center_Ratio_Y * float(New_Image_Height)
                self._Zoom_Center = (New_Center_X, New_Center_Y)
            else:
                if self._Zoom_Center is None:
                    self._Zoom_Center = (self._Image_Width // 2, self._Image_Height // 2)
            Center_X, Center_Y = self._Zoom_Center
            Center_X = max(0.0, min(float(Center_X), float(self._Image_Width)))
            Center_Y = max(0.0, min(float(Center_Y), float(self._Image_Height)))
            self._Zoom_Center = (Center_X, Center_Y)
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Load -> {E}")

    def Convert(self, Frame_Width, Frame_Height):
        try:
            if not self._Image:
                return None
            Padding = self.Inner_Padding()
            Inner_W = max(1, int(Frame_Width - 2 * Padding))
            Inner_H = max(1, int(Frame_Height - 2 * Padding))
            Zoom_W = self._Image_Width / max(1e-9, self._Zoom_Scale)
            Zoom_H = self._Image_Height / max(1e-9, self._Zoom_Scale)
            if Inner_W < 1 or Inner_H < 1 or Zoom_W < 1 or Zoom_H < 1:
                return False
            Cx, Cy = self._Zoom_Center
            Cx = max(Zoom_W / 2, min(self._Image_Width - Zoom_W / 2, Cx))
            Cy = max(Zoom_H / 2, min(self._Image_Height - Zoom_H / 2, Cy))
            self._Zoom_Center = (Cx, Cy)
            Left = Cx - Zoom_W / 2
            Top = Cy - Zoom_H / 2
            Right = Left + Zoom_W
            Bottom = Top + Zoom_H
            View_Aspect = Zoom_W / Zoom_H
            Frame_Aspect = Inner_W / Inner_H
            if self._Zoom_Scale > 1.0:
                if View_Aspect > Frame_Aspect:
                    New_W = Zoom_H * Frame_Aspect
                    Mid = Left + Zoom_W / 2
                    Left = Mid - New_W / 2
                    Right = Mid + New_W / 2
                elif View_Aspect < Frame_Aspect:
                    New_H = Zoom_W / Frame_Aspect
                    Mid = Top + Zoom_H / 2
                    Top = Mid - New_H / 2
                    Bottom = Mid + New_H / 2
            Crop = self._Image.crop((int(Left), int(Top), int(Right), int(Bottom))).convert("RGBA")
            if self._Zoom_Scale > 1.0:
                New_Width = Inner_W
                New_Height = Inner_H
            else:
                Image_Width, Image_Height = Crop.size
                if Image_Width < 1 or Image_Height < 1:
                    return False
                Image_Aspect = Image_Width / Image_Height
                if Image_Aspect > Frame_Aspect:
                    New_Width = int(Inner_W)
                    New_Height = int(Inner_W / Image_Aspect)
                else:
                    New_Height = int(Inner_H)
                    New_Width = int(Inner_H * Image_Aspect)
            if int(New_Width) < 1 or int(New_Height) < 1:
                return False
            Crop = Crop.resize((int(New_Width), int(New_Height)), PIL_Image.NEAREST)
            Canvas_Left = Padding + (Inner_W - New_Width) // 2
            Canvas_Top = Padding + (Inner_H - New_Height) // 2
            Scale = New_Width / (Right - Left)
            Image_Tk = PIL_ImageTk.PhotoImage(Crop)
            return {"Image": Image_Tk, "Top": int(Canvas_Top), "Left": int(Canvas_Left), "Crop_Left": Left, "Crop_Top": Top, "Crop_Right": Right, "Crop_Bottom": Bottom, "Scale": Scale, "Pad": Padding, "Inner_W": Inner_W, "Inner_H": Inner_H, "Canvas_W": New_Width, "Canvas_H": New_Height}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Convert -> {E}")

    def Image_To_Canvas(self, X, Y):
        try:
            if not self._Render_Info:
                return None
            L = self._Render_Info["Left"]
            T = self._Render_Info["Top"]
            S = self._Render_Info["Scale"]
            CL = self._Render_Info["Crop_Left"]
            CT = self._Render_Info["Crop_Top"]
            return (L + (X - CL) * S, T + (Y - CT) * S)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Image_To_Canvas -> {E}")

    def Canvas_To_Image(self, X, Y):
        try:
            if not self._Render_Info:
                return None
            L = self._Render_Info["Left"]
            T = self._Render_Info["Top"]
            S = self._Render_Info["Scale"]
            CL = self._Render_Info["Crop_Left"]
            CT = self._Render_Info["Crop_Top"]
            W = self._Render_Info["Canvas_W"]
            H = self._Render_Info["Canvas_H"]
            if X < L or Y < T or X > L + W or Y > T + H:
                return None
            return (CL + (X - L) / S, CT + (Y - T) / S)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Canvas_To_Image -> {E}")

    def Rect_Corners_Image(self, Rect):
        try:
            Cx, Cy, Width, Height, Angle, Thickness, Color, Item = Rect
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
            self._GUI.Error(f"{self._Type} -> Rect_Corners_Image -> {E}")

    def Point_In_Rect(self, ID, X, Y):
        try:
            if ID not in self._Rectangles:
                return False
            Cx, Cy, Width, Height, Angle, Thickness, Color, Item = self._Rectangles[ID]
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

    def Point_In_Circle(self, ID, X, Y):
        try:
            if ID not in self._Circles:
                return False
            Cx, Cy, Radius, Thickness, Color, Item = self._Circles[ID]
            Dx = X - Cx
            Dy = Y - Cy
            return Dx * Dx + Dy * Dy <= Radius * Radius
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Point_In_Circle -> {E}")

    def Rect_Edge_Hit(self, ID, X, Y, Tol_Image):
        try:
            Cx, Cy, Width, Height, Angle, Thickness, Color, Item = self._Rectangles[ID]
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
            if m > Tol_Image * 1.5:
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

    def Rect_Grip_Hit(self, ID, X, Y, Tol_Image):
        try:
            if ID not in self._Rectangles:
                return None, None, None
            Cx, Cy, Width, Height, Angle, Thickness, Color, Item = self._Rectangles[ID]
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
            if Best_Corner_D is not None and Best_Corner_D <= Tol_Image * 1.15:
                return Best_Corner, (U, V), Best_Corner_D
            Edge, Local, Dist = self.Rect_Edge_Hit(ID, X, Y, Tol_Image)
            if Edge:
                return Edge, (U, V), Dist
            return None, (U, V), None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rect_Grip_Hit -> {E}")
            return None, None, None


    def Rect_Draw(self, ID):
        try:
            if ID not in self._Rectangles or not self._Render_Info:
                return
            Rect = self._Rectangles[ID]
            Corners = self.Rect_Corners_Image(Rect)
            Screen = []
            for X, Y in Corners:
                P = self.Image_To_Canvas(X, Y)
                if not P:
                    return
                Screen.append(P[0])
                Screen.append(P[1])
            Cx, Cy, Width, Height, Angle, Thickness, Color, Item = Rect
            Width_Draw = Thickness * (2 if self._Selected_Rect_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_polygon(*Screen, outline=Color, fill="", width=Width_Draw)
                self._Rectangles[ID] = (Cx, Cy, Width, Height, Angle, Thickness, Color, Item)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(Item, outline=Color, width=Width_Draw, state="normal")
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

    def Circle_Draw(self, ID):
        try:
            if ID not in self._Circles or not self._Render_Info:
                return
            Cx, Cy, Radius, Thickness, Color, Item = self._Circles[ID]
            P1 = self.Image_To_Canvas(Cx - Radius, Cy - Radius)
            P2 = self.Image_To_Canvas(Cx + Radius, Cy + Radius)
            if not P1 or not P2:
                return
            Width_Draw = Thickness * (2 if self._Selected_Circle_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_oval(P1[0], P1[1], P2[0], P2[1], outline=Color, width=Width_Draw)
                self._Circles[ID] = (Cx, Cy, Radius, Thickness, Color, Item)
            else:
                self._Canvas._Frame.coords(Item, P1[0], P1[1], P2[0], P2[1])
                self._Canvas._Frame.itemconfigure(Item, outline=Color, width=Width_Draw, state="normal")
            self._Canvas._Frame.tag_raise(Item)
            if not hasattr(self, "_Circle_Center_Handles"):
                self._Circle_Center_Handles = {}
            Handles = self._Circle_Center_Handles.get(ID, [])
            if self._Selected_Circle_ID == ID:
                Handles = self._Draw_Point_Handles([(Cx, Cy)], Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Circle_Center_Handles[ID] = Handles
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Circle_Draw -> {E}")
    def Quad_Center(self, Points):
        Cx = 0.0
        Cy = 0.0
        for X, Y in Points:
            Cx += X
            Cy += Y
        return (Cx / 4.0, Cy / 4.0)

    def Quad_Area(self, Points):
        A = 0.0
        for I in range(4):
            X1, Y1 = Points[I]
            X2, Y2 = Points[(I + 1) % 4]
            A += X1 * Y2 - X2 * Y1
        return abs(A) * 0.5

    def Point_In_Quad(self, ID, X, Y):
        try:
            if ID not in self._Quadrilaterals:
                return False
            P1, P2, P3, P4, Angle, Thickness, Color, Item = self._Quadrilaterals[ID]
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

    def Quad_Corner_Hit(self, ID, X, Y, Tol_Image):
        try:
            if ID not in self._Quadrilaterals:
                return None, None
            P1, P2, P3, P4, Angle, Thickness, Color, Item = self._Quadrilaterals[ID]
            Points = [P1, P2, P3, P4]
            Best_I = None
            Best_D = None
            for I, (Px, Py) in enumerate(Points):
                D = math.hypot(X - Px, Y - Py)
                if Best_D is None or D < Best_D:
                    Best_D = D
                    Best_I = I
            if Best_D is not None and Best_D <= Tol_Image * 1.15:
                return Best_I, Best_D
            return None, None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Quad_Corner_Hit -> {E}")
            return None, None

    def Quad_Rotate_Points(self, Points, Center, Delta_A_CW):
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


    def Quad_Draw(self, ID):
        try:
            if ID not in self._Quadrilaterals or not self._Render_Info:
                return
            P1, P2, P3, P4, Angle, Thickness, Color, Item = self._Quadrilaterals[ID]
            Points = [P1, P2, P3, P4]
            Screen = []
            for X, Y in Points:
                P = self.Image_To_Canvas(X, Y)
                if not P:
                    return
                Screen.append(P[0])
                Screen.append(P[1])
            Width_Draw = Thickness * (2 if self._Selected_Quad_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_polygon(*Screen, outline=Color, fill="", width=Width_Draw)
                self._Quadrilaterals[ID] = (P1, P2, P3, P4, Angle, Thickness, Color, Item)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(Item, outline=Color, width=Width_Draw, state="normal")
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
    def _Line_Endpoint_Hit(self, ID, X, Y, Tol_Image):
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
            if Best_D is not None and Best_D <= Tol_Image * 1.15:
                return Best_I, Best_D
            return None, None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Line_Endpoint_Hit -> {E}")
            return None, None

    def Point_On_Line(self, ID, X, Y, Tol_Image):
        try:
            if ID not in self._Lines:
                return False
            Points, Angle, Thickness, Color, Item, Handles = self._Lines[ID]
            if not Points or len(Points) < 2:
                return False
            (X1, Y1), (X2, Y2) = Points[:2]
            D, _ = self._Distance_Point_To_Segment(X, Y, X1, Y1, X2, Y2)
            return D <= Tol_Image * 1.5
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
            if ID not in self._Lines or not self._Render_Info:
                return
            Points, Angle, Thickness, Color, Item, Handles = self._Lines[ID]
            if not Points or len(Points) < 2:
                return
            P1 = self.Image_To_Canvas(Points[0][0], Points[0][1])
            P2 = self.Image_To_Canvas(Points[1][0], Points[1][1])
            if not P1 or not P2:
                return
            Width_Draw = Thickness * (2 if self._Selected_Line_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_line(P1[0], P1[1], P2[0], P2[1], fill=Color, width=Width_Draw)
            else:
                self._Canvas._Frame.coords(Item, P1[0], P1[1], P2[0], P2[1])
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
            if not hasattr(self, "_Lines"):
                self._Lines = {}
            if not hasattr(self, "_Line_ID_Next"):
                self._Line_ID_Next = 1
            if not hasattr(self, "_Selected_Line_ID"):
                self._Selected_Line_ID = None
            if not hasattr(self, "_Line_Disabled"):
                self._Line_Disabled = {}
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            View_Width = float(self._Image_Width) / max(1e-9, Zoom_Scale)
            View_Height = float(self._Image_Height) / max(1e-9, Zoom_Scale)
            if getattr(self, "_Zoom_Center", None) is not None:
                Center_X, Center_Y = self._Zoom_Center
                Center_X = float(Center_X)
                Center_Y = float(Center_Y)
            else:
                Center_X = float(self._Image_Width) * 0.5
                Center_Y = float(self._Image_Height) * 0.5
            Default_L = min(float(View_Width), float(View_Height)) * 0.35
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
            if not hasattr(self, "_Lines"):
                self._Lines = {}
            if not hasattr(self, "_Line_Disabled"):
                self._Line_Disabled = {}
            if not self._Lines:
                return
            if ID is None:
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
            if not hasattr(self, "_Lines"):
                self._Lines = {}
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
            if not hasattr(self, "_Lines"):
                self._Lines = {}
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
                if hasattr(self, "_Selected_Line_ID"):
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
            if hasattr(self, "_Selected_Line_ID") and self._Selected_Line_ID == ID:
                self._Selected_Line_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Line -> {E}")

    def _Poly_Point_Hit(self, Points, X, Y, Tol_Image):
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
            if Best_D is not None and Best_D <= Tol_Image * 1.15:
                return Best_I, Best_D
            return None, None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Poly_Point_Hit -> {E}")
            return None, None

    def _Point_On_Polyline(self, Points, X, Y, Tol_Image):
        try:
            I, D, T = self._Closest_Segment_Index(Points, X, Y)
            if D is None:
                return False
            return D <= Tol_Image * 1.5
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Point_On_Polyline -> {E}")
            return False

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

    def _Point_On_Polygon_Edge(self, Points, X, Y, Tol_Image):
        try:
            I, D, T = self._Closest_Edge_Index(Points, X, Y)
            if D is None:
                return False
            return D <= Tol_Image * 1.5
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Point_On_Polygon_Edge -> {E}")
            return False

    def Polyline_Draw(self, ID):
        try:
            if ID not in self._Polylines or not self._Render_Info:
                return
            Points, Angle, Thickness, Color, Item, Handles = self._Polylines[ID]
            if not Points or len(Points) < 2:
                return
            Screen = []
            for X, Y in Points:
                P = self.Image_To_Canvas(X, Y)
                if not P:
                    return
                Screen.append(P[0])
                Screen.append(P[1])
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

    def Polygon_Draw(self, ID):
        try:
            if ID not in self._Polygons or not self._Render_Info:
                return
            Points, Angle, Thickness, Color, Item, Handles = self._Polygons[ID]
            if not Points or len(Points) < 3:
                return
            Screen = []
            for X, Y in Points:
                P = self.Image_To_Canvas(X, Y)
                if not P:
                    return
                Screen.append(P[0])
                Screen.append(P[1])
            Width_Draw = Thickness * (2 if self._Selected_Polygon_ID == ID else 1)
            if not Item:
                Item = self._Canvas._Frame.create_polygon(*Screen, outline=Color, fill="", width=Width_Draw)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(Item, outline=Color, width=Width_Draw, state="normal")
                self._Canvas._Frame.tag_raise(Item)
            if self._Selected_Polygon_ID == ID:
                Handles = self._Draw_Point_Handles(Points, Color, Handles)
            else:
                Handles = self._Clear_Handles(Handles)
            self._Polygons[ID] = (Points, Angle, Thickness, Color, Item, Handles)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polygon_Draw -> {E}")

    def Add_Polyline(self, Points=None, Angle=0, Thickness=2, Color="#5d6d7e"):
        try:
            if not hasattr(self, "_Polylines"):
                self._Polylines = {}
            if not hasattr(self, "_Polyline_ID_Next"):
                self._Polyline_ID_Next = 1
            if not hasattr(self, "_Selected_Polyline_ID"):
                self._Selected_Polyline_ID = None
            if not hasattr(self, "_Polyline_Disabled"):
                self._Polyline_Disabled = {}
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            View_Width = float(self._Image_Width) / max(1e-9, Zoom_Scale)
            View_Height = float(self._Image_Height) / max(1e-9, Zoom_Scale)
            if getattr(self, "_Zoom_Center", None) is not None:
                Center_X, Center_Y = self._Zoom_Center
                Center_X = float(Center_X)
                Center_Y = float(Center_Y)
            else:
                Center_X = float(self._Image_Width) * 0.5
                Center_Y = float(self._Image_Height) * 0.5
            D = min(View_Width, View_Height) * 0.18
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
            if not hasattr(self, "_Polylines"):
                self._Polylines = {}
            if not hasattr(self, "_Polyline_Disabled"):
                self._Polyline_Disabled = {}
            if not self._Polylines:
                return
            if ID is None:
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
            if not hasattr(self, "_Polylines"):
                self._Polylines = {}
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
            if not hasattr(self, "_Polylines"):
                self._Polylines = {}
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
                if hasattr(self, "_Selected_Polyline_ID"):
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
            if hasattr(self, "_Selected_Polyline_ID") and self._Selected_Polyline_ID == ID:
                self._Selected_Polyline_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Polyline -> {E}")

    def Add_Polygon(self, Points=None, Angle=0, Thickness=2, Color="#5499c7"):
        try:
            if not hasattr(self, "_Polygons"):
                self._Polygons = {}
            if not hasattr(self, "_Polygon_ID_Next"):
                self._Polygon_ID_Next = 1
            if not hasattr(self, "_Selected_Polygon_ID"):
                self._Selected_Polygon_ID = None
            if not hasattr(self, "_Polygon_Disabled"):
                self._Polygon_Disabled = {}
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            View_Width = float(self._Image_Width) / max(1e-9, Zoom_Scale)
            View_Height = float(self._Image_Height) / max(1e-9, Zoom_Scale)
            if getattr(self, "_Zoom_Center", None) is not None:
                Center_X, Center_Y = self._Zoom_Center
                Center_X = float(Center_X)
                Center_Y = float(Center_Y)
            else:
                Center_X = float(self._Image_Width) * 0.5
                Center_Y = float(self._Image_Height) * 0.5
            D = min(View_Width, View_Height) * 0.20
            Default = [(Center_X, Center_Y - D), (Center_X + D, Center_Y + D), (Center_X - D, Center_Y + D)]
            if Points is None:
                Points = Default
            if not isinstance(Points, (list, tuple)) or len(Points) < 3:
                return None
            Points_Out = [(float(P[0]), float(P[1])) for P in Points]
            ID = self._Polygon_ID_Next
            self._Polygon_ID_Next += 1
            self._Polygons[ID] = (Points_Out, float(Angle), float(Thickness), str(Color), None, [])
            self.Render()
            self._Callback_Invoke("Polygon", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Polygon -> {E}")

    def Update_Polygon(self, ID=None, Points=None, Angle=None, Thickness=None, Color=None, Disabled=None):
        try:
            if not hasattr(self, "_Polygons"):
                self._Polygons = {}
            if not hasattr(self, "_Polygon_Disabled"):
                self._Polygon_Disabled = {}
            if not self._Polygons:
                return
            if ID is None:
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return
            P0, A0, T0, C0, Item0, Handles0 = self._Polygons[ID]
            if Points is None:
                Points = P0
            if not isinstance(Points, (list, tuple)) or len(Points) < 3:
                return
            Points_Out = [(float(P[0]), float(P[1])) for P in Points]
            Angle = float(Angle) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(C0)
            self._Polygons[ID] = (Points_Out, Angle, Thickness, Color, Item0, Handles0)
            if Disabled is not None:
                self._Polygon_Disabled[ID] = bool(Disabled)
            self.Polygon_Draw(ID)
            self._Callback_Invoke("Polygon", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Polygon -> {E}")

    def Get_Polygon(self, ID=None):
        try:
            if not hasattr(self, "_Polygons"):
                self._Polygons = {}
            if not self._Polygons:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Polygons.keys()):
                    Points, Angle, Thickness, Color, Item, Handles = self._Polygons[Each_ID]
                    Out_List.append({"ID": Each_ID, "Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color})
                return Out_List
            if ID is None:
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return None
            Points, Angle, Thickness, Color, Item, Handles = self._Polygons[ID]
            return {"Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Polygon -> {E}")

    def Remove_Polygon(self, ID=None):
        try:
            if not hasattr(self, "_Polygons"):
                self._Polygons = {}
            if not self._Polygons:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Polygons.items()):
                    self._Callback_Invoke("Polygon", ID=Each_ID, Event="Remove")
                    Item = Data[4]
                    Handles = Data[5]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    self._Clear_Handles(Handles)
                self._Polygons.clear()
                if hasattr(self, "_Selected_Polygon_ID"):
                    self._Selected_Polygon_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return
            self._Callback_Invoke("Polygon", ID=ID, Event="Remove")
            Item = self._Polygons[ID][4]
            Handles = self._Polygons[ID][5]
            if Item:
                self._Canvas.Delete_Item(Item)
            self._Clear_Handles(Handles)
            del self._Polygons[ID]
            if hasattr(self, "_Selected_Polygon_ID") and self._Selected_Polygon_ID == ID:
                self._Selected_Polygon_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Polygon -> {E}")

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
            self._Callback_Invoke("Polyline", ID=ID, Event="Insert_Point")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Insert_Point_In_Polyline -> {E}")

    def _Insert_Point_In_Polygon(self, ID, X, Y):
        try:
            if ID not in self._Polygons:
                return
            Points, Angle, Thickness, Color, Item, Handles = self._Polygons[ID]
            I, D, T = self._Closest_Edge_Index(Points, X, Y)
            if I is None:
                return
            Points2 = list(Points)
            Points2.insert(I + 1, (float(X), float(Y)))
            self._Polygons[ID] = (Points2, Angle, Thickness, Color, Item, Handles)
            self.Polygon_Draw(ID)
            self._Callback_Invoke("Polygon", ID=ID, Event="Insert_Point")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Insert_Point_In_Polygon -> {E}")

    def Add_Quadrilateral(self, P1=None, P2=None, P3=None, P4=None, Angle=0, Thickness=2, Color="#45b39d"):
        try:
            if not hasattr(self, "_Quadrilaterals"):
                self._Quadrilaterals = {}
            if not hasattr(self, "_Quad_ID_Next"):
                self._Quad_ID_Next = 1
            if not hasattr(self, "_Selected_Quad_ID"):
                self._Selected_Quad_ID = None
            if not hasattr(self, "_Quad_Disabled"):
                self._Quad_Disabled = {}
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            View_Width = float(self._Image_Width) / max(1e-9, Zoom_Scale)
            View_Height = float(self._Image_Height) / max(1e-9, Zoom_Scale)
            if getattr(self, "_Zoom_Center", None) is not None:
                Center_X, Center_Y = self._Zoom_Center
                Center_X = float(Center_X)
                Center_Y = float(Center_Y)
            else:
                Center_X = float(self._Image_Width) * 0.5
                Center_Y = float(self._Image_Height) * 0.5
            Default_W = float(View_Width) * 0.25
            Default_H = float(View_Height) * 0.25
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
            self._Quadrilaterals[ID] = (P1, P2, P3, P4, float(Angle), float(Thickness), str(Color), None)
            self.Render()
            self._Callback_Invoke("Quadrilateral", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Quadrilateral -> {E}")

    def Update_Quadrilateral(self, ID=None, P1=None, P2=None, P3=None, P4=None, Angle=None, Thickness=None, Color=None, Disabled=None):
        try:
            if not hasattr(self, "_Quadrilaterals"):
                self._Quadrilaterals = {}
            if not hasattr(self, "_Quad_Disabled"):
                self._Quad_Disabled = {}
            if not self._Quadrilaterals:
                return
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            P10, P20, P30, P40, A0, T0, Col0, Item0 = self._Quadrilaterals[ID]
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
            Color = str(Color) if Color is not None else str(Col0)
            self._Quadrilaterals[ID] = (P1, P2, P3, P4, Angle, Thickness, Color, Item0)
            if Disabled is not None:
                self._Quad_Disabled[ID] = bool(Disabled)
            if hasattr(self, "_Quad_Draw"):
                self._Quad_Draw(ID)
            else:
                self.Render()
            self._Callback_Invoke("Quadrilateral", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Quadrilateral -> {E}")

    def Get_Quadrilateral(self, ID=None):
        try:
            if not hasattr(self, "_Quadrilaterals"):
                self._Quadrilaterals = {}
            if not self._Quadrilaterals:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out_List = []
                for Each_ID in sorted(self._Quadrilaterals.keys()):
                    P1, P2, P3, P4, Angle, Thickness, Color, Item = self._Quadrilaterals[Each_ID]
                    Out_List.append({"ID": Each_ID, "P1": [P1[0], P1[1]], "P2": [P2[0], P2[1]], "P3": [P3[0], P3[1]], "P4": [P4[0], P4[1]], "Angle": Angle, "Thickness": Thickness, "Color": Color})
                return Out_List
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return None
            P1, P2, P3, P4, Angle, Thickness, Color, Item = self._Quadrilaterals[ID]
            return {"P1": [P1[0], P1[1]], "P2": [P2[0], P2[1]], "P3": [P3[0], P3[1]], "P4": [P4[0], P4[1]], "Angle": Angle, "Thickness": Thickness, "Color": Color}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Quadrilateral -> {E}")

    def Remove_Quadrilateral(self, ID=None):
        try:
            if not hasattr(self, "_Quadrilaterals"):
                self._Quadrilaterals = {}
            if not self._Quadrilaterals:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Quadrilaterals.items()):
                    self._Callback_Invoke("Quadrilateral", ID=Each_ID, Event="Remove")
                    Item = Data[7]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Quad_Handles"):
                        Handles = self._Quad_Handles.pop(Each_ID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                self._Quadrilaterals.clear()
                if hasattr(self, "_Selected_Quad_ID"):
                    self._Selected_Quad_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            self._Callback_Invoke("Quadrilateral", ID=ID, Event="Remove")
            Item = self._Quadrilaterals[ID][7]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Quad_Handles"):
                Handles = self._Quad_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)

            del self._Quadrilaterals[ID]
            if hasattr(self, "_Selected_Quad_ID") and self._Selected_Quad_ID == ID:
                self._Selected_Quad_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Quadrilateral -> {E}")

    def Add_Rectangle(self, X=None, Y=None, Width=None, Height=None, Angle=0, Thickness=2, Color="#dc7633"):
        try:
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            View_Width = float(self._Image_Width) / max(1e-9, Zoom_Scale)
            View_Height = float(self._Image_Height) / max(1e-9, Zoom_Scale)
            if X is None or Y is None:
                if getattr(self, "_Zoom_Center", None) is not None:
                    Center_X, Center_Y = self._Zoom_Center
                    X = float(Center_X)
                    Y = float(Center_Y)
                else:
                    X = float(self._Image_Width) * 0.5
                    Y = float(self._Image_Height) * 0.5
            if Width is None:
                Width = float(View_Width) * 0.2
            if Height is None:
                Height = float(View_Height) * 0.2
            ID = self._Rect_ID_Next
            self._Rect_ID_Next += 1
            self._Rectangles[ID] = (float(X), float(Y), float(Width), float(Height), float(Angle), float(Thickness), str(Color), None)
            self.Render()
            self._Callback_Invoke("Rectangle", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Rectangle -> {E}")

    def Update_Rectangle(self, ID=None, X=None, Y=None, Width=None, Height=None, Angle=None, Thickness=None, Color=None, Disabled=None, Disable_Rotation=None):
        try:
            if not hasattr(self, "_Rect_Disabled"):
                self._Rect_Disabled = {}
            if not hasattr(self, "_Rect_Disable_Rotation"):
                self._Rect_Disable_Rotation = {}
            if ID is None:
                if not self._Rectangles:
                    return
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            C0x, C0y, W0, H0, A0, T0, Col0, Item0 = self._Rectangles[ID]
            X = X if X is not None else C0x
            Y = Y if Y is not None else C0y
            Width = max(2.0, Width if Width is not None else W0)
            Height = max(2.0, Height if Height is not None else H0)
            Angle = self.Normalize_Angle(Angle if Angle is not None else A0)
            Thickness = Thickness if Thickness is not None else T0
            Color = Color if Color is not None else Col0
            self._Rectangles[ID] = (float(X), float(Y), float(Width), float(Height), float(Angle), float(Thickness), str(Color), Item0)
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
                    X, Y, Width, Height, Angle, Thickness, Color, Item = self._Rectangles[Each_ID]
                    Out_List.append({"ID": Each_ID, "X": X, "Y": Y, "Width": Width, "Height": Height, "Angle": Angle, "Thickness": Thickness, "Color": Color})
                return Out_List
            if ID is None:
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return None
            X, Y, Width, Height, Angle, Thickness, Color, Item = self._Rectangles[ID]
            return {"X": X, "Y": Y, "Width": Width, "Height": Height, "Angle": Angle, "Thickness": Thickness, "Color": Color}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Rectangle -> {E}")

    def Remove_Rectangle(self, ID=None):
        try:
            if not self._Rectangles:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Rectangles.items()):
                    self._Callback_Invoke("Rectangle", ID=Each_ID, Event="Remove")
                    Item = Data[7]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Rect_Handles"):
                        Handles = self._Rect_Handles.pop(Each_ID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                self._Rectangles.clear()
                self._Selected_Rect_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            self._Callback_Invoke("Rectangle", ID=ID, Event="Remove")
            Item = self._Rectangles[ID][7]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Rect_Handles"):
                Handles = self._Rect_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)

            del self._Rectangles[ID]
            if self._Selected_Rect_ID == ID:
                self._Selected_Rect_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Rectangle -> {E}")

    def Add_Circle(self, X=None, Y=None, Radius=None, Thickness=2, Color="#a569bd"):
        try:
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            View_Width = float(self._Image_Width) / max(1e-9, Zoom_Scale)
            View_Height = float(self._Image_Height) / max(1e-9, Zoom_Scale)
            if X is None or Y is None:
                if getattr(self, "_Zoom_Center", None) is not None:
                    Center_X, Center_Y = self._Zoom_Center
                    X = float(Center_X)
                    Y = float(Center_Y)
                else:
                    X = float(self._Image_Width) * 0.5
                    Y = float(self._Image_Height) * 0.5
            if Radius is None:
                Radius = min(float(View_Width), float(View_Height)) * 0.1
            ID = self._Circle_ID_Next
            self._Circle_ID_Next += 1
            self._Circles[ID] = (float(X), float(Y), float(Radius), float(Thickness), str(Color), None)
            self.Render()
            self._Callback_Invoke("Circle", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Circle -> {E}")

    def Update_Circle(self, ID=None, X=None, Y=None, Radius=None, Thickness=None, Color=None, Disabled=None):
        try:
            if not hasattr(self, "_Circle_Disabled"):
                self._Circle_Disabled = {}
            if ID is None:
                if not self._Circles:
                    return
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            C0x, C0y, R0, T0, Col0, Item0 = self._Circles[ID]
            X = X if X is not None else C0x
            Y = Y if Y is not None else C0y
            Radius = max(1.0, Radius if Radius is not None else R0)
            Thickness = Thickness if Thickness is not None else T0
            Color = Color if Color is not None else Col0
            self._Circles[ID] = (float(X), float(Y), float(Radius), float(Thickness), str(Color), Item0)
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
                    X, Y, Radius, Thickness, Color, Item = self._Circles[Each_ID]
                    Out_List.append({"ID": Each_ID, "X": X, "Y": Y, "Radius": Radius, "Thickness": Thickness, "Color": Color})
                return Out_List
            if ID is None:
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return None
            X, Y, Radius, Thickness, Color, Item = self._Circles[ID]
            return {"X": X, "Y": Y, "Radius": Radius, "Thickness": Thickness, "Color": Color}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Circle -> {E}")

    def Remove_Circle(self, ID=None):
        try:
            if not self._Circles:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for Each_ID, Data in list(self._Circles.items()):
                    self._Callback_Invoke("Circle", ID=Each_ID, Event="Remove")
                    Item = Data[5]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Circle_Center_Handles"):
                        Handles = self._Circle_Center_Handles.pop(Each_ID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                self._Circles.clear()
                self._Selected_Circle_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            self._Callback_Invoke("Circle", ID=ID, Event="Remove")
            Item = self._Circles[ID][5]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Circle_Center_Handles"):
                Handles = self._Circle_Center_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)

            del self._Circles[ID]
            if self._Selected_Circle_ID == ID:
                self._Selected_Circle_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Circle -> {E}")

    def Clear(self):
        try:
            for _, Data in list(self._Rectangles.items()):
                Item = Data[7]
                if Item:
                    self._Canvas.Delete_Item(Item)
            for _, Data in list(self._Circles.items()):
                Item = Data[5]
                if Item:
                    self._Canvas.Delete_Item(Item)
            for _, Data in list(self._Quadrilaterals.items()):
                Item = Data[7]
                if Item:
                    self._Canvas.Delete_Item(Item)
            for _, Data in list(getattr(self, "_Lines", {}).items()):
                Item = Data[4]
                Handles = Data[5]
                if Item:
                    self._Canvas.Delete_Item(Item)
                self._Clear_Handles(Handles)
            for _, Data in list(getattr(self, "_Polylines", {}).items()):
                Item = Data[4]
                Handles = Data[5]
                if Item:
                    self._Canvas.Delete_Item(Item)
                self._Clear_Handles(Handles)
            for _, Data in list(getattr(self, "_Polygons", {}).items()):
                Item = Data[4]
                Handles = Data[5]
                if Item:
                    self._Canvas.Delete_Item(Item)
                self._Clear_Handles(Handles)
            self._Rectangles.clear()
            self._Circles.clear()
            self._Quadrilaterals.clear()
            self._Lines.clear()
            self._Polylines.clear()
            self._Polygons.clear()
            self._Selected_Rect_ID = None
            self._Selected_Circle_ID = None
            self._Selected_Quad_ID = None
            self._Selected_Line_ID = None
            self._Selected_Polyline_ID = None
            self._Selected_Polygon_ID = None
            self._Rect_ID_Next = 1
            self._Circle_ID_Next = 1
            self._Quad_ID_Next = 1
            self._Line_ID_Next = 1
            self._Polyline_ID_Next = 1
            self._Polygon_ID_Next = 1

            if hasattr(self, "_Rect_Handles"):
                for _, Handles in list(self._Rect_Handles.items()):
                    self._Clear_Handles(Handles)
                self._Rect_Handles.clear()
            if hasattr(self, "_Quad_Handles"):
                for _, Handles in list(self._Quad_Handles.items()):
                    self._Clear_Handles(Handles)
                self._Quad_Handles.clear()
            if hasattr(self, "_Circle_Center_Handles"):
                for _, Handles in list(self._Circle_Center_Handles.items()):
                    self._Clear_Handles(Handles)
                self._Circle_Center_Handles.clear()
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Render(self):
        try:
            if not self._Image:
                return
            FX, FY, FW, FH = self._Canvas.Box()
            if FH <= 0 or FW <= 0:
                return
            Out = self.Convert(FW, FH)
            if not Out:
                return
            self._Render_Info = {"Left": Out["Left"], "Top": Out["Top"], "Scale": Out["Scale"], "Crop_Left": Out["Crop_Left"], "Crop_Top": Out["Crop_Top"], "Canvas_W": Out["Canvas_W"], "Canvas_H": Out["Canvas_H"]}
            if not self._Image_Window:
                self._Image_Window = self._Canvas._Frame.create_image(Out["Left"], Out["Top"], image=Out["Image"], anchor="nw")
                self._Canvas._Frame.Temp_Image = Out["Image"]
            else:
                self._Canvas._Frame.itemconfig(self._Image_Window, image=Out["Image"])
                self._Canvas._Frame.coords(self._Image_Window, Out["Left"], Out["Top"])
                self._Canvas._Frame.Temp_Image = Out["Image"]
            self._Canvas._Frame.itemconfigure(self._Image_Window, state="normal")
            self._Canvas._Frame.tag_raise(self._Image_Window)
            for ID in sorted(self._Rectangles.keys()):
                self.Rect_Draw(ID)
            for ID in sorted(self._Circles.keys()):
                self.Circle_Draw(ID)
            for ID in sorted(self._Quadrilaterals.keys()):
                self.Quad_Draw(ID)
            for ID in sorted(getattr(self, "_Lines", {}).keys()):
                self.Line_Draw(ID)
            for ID in sorted(getattr(self, "_Polylines", {}).keys()):
                self.Polyline_Draw(ID)
            for ID in sorted(getattr(self, "_Polygons", {}).keys()):
                self.Polygon_Draw(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Render -> {E}")

    def Pick_Shape(self, IX, IY):
        try:
            if not hasattr(self, "_Rect_Disabled"):
                self._Rect_Disabled = {}
            if not hasattr(self, "_Circle_Disabled"):
                self._Circle_Disabled = {}
            if not hasattr(self, "_Quad_Disabled"):
                self._Quad_Disabled = {}
            if not hasattr(self, "_Line_Disabled"):
                self._Line_Disabled = {}
            if not hasattr(self, "_Polyline_Disabled"):
                self._Polyline_Disabled = {}
            if not hasattr(self, "_Polygon_Disabled"):
                self._Polygon_Disabled = {}
            Tol_I = self.Edge_Tolerance()
            Candidates = []
            for ID, (Cx, Cy, W, H, A, T, Col, Item) in self._Rectangles.items():
                if self._Rect_Disabled.get(ID, False):
                    continue
                if self.Point_In_Rect(ID, IX, IY):
                    Candidates.append(("rect", ID, W * H))
            for ID, (Cx, Cy, R, T, Col, Item) in self._Circles.items():
                if self._Circle_Disabled.get(ID, False):
                    continue
                if self.Point_In_Circle(ID, IX, IY):
                    Candidates.append(("circle", ID, math.pi * R * R))
            for ID, Quad in self._Quadrilaterals.items():
                if self._Quad_Disabled.get(ID, False):
                    continue
                if self.Point_In_Quad(ID, IX, IY):
                    P1, P2, P3, P4, A0, T0, C0, Item0 = Quad
                    Area = self.Quad_Area([P1, P2, P3, P4])
                    Candidates.append(("quad", ID, Area))
            for ID, Data in getattr(self, "_Lines", {}).items():
                if self._Line_Disabled.get(ID, False):
                    continue
                if self.Point_On_Line(ID, IX, IY, Tol_I):
                    Points, Angle, Thickness, Color, Item, Handles = Data
                    (X1, Y1), (X2, Y2) = Points[:2]
                    Bx = abs(X2 - X1) + Tol_I
                    By = abs(Y2 - Y1) + Tol_I
                    Candidates.append(("line", ID, Bx * By))
            for ID, Data in getattr(self, "_Polylines", {}).items():
                if self._Polyline_Disabled.get(ID, False):
                    continue
                Points, Angle, Thickness, Color, Item, Handles = Data
                if self._Point_On_Polyline(Points, IX, IY, Tol_I):
                    L = self._Polyline_Length(Points)
                    Candidates.append(("polyline", ID, max(1.0, L)))
            for ID, Data in getattr(self, "_Polygons", {}).items():
                if self._Polygon_Disabled.get(ID, False):
                    continue
                Points, Angle, Thickness, Color, Item, Handles = Data
                if self._Point_In_Polygon(Points, IX, IY) or self._Point_On_Polygon_Edge(Points, IX, IY, Tol_I):
                    Area = self._Poly_Area(Points)
                    Candidates.append(("polygon", ID, max(1.0, Area)))
            if not Candidates:
                return ("none", None)
            Candidates.sort(key=lambda X: X[2])
            Mode, ID, _ = Candidates[0]
            self._Selected_Rect_ID = None
            self._Selected_Circle_ID = None
            self._Selected_Quad_ID = None
            self._Selected_Line_ID = None
            self._Selected_Polyline_ID = None
            self._Selected_Polygon_ID = None
            if Mode == "rect":
                self._Selected_Rect_ID = ID
            elif Mode == "circle":
                self._Selected_Circle_ID = ID
            elif Mode == "quad":
                self._Selected_Quad_ID = ID
            elif Mode == "line":
                self._Selected_Line_ID = ID
            elif Mode == "polyline":
                self._Selected_Polyline_ID = ID
            elif Mode == "polygon":
                self._Selected_Polygon_ID = ID
            self.Render()
            return (Mode, ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pick_Shape -> {E}")

    def On_Motion(self, Event):
        try:
            CX = self._Canvas._Frame.canvasx(Event.x)
            CY = self._Canvas._Frame.canvasy(Event.y)
            P = self.Canvas_To_Image(CX, CY)
            if not P:
                self._Canvas.Bind(Cursor_Arrow=True)
                return
            X, Y = P
            Tol_I = self.Edge_Tolerance()
            if self._Selected_Rect_ID and not getattr(self, "_Rect_Disabled", {}).get(self._Selected_Rect_ID, False):
                Grip, _, _ = self.Rect_Grip_Hit(self._Selected_Rect_ID, X, Y, Tol_I)
                if Grip:
                    self._Canvas.Bind(Cursor="sizing")
                    return
                if self.Point_In_Rect(self._Selected_Rect_ID, X, Y):
                    self._Canvas.Bind(Cursor="fleur")
                    return
                self._Canvas.Bind(Cursor="exchange")
                return
            if self._Selected_Circle_ID and not getattr(self, "_Circle_Disabled", {}).get(self._Selected_Circle_ID, False):
                Cx, Cy, R, T, Col, Item = self._Circles[self._Selected_Circle_ID]
                D = math.hypot(X - Cx, Y - Cy)
                if abs(D - R) <= Tol_I * 1.5:
                    self._Canvas.Bind(Cursor="sizing")
                    return
                if self.Point_In_Circle(self._Selected_Circle_ID, X, Y):
                    self._Canvas.Bind(Cursor="fleur")
                    return
                self._Canvas.Bind(Cursor="exchange")
                return
            if self._Selected_Quad_ID and not getattr(self, "_Quad_Disabled", {}).get(self._Selected_Quad_ID, False):
                Corner_I, _ = self.Quad_Corner_Hit(self._Selected_Quad_ID, X, Y, Tol_I)
                if Corner_I is not None:
                    self._Canvas.Bind(Cursor="sizing")
                    return
                if self.Point_In_Quad(self._Selected_Quad_ID, X, Y):
                    self._Canvas.Bind(Cursor="fleur")
                    return
                self._Canvas.Bind(Cursor="exchange")
                return
            if self._Selected_Line_ID and not getattr(self, "_Line_Disabled", {}).get(self._Selected_Line_ID, False):
                End_I, _ = self._Line_Endpoint_Hit(self._Selected_Line_ID, X, Y, Tol_I)
                if End_I is not None:
                    self._Canvas.Bind(Cursor="sizing")
                    return
                if self.Point_On_Line(self._Selected_Line_ID, X, Y, Tol_I):
                    self._Canvas.Bind(Cursor="fleur")
                    return
                self._Canvas.Bind(Cursor="exchange")
                return
            if self._Selected_Polyline_ID and not getattr(self, "_Polyline_Disabled", {}).get(self._Selected_Polyline_ID, False):
                Points, Angle, Thickness, Color, Item, Handles = self._Polylines[self._Selected_Polyline_ID]
                Pi, _ = self._Poly_Point_Hit(Points, X, Y, Tol_I)
                if Pi is not None:
                    self._Canvas.Bind(Cursor="sizing")
                    return
                if self._Point_On_Polyline(Points, X, Y, Tol_I):
                    self._Canvas.Bind(Cursor="fleur")
                    return
                self._Canvas.Bind(Cursor="exchange")
                return
            if self._Selected_Polygon_ID and not getattr(self, "_Polygon_Disabled", {}).get(self._Selected_Polygon_ID, False):
                Points, Angle, Thickness, Color, Item, Handles = self._Polygons[self._Selected_Polygon_ID]
                Pi, _ = self._Poly_Point_Hit(Points, X, Y, Tol_I)
                if Pi is not None:
                    self._Canvas.Bind(Cursor="sizing")
                    return
                if self._Point_In_Polygon(Points, X, Y) or self._Point_On_Polygon_Edge(Points, X, Y, Tol_I):
                    self._Canvas.Bind(Cursor="fleur")
                    return
                self._Canvas.Bind(Cursor="exchange")
                return
            self._Canvas.Bind(Cursor_Arrow=True)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Motion -> {E}")

    def Drag_Start(self, Event):
        try:
            self._Drag_Last_X = self._Canvas._Frame.canvasx(Event.x)
            self._Drag_Last_Y = self._Canvas._Frame.canvasy(Event.y)
            self._Drag_Start_Pos = (self._Drag_Last_X, self._Drag_Last_Y)
            P = self.Canvas_To_Image(self._Drag_Last_X, self._Drag_Last_Y)
            if not P:
                self._Click_Target = ("image", None)
                self._Drag_Mode = "image"
                return
            X, Y = P
            Tol_I = self.Edge_Tolerance()
            if not hasattr(self, "_Rect_Disabled"):
                self._Rect_Disabled = {}
            if not hasattr(self, "_Circle_Disabled"):
                self._Circle_Disabled = {}
            if not hasattr(self, "_Quad_Disabled"):
                self._Quad_Disabled = {}
            if not hasattr(self, "_Line_Disabled"):
                self._Line_Disabled = {}
            if not hasattr(self, "_Polyline_Disabled"):
                self._Polyline_Disabled = {}
            if not hasattr(self, "_Polygon_Disabled"):
                self._Polygon_Disabled = {}
            if not hasattr(self, "_Rect_Disable_Rotation"):
                self._Rect_Disable_Rotation = {}

            if self._Selected_Rect_ID and not self._Rect_Disabled.get(self._Selected_Rect_ID, False):
                Grip, Local, _ = self.Rect_Grip_Hit(self._Selected_Rect_ID, X, Y, Tol_I)
                if Grip:
                    ID = self._Selected_Rect_ID
                    Cx, Cy, W, H, A, T, Col, Item = self._Rectangles[ID]
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
                Corner_I, _ = self.Quad_Corner_Hit(self._Selected_Quad_ID, X, Y, Tol_I)
                if Corner_I is not None:
                    ID = self._Selected_Quad_ID
                    P1, P2, P3, P4, A0, T0, C0, Item0 = self._Quadrilaterals[ID]
                    self._Resize_Info = {"ID": ID, "Type": "quad_corner", "Corner_Index": int(Corner_I), "Init_Points": [P1, P2, P3, P4], "Start_Angle": A0}
                    self._Drag_Mode = "quad_resize"
                    return

            if self._Selected_Line_ID and not self._Line_Disabled.get(self._Selected_Line_ID, False):
                End_I, _ = self._Line_Endpoint_Hit(self._Selected_Line_ID, X, Y, Tol_I)
                if End_I is not None:
                    ID = self._Selected_Line_ID
                    Points, A0, T0, C0, Item0, Handles0 = self._Lines[ID]
                    Center = self._Line_Center(Points)
                    self._Resize_Info = {"ID": ID, "Type": "line_endpoint", "Point_Index": int(End_I), "Init_Points": list(Points), "Center": Center, "Start_Angle": A0}
                    self._Drag_Mode = "line_resize"
                    return
                if self.Point_On_Line(self._Selected_Line_ID, X, Y, Tol_I):
                    self._Click_Target = ("line", self._Selected_Line_ID)
                    self._Drag_Mode = "line"
                    return

            if self._Selected_Polyline_ID and not self._Polyline_Disabled.get(self._Selected_Polyline_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[self._Selected_Polyline_ID]
                Pi, _ = self._Poly_Point_Hit(Points, X, Y, Tol_I)
                if Pi is not None:
                    Center = self._Poly_Center(Points)
                    self._Resize_Info = {"ID": self._Selected_Polyline_ID, "Type": "polyline_point", "Point_Index": int(Pi), "Init_Points": list(Points), "Center": Center, "Start_Angle": A0}
                    self._Drag_Mode = "polyline_point"
                    return
                if self._Point_On_Polyline(Points, X, Y, Tol_I):
                    self._Click_Target = ("polyline", self._Selected_Polyline_ID)
                    self._Drag_Mode = "polyline"
                    return

            if self._Selected_Polygon_ID and not self._Polygon_Disabled.get(self._Selected_Polygon_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Polygons[self._Selected_Polygon_ID]
                Pi, _ = self._Poly_Point_Hit(Points, X, Y, Tol_I)
                if Pi is not None:
                    Center = self._Poly_Center(Points)
                    self._Resize_Info = {"ID": self._Selected_Polygon_ID, "Type": "polygon_point", "Point_Index": int(Pi), "Init_Points": list(Points), "Center": Center, "Start_Angle": A0}
                    self._Drag_Mode = "polygon_point"
                    return
                if self._Point_In_Polygon(Points, X, Y) or self._Point_On_Polygon_Edge(Points, X, Y, Tol_I):
                    self._Click_Target = ("polygon", self._Selected_Polygon_ID)
                    self._Drag_Mode = "polygon"
                    return

            Best = None
            Best_D = None

            for ID in self._Rectangles:
                if self._Rect_Disabled.get(ID, False):
                    continue
                Grip, Local, Dist = self.Rect_Grip_Hit(ID, X, Y, Tol_I)
                if Grip:
                    if Best_D is None or Dist < Best_D:
                        Best = ("rect", ID, Grip)
                        Best_D = Dist

            for ID in self._Quadrilaterals:
                if self._Quad_Disabled.get(ID, False):
                    continue
                Corner_I, Dist = self.Quad_Corner_Hit(ID, X, Y, Tol_I)
                if Corner_I is not None:
                    if Best_D is None or Dist < Best_D:
                        Best = ("quad_corner", ID, int(Corner_I))
                        Best_D = Dist

            for ID, (Cx, Cy, R, T, Col, Item) in self._Circles.items():
                if self._Circle_Disabled.get(ID, False):
                    continue
                D = math.hypot(X - Cx, Y - Cy)
                Diff = abs(D - R)
                if Diff <= Tol_I * 1.5:
                    if Best_D is None or Diff < Best_D:
                        Best = ("circle_resize", ID, None)
                        Best_D = Diff

            for ID, Data in getattr(self, "_Lines", {}).items():
                if self._Line_Disabled.get(ID, False):
                    continue
                End_I, Dist = self._Line_Endpoint_Hit(ID, X, Y, Tol_I)
                if End_I is not None:
                    if Best_D is None or Dist < Best_D:
                        Best = ("line_endpoint", ID, int(End_I))
                        Best_D = Dist

            for ID, Data in getattr(self, "_Polylines", {}).items():
                if self._Polyline_Disabled.get(ID, False):
                    continue
                Points, A0, T0, C0, Item0, Handles0 = Data
                Pi, Dist = self._Poly_Point_Hit(Points, X, Y, Tol_I)
                if Pi is not None:
                    if Best_D is None or Dist < Best_D:
                        Best = ("polyline_point", ID, int(Pi))
                        Best_D = Dist

            for ID, Data in getattr(self, "_Polygons", {}).items():
                if self._Polygon_Disabled.get(ID, False):
                    continue
                Points, A0, T0, C0, Item0, Handles0 = Data
                Pi, Dist = self._Poly_Point_Hit(Points, X, Y, Tol_I)
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
                    Cx, Cy, W, H, A, T, Col, Item = self._Rectangles[ID]
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
                    P1, P2, P3, P4, A0, T0, C0, Item0 = self._Quadrilaterals[ID]
                    self._Resize_Info = {"ID": ID, "Type": "quad_corner", "Corner_Index": int(Hit), "Init_Points": [P1, P2, P3, P4], "Start_Angle": A0}
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
                    Cx, Cy, R, T, Col, Item = self._Circles[ID]
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
                    self._Resize_Info = {"ID": ID, "Type": "line_endpoint", "Point_Index": int(Hit), "Init_Points": list(Points), "Center": Center, "Start_Angle": A0}
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
                    self._Resize_Info = {"ID": ID, "Type": "polyline_point", "Point_Index": int(Hit), "Init_Points": list(Points), "Center": Center, "Start_Angle": A0}
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
                    Points, A0, T0, C0, Item0, Handles0 = self._Polygons[ID]
                    Center = self._Poly_Center(Points)
                    self._Resize_Info = {"ID": ID, "Type": "polygon_point", "Point_Index": int(Hit), "Init_Points": list(Points), "Center": Center, "Start_Angle": A0}
                    self._Drag_Mode = "polygon_point"
                    self.Render()
                    return

            Mode, ID = self.Pick_Shape(X, Y)
            if Mode == "rect" and not self._Rect_Disabled.get(ID, False):
                self._Click_Target = ("rect", ID)
                self._Drag_Mode = "rect"
                return
            if Mode == "circle" and not self._Circle_Disabled.get(ID, False):
                self._Click_Target = ("circle", ID)
                self._Drag_Mode = "circle"
                return
            if Mode == "quad" and not self._Quad_Disabled.get(ID, False):
                self._Click_Target = ("quad", ID)
                self._Drag_Mode = "quad"
                return
            if Mode == "line" and not self._Line_Disabled.get(ID, False):
                self._Click_Target = ("line", ID)
                self._Drag_Mode = "line"
                return
            if Mode == "polyline" and not self._Polyline_Disabled.get(ID, False):
                self._Click_Target = ("polyline", ID)
                self._Drag_Mode = "polyline"
                return
            if Mode == "polygon" and not self._Polygon_Disabled.get(ID, False):
                self._Click_Target = ("polygon", ID)
                self._Drag_Mode = "polygon"
                return

            if self._Selected_Rect_ID and not self._Rect_Disabled.get(self._Selected_Rect_ID, False) and not self._Rect_Disable_Rotation.get(self._Selected_Rect_ID, False):
                Cx, Cy, W, H, A, T, Col, Item = self._Rectangles[self._Selected_Rect_ID]
                self._Resize_Info = {"ID": self._Selected_Rect_ID, "Type": "rect_rotate", "Start_Angle": A, "Start_Vector": (X - Cx, Y - Cy)}
                self._Drag_Mode = "rect_rotate"
                return

            if self._Selected_Quad_ID and not self._Quad_Disabled.get(self._Selected_Quad_ID, False):
                P1, P2, P3, P4, A0, T0, C0, Item0 = self._Quadrilaterals[self._Selected_Quad_ID]
                Points0 = [P1, P2, P3, P4]
                Center = self.Quad_Center(Points0)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Quad_ID, "Type": "quad_rotate", "Start_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": Points0, "Center": Center}
                self._Drag_Mode = "quad_rotate"
                return

            if self._Selected_Line_ID and not self._Line_Disabled.get(self._Selected_Line_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Lines[self._Selected_Line_ID]
                Center = self._Line_Center(Points)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Line_ID, "Type": "line_rotate", "Start_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": list(Points), "Center": Center}
                self._Drag_Mode = "line_rotate"
                return

            if self._Selected_Polyline_ID and not self._Polyline_Disabled.get(self._Selected_Polyline_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[self._Selected_Polyline_ID]
                Center = self._Poly_Center(Points)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Polyline_ID, "Type": "polyline_rotate", "Start_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": list(Points), "Center": Center}
                self._Drag_Mode = "polyline_rotate"
                return

            if self._Selected_Polygon_ID and not self._Polygon_Disabled.get(self._Selected_Polygon_ID, False):
                Points, A0, T0, C0, Item0, Handles0 = self._Polygons[self._Selected_Polygon_ID]
                Center = self._Poly_Center(Points)
                Cx, Cy = Center
                self._Resize_Info = {"ID": self._Selected_Polygon_ID, "Type": "polygon_rotate", "Start_Angle": A0, "Start_Vector": (X - Cx, Y - Cy), "Init_Points": list(Points), "Center": Center}
                self._Drag_Mode = "polygon_rotate"
                return

            self._Click_Target = ("image", None)
            self._Drag_Mode = "image"
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag_Start -> {E}")

    def Drag(self, Event):
        try:
            if not self._Image:
                return
            CX = self._Canvas._Frame.canvasx(Event.x)
            CY = self._Canvas._Frame.canvasy(Event.y)
            DX = CX - self._Drag_Last_X
            DY = CY - self._Drag_Last_Y
            self._Drag_Last_X = CX
            self._Drag_Last_Y = CY

            if self._Drag_Mode == "rect" and self._Selected_Rect_ID and self._Render_Info and not getattr(self, "_Rect_Disabled", {}).get(self._Selected_Rect_ID, False):
                S = self._Render_Info["Scale"]
                IX = DX / S
                IY = DY / S
                Cx, Cy, W, H, A, T, Col, Item = self._Rectangles[self._Selected_Rect_ID]
                Cx = max(0, min(self._Image_Width, Cx + IX))
                Cy = max(0, min(self._Image_Height, Cy + IY))
                self._Rectangles[self._Selected_Rect_ID] = (Cx, Cy, W, H, A, T, Col, Item)
                self.Rect_Draw(self._Selected_Rect_ID)
                self._Callback_Invoke("Rectangle", ID=self._Selected_Rect_ID, Event="Update")
                return

            if self._Drag_Mode == "rect_resize" and self._Resize_Info and self._Render_Info and not getattr(self, "_Rect_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Mode = self._Resize_Info.get("Mode", "edge")
                Cx0, Cy0, W0, H0, A0 = self._Resize_Info["Init"]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Rad = -A0 * math.pi / 180.0
                CosA = math.cos(Rad)
                SinA = math.sin(Rad)
                if Mode == "corner":
                    Anchor_X, Anchor_Y = self._Resize_Info["Anchor"]
                    Dx = P[0] - Anchor_X
                    Dy = P[1] - Anchor_Y
                    U = Dx * CosA + Dy * SinA
                    V = -Dx * SinA + Dy * CosA
                    New_W = max(2.0, abs(U))
                    New_H = max(2.0, abs(V))
                    Cx = Anchor_X + 0.5 * Dx
                    Cy = Anchor_Y + 0.5 * Dy
                    self.Update_Rectangle(ID=ID, X=Cx, Y=Cy, Width=New_W, Height=New_H, Angle=A0)
                    return
                Edge = self._Resize_Info["Edge"]
                OppX, OppY = self._Resize_Info["Opp"]
                Dx = P[0] - Cx0
                Dy = P[1] - Cy0
                U = Dx * CosA + Dy * SinA
                V = -Dx * SinA + Dy * CosA
                if Edge in ("left", "right"):
                    Uc = U
                    New_W = max(2.0, abs(Uc - OppX))
                    Cx_L = (Uc + OppX) / 2.0
                    Cy_L = 0.0
                    Cx = Cx0 + Cx_L * CosA - Cy_L * SinA
                    Cy = Cy0 + Cx_L * SinA + Cy_L * CosA
                    self.Update_Rectangle(ID=ID, X=Cx, Y=Cy, Width=New_W, Height=H0, Angle=A0)
                else:
                    Vc = V
                    New_H = max(2.0, abs(Vc - OppY))
                    Cx_L = 0.0
                    Cy_L = (Vc + OppY) / 2.0
                    Cx = Cx0 + Cx_L * CosA - Cy_L * SinA
                    Cy = Cy0 + Cx_L * SinA + Cy_L * CosA
                    self.Update_Rectangle(ID=ID, X=Cx, Y=Cy, Width=W0, Height=New_H, Angle=A0)
                return

            if self._Drag_Mode == "rect_rotate" and self._Resize_Info and self._Render_Info and not getattr(self, "_Rect_Disabled", {}).get(self._Resize_Info["ID"], False) and not getattr(self, "_Rect_Disable_Rotation", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Cx, Cy, W, H, A, T, Col, Item = self._Rectangles[ID]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                V0x, V0y = self._Resize_Info["Start_Vector"]
                Ang0 = math.atan2(V0y, V0x)
                V1x = P[0] - Cx
                V1y = P[1] - Cy
                Ang1 = math.atan2(V1y, V1x)
                Delta_A_CW = -math.degrees(Ang1 - Ang0)
                self.Update_Rectangle(ID=ID, Angle=self.Normalize_Angle(self._Resize_Info["Start_Angle"] + Delta_A_CW))
                return

            if self._Drag_Mode == "circle" and self._Selected_Circle_ID and self._Render_Info and not getattr(self, "_Circle_Disabled", {}).get(self._Selected_Circle_ID, False):
                S = self._Render_Info["Scale"]
                IX = DX / S
                IY = DY / S
                Cx, Cy, R, T, Col, Item = self._Circles[self._Selected_Circle_ID]
                Cx = max(0, min(self._Image_Width, Cx + IX))
                Cy = max(0, min(self._Image_Height, Cy + IY))
                self._Circles[self._Selected_Circle_ID] = (Cx, Cy, R, T, Col, Item)
                self.Circle_Draw(self._Selected_Circle_ID)
                self._Callback_Invoke("Circle", ID=self._Selected_Circle_ID, Event="Update")
                return

            if self._Drag_Mode == "circle_resize" and self._Resize_Info and self._Render_Info and not getattr(self, "_Circle_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Cx0, Cy0 = self._Resize_Info["Init_Center"]
                R0 = self._Resize_Info["Init_R"]
                Ux, Uy = self._Resize_Info["Dir"]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Dist = math.hypot(P[0] - Cx0, P[1] - Cy0)
                Delta = Dist - self._Resize_Info["Start_Dist"]
                R = max(1.0, R0 + 0.5 * Delta)
                Cx = Cx0 + Ux * (0.5 * Delta)
                Cy = Cy0 + Uy * (0.5 * Delta)
                self.Update_Circle(ID=ID, X=Cx, Y=Cy, Radius=R)
                return

            if self._Drag_Mode == "quad" and self._Selected_Quad_ID and self._Render_Info and not getattr(self, "_Quad_Disabled", {}).get(self._Selected_Quad_ID, False):
                S = self._Render_Info["Scale"]
                IX = DX / S
                IY = DY / S
                P1, P2, P3, P4, A0, T0, C0, Item0 = self._Quadrilaterals[self._Selected_Quad_ID]
                Points = [(P1[0] + IX, P1[1] + IY), (P2[0] + IX, P2[1] + IY), (P3[0] + IX, P3[1] + IY), (P4[0] + IX, P4[1] + IY)]
                Clamped = []
                for Xp, Yp in Points:
                    Xp = max(0.0, min(float(self._Image_Width), Xp))
                    Yp = max(0.0, min(float(self._Image_Height), Yp))
                    Clamped.append((Xp, Yp))
                self._Quadrilaterals[self._Selected_Quad_ID] = (Clamped[0], Clamped[1], Clamped[2], Clamped[3], A0, T0, C0, Item0)
                self.Quad_Draw(self._Selected_Quad_ID)
                self._Callback_Invoke("Quadrilateral", ID=self._Selected_Quad_ID, Event="Update")
                return

            if self._Drag_Mode == "quad_resize" and self._Resize_Info and self._Render_Info and not getattr(self, "_Quad_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Corner_I = int(self._Resize_Info["Corner_Index"])
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Xn = max(0.0, min(float(self._Image_Width), float(P[0])))
                Yn = max(0.0, min(float(self._Image_Height), float(P[1])))
                P1, P2, P3, P4, A0, T0, C0, Item0 = self._Quadrilaterals[ID]
                Points = [P1, P2, P3, P4]
                Points[Corner_I] = (Xn, Yn)
                self._Quadrilaterals[ID] = (Points[0], Points[1], Points[2], Points[3], A0, T0, C0, Item0)
                self.Quad_Draw(ID)
                self._Callback_Invoke("Quadrilateral", ID=ID, Event="Update")
                return

            if self._Drag_Mode == "quad_rotate" and self._Resize_Info and self._Render_Info and not getattr(self, "_Quad_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Center = self._Resize_Info["Center"]
                Cx, Cy = Center
                V0x, V0y = self._Resize_Info["Start_Vector"]
                Ang0 = math.atan2(V0y, V0x)
                V1x = P[0] - Cx
                V1y = P[1] - Cy
                Ang1 = math.atan2(V1y, V1x)
                Delta_A_CW = -math.degrees(Ang1 - Ang0)
                P0 = self._Resize_Info["Init_Points"]
                Rot = self.Quad_Rotate_Points(P0, Center, Delta_A_CW)
                P1, P2, P3, P4, A0, T0, C0, Item0 = self._Quadrilaterals[ID]
                NA = self.Normalize_Angle(self._Resize_Info["Start_Angle"] + Delta_A_CW)
                self._Quadrilaterals[ID] = (Rot[0], Rot[1], Rot[2], Rot[3], NA, T0, C0, Item0)
                self.Quad_Draw(ID)
                return

            if self._Drag_Mode == "line" and self._Selected_Line_ID and self._Render_Info and not getattr(self, "_Line_Disabled", {}).get(self._Selected_Line_ID, False):
                S = self._Render_Info["Scale"]
                IX = DX / S
                IY = DY / S
                Points, A0, T0, C0, Item0, Handles0 = self._Lines[self._Selected_Line_ID]
                P1 = (max(0.0, min(float(self._Image_Width), Points[0][0] + IX)), max(0.0, min(float(self._Image_Height), Points[0][1] + IY)))
                P2 = (max(0.0, min(float(self._Image_Width), Points[1][0] + IX)), max(0.0, min(float(self._Image_Height), Points[1][1] + IY)))
                self._Lines[self._Selected_Line_ID] = ([P1, P2], A0, T0, C0, Item0, Handles0)
                self.Line_Draw(self._Selected_Line_ID)
                self._Callback_Invoke("Line", ID=self._Selected_Line_ID, Event="Update")
                return

            if self._Drag_Mode == "line_resize" and self._Resize_Info and self._Render_Info and not getattr(self, "_Line_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Pi = int(self._Resize_Info["Point_Index"])
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Xn = max(0.0, min(float(self._Image_Width), float(P[0])))
                Yn = max(0.0, min(float(self._Image_Height), float(P[1])))
                Points, A0, T0, C0, Item0, Handles0 = self._Lines[ID]
                Points2 = list(Points)
                Points2[Pi] = (Xn, Yn)
                self._Lines[ID] = (Points2, A0, T0, C0, Item0, Handles0)
                self.Line_Draw(ID)
                self._Callback_Invoke("Line", ID=ID, Event="Update")
                return

            if self._Drag_Mode == "line_rotate" and self._Resize_Info and self._Render_Info and not getattr(self, "_Line_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Center = self._Resize_Info["Center"]
                Cx, Cy = Center
                V0x, V0y = self._Resize_Info["Start_Vector"]
                Ang0 = math.atan2(V0y, V0x)
                V1x = P[0] - Cx
                V1y = P[1] - Cy
                Ang1 = math.atan2(V1y, V1x)
                Delta_A_CW = -math.degrees(Ang1 - Ang0)
                P0 = self._Resize_Info["Init_Points"]
                Rot = self._Rotate_Points(P0, Center, Delta_A_CW)
                Points, A0, T0, C0, Item0, Handles0 = self._Lines[ID]
                NA = self.Normalize_Angle(self._Resize_Info["Start_Angle"] + Delta_A_CW)
                self._Lines[ID] = (Rot[:2], NA, T0, C0, Item0, Handles0)
                self.Line_Draw(ID)
                return

            if self._Drag_Mode == "polyline" and self._Selected_Polyline_ID and self._Render_Info and not getattr(self, "_Polyline_Disabled", {}).get(self._Selected_Polyline_ID, False):
                S = self._Render_Info["Scale"]
                IX = DX / S
                IY = DY / S
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[self._Selected_Polyline_ID]
                Moved = []
                for Xp, Yp in Points:
                    Xp = max(0.0, min(float(self._Image_Width), Xp + IX))
                    Yp = max(0.0, min(float(self._Image_Height), Yp + IY))
                    Moved.append((Xp, Yp))
                self._Polylines[self._Selected_Polyline_ID] = (Moved, A0, T0, C0, Item0, Handles0)
                self.Polyline_Draw(self._Selected_Polyline_ID)
                self._Callback_Invoke("Polyline", ID=self._Selected_Polyline_ID, Event="Update")
                return

            if self._Drag_Mode == "polyline_point" and self._Resize_Info and self._Render_Info and not getattr(self, "_Polyline_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Pi = int(self._Resize_Info["Point_Index"])
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Xn = max(0.0, min(float(self._Image_Width), float(P[0])))
                Yn = max(0.0, min(float(self._Image_Height), float(P[1])))
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[ID]
                Points2 = list(Points)
                if 0 <= Pi < len(Points2):
                    Points2[Pi] = (Xn, Yn)
                self._Polylines[ID] = (Points2, A0, T0, C0, Item0, Handles0)
                self.Polyline_Draw(ID)
                self._Callback_Invoke("Polyline", ID=ID, Event="Update")
                return

            if self._Drag_Mode == "polyline_rotate" and self._Resize_Info and self._Render_Info and not getattr(self, "_Polyline_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Center = self._Resize_Info["Center"]
                Cx, Cy = Center
                V0x, V0y = self._Resize_Info["Start_Vector"]
                Ang0 = math.atan2(V0y, V0x)
                V1x = P[0] - Cx
                V1y = P[1] - Cy
                Ang1 = math.atan2(V1y, V1x)
                Delta_A_CW = -math.degrees(Ang1 - Ang0)
                P0 = self._Resize_Info["Init_Points"]
                Rot = self._Rotate_Points(P0, Center, Delta_A_CW)
                Points, A0, T0, C0, Item0, Handles0 = self._Polylines[ID]
                NA = self.Normalize_Angle(self._Resize_Info["Start_Angle"] + Delta_A_CW)
                self._Polylines[ID] = (Rot, NA, T0, C0, Item0, Handles0)
                self.Polyline_Draw(ID)
                return

            if self._Drag_Mode == "polygon" and self._Selected_Polygon_ID and self._Render_Info and not getattr(self, "_Polygon_Disabled", {}).get(self._Selected_Polygon_ID, False):
                S = self._Render_Info["Scale"]
                IX = DX / S
                IY = DY / S
                Points, A0, T0, C0, Item0, Handles0 = self._Polygons[self._Selected_Polygon_ID]
                Moved = []
                for Xp, Yp in Points:
                    Xp = max(0.0, min(float(self._Image_Width), Xp + IX))
                    Yp = max(0.0, min(float(self._Image_Height), Yp + IY))
                    Moved.append((Xp, Yp))
                self._Polygons[self._Selected_Polygon_ID] = (Moved, A0, T0, C0, Item0, Handles0)
                self.Polygon_Draw(self._Selected_Polygon_ID)
                self._Callback_Invoke("Polygon", ID=self._Selected_Polygon_ID, Event="Update")
                return

            if self._Drag_Mode == "polygon_point" and self._Resize_Info and self._Render_Info and not getattr(self, "_Polygon_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Pi = int(self._Resize_Info["Point_Index"])
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Xn = max(0.0, min(float(self._Image_Width), float(P[0])))
                Yn = max(0.0, min(float(self._Image_Height), float(P[1])))
                Points, A0, T0, C0, Item0, Handles0 = self._Polygons[ID]
                Points2 = list(Points)
                if 0 <= Pi < len(Points2):
                    Points2[Pi] = (Xn, Yn)
                self._Polygons[ID] = (Points2, A0, T0, C0, Item0, Handles0)
                self.Polygon_Draw(ID)
                self._Callback_Invoke("Polygon", ID=ID, Event="Update")
                return

            if self._Drag_Mode == "polygon_rotate" and self._Resize_Info and self._Render_Info and not getattr(self, "_Polygon_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Center = self._Resize_Info["Center"]
                Cx, Cy = Center
                V0x, V0y = self._Resize_Info["Start_Vector"]
                Ang0 = math.atan2(V0y, V0x)
                V1x = P[0] - Cx
                V1y = P[1] - Cy
                Ang1 = math.atan2(V1y, V1x)
                Delta_A_CW = -math.degrees(Ang1 - Ang0)
                P0 = self._Resize_Info["Init_Points"]
                Rot = self._Rotate_Points(P0, Center, Delta_A_CW)
                Points, A0, T0, C0, Item0, Handles0 = self._Polygons[ID]
                NA = self.Normalize_Angle(self._Resize_Info["Start_Angle"] + Delta_A_CW)
                self._Polygons[ID] = (Rot, NA, T0, C0, Item0, Handles0)
                self.Polygon_Draw(ID)
                return

            View_W = self._Image_Width / max(1e-9, self._Zoom_Scale)
            View_H = self._Image_Height / max(1e-9, self._Zoom_Scale)
            FX, FY, FW, FH = self._Canvas.Box()
            Pad = self.Inner_Padding()
            IW = max(1, FW - 2 * Pad)
            IH = max(1, FH - 2 * Pad)
            MX = -DX * (View_W / IW)
            MY = -DY * (View_H / IH)
            NCX = self._Zoom_Center[0] + MX
            NCY = self._Zoom_Center[1] + MY
            HW = View_W / 2
            HH = View_H / 2
            NCX = max(HW, min(self._Image_Width - HW, NCX))
            NCY = max(HH, min(self._Image_Height - HH, NCY))
            self._Zoom_Center = (NCX, NCY)
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag -> {E}")

    def _Is_Double_Click(self, X, Y):
        try:
            Now = time.time()
            if self._Last_Click_Pos is None:
                return False
            Dt = Now - float(self._Last_Click_Time or 0.0)
            if Dt > float(self._Double_Click_Threshold or 0.35):
                return False
            X0, Y0 = self._Last_Click_Pos
            if abs(X - X0) > 6 or abs(Y - Y0) > 6:
                return False
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Is_Double_Click -> {E}")
            return False

    def _Update_Click_Tracker(self, X, Y):
        try:
            self._Last_Click_Time = time.time()
            self._Last_Click_Pos = (float(X), float(Y))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Update_Click_Tracker -> {E}")

    def Release(self, Event):
        try:
            if not self._Drag_Start_Pos:
                return
            X0, Y0 = self._Drag_Start_Pos
            X1 = self._Canvas._Frame.canvasx(Event.x)
            Y1 = self._Canvas._Frame.canvasy(Event.y)
            Is_Click = abs(X1 - X0) < 2 and abs(Y1 - Y0) < 2
            Was_Double = False
            if Is_Click:
                Was_Double = self._Is_Double_Click(X1, Y1)
            if Is_Click:
                P = self.Canvas_To_Image(X1, Y1)
                if not P:
                    self._Selected_Rect_ID = None
                    self._Selected_Circle_ID = None
                    self._Selected_Quad_ID = None
                    self._Selected_Line_ID = None
                    self._Selected_Polyline_ID = None
                    self._Selected_Polygon_ID = None
                    self.Render()
                else:
                    Mode, ID = self.Pick_Shape(P[0], P[1])
                    if Was_Double and Mode == "polyline" and ID is not None:
                        self._Insert_Point_In_Polyline(ID, P[0], P[1])
                    if Was_Double and Mode == "polygon" and ID is not None:
                        self._Insert_Point_In_Polygon(ID, P[0], P[1])
                    if Mode == "none":
                        self._Selected_Rect_ID = None
                        self._Selected_Circle_ID = None
                        self._Selected_Quad_ID = None
                        self._Selected_Line_ID = None
                        self._Selected_Polyline_ID = None
                        self._Selected_Polygon_ID = None
                        self.Render()
                self._Update_Click_Tracker(X1, Y1)
            self._Resize_Info = None
            self._Drag_Mode = "image"
            self._Drag_Start_Pos = None
            self._Canvas.Bind(Cursor_Arrow=True)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Release -> {E}")

    def Zoom(self, Event):
        try:
            if not self._Image or not self._Image_Window:
                return
            ZF = 1.1 if getattr(Event, "delta", 0) > 0 else 0.9
            NZ = max(1.0, self._Zoom_Scale * ZF)
            if NZ == self._Zoom_Scale:
                return
            CX = self._Canvas._Frame.canvasx(Event.x)
            CY = self._Canvas._Frame.canvasy(Event.y)
            IXY = self.Canvas_To_Image(CX, CY)
            if not IXY:
                self._Zoom_Scale = NZ
                self.Render()
                return
            MX, MY = IXY
            VW = self._Image_Width / max(1e-9, self._Zoom_Scale)
            VH = self._Image_Height / max(1e-9, self._Zoom_Scale)
            VL = self._Zoom_Center[0] - VW / 2
            VT = self._Zoom_Center[1] - VH / 2
            RX = (MX - VL) / VW
            RY = (MY - VT) / VH
            NVW = self._Image_Width / max(1e-9, NZ)
            NVH = self._Image_Height / max(1e-9, NZ)
            NVL = MX - RX * NVW
            NVT = MY - RY * NVH
            NCX = NVL + NVW / 2
            NCY = NVT + NVH / 2
            HW = NVW / 2
            HH = NVH / 2
            NCX = max(HW, min(self._Image_Width - HW, NCX))
            NCY = max(HH, min(self._Image_Height - HH, NCY))
            self._Zoom_Scale = NZ
            self._Zoom_Center = (NCX, NCY)
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Zoom -> {E}")

    def Reset(self, Event=False):
        try:
            self._Zoom_Scale = 1.0
            if self._Image:
                self._Zoom_Center = (self._Image_Width // 2, self._Image_Height // 2)
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Reset -> {E}")

    def Resize(self, Event):
        try:
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")

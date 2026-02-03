from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
import math
import time
from .N_GUI import GUI

PIL_Image.MAX_IMAGE_PIXELS = None

class Viewport:

    def __init__(self, Canvas, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Viewport"
            try:
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
                self._Circle_Handles = {}
                self._Rect_Disabled = {}
                self._Circle_Disabled = {}
                self._Quad_Disabled = {}
                self._Line_Disabled = {}
                self._Polyline_Disabled = {}
                self._Polygon_Disabled = {}
                self._Rect_Disable_Rotation = {}
                self._Rect_Fill = {}
                self._Rect_Transparent = {}
                self._Circle_Fill = {}
                self._Circle_Transparent = {}
                self._Quad_Fill = {}
                self._Quad_Transparent = {}
                self._Polygon_Fill = {}
                self._Polygon_Transparent = {}
                self._Canvas._Item.append(self)
                self._Callback = None
                self._Callback_Mode = "Continuous"
                self.Bind()
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return f"Nucleon_Glunoix_Viewport[]"

    def __repr__(self):
        return f"Nucleon_Glunoix_Viewport[]"
            
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
            self._Canvas.Bind(On_Click=self.Drag_Start, On_Drag=self.Drag, On_Release=self.Release, On_Mouse_Wheel=self.Zoom, On_Right_Click=self.Reset, On_Resize=self.Resize, On_Motion=self.Motion)
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

    def Callback(self, Function, Mode="Continuous"):
        try:
            self._Callback = Function
            if Mode in ["Release", "Continuous"]:
                self._Callback_Mode = Mode
            else:
                self._Callback_Mode = "Continuous"
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Callback -> {E}")

    def Edge_Tolerance(self):
        try:
            S = self._Render_Info["Scale"] if self._Render_Info else 1.0
            return 14.0 / max(1e-9, S)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Edge_Tolerance -> {E}")

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
            OldImageWidth = float(getattr(self, "ImageWidth", 0) or getattr(self, "_Image_Width", 0) or 0)
            OldImageHeight = float(getattr(self, "ImageHeight", 0) or getattr(self, "_Image_Height", 0) or 0)
            OldZoomCenter = getattr(self, "ZoomCenter", None) if getattr(self, "ZoomCenter", None) is not None else getattr(self, "_Zoom_Center", None)
            OldZoomScale = float(getattr(self, "ZoomScale", 1.0) or getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            OldZoomOffset = getattr(self, "_Zoom_Offset", None)
            SourceObj = Frame
            if SourceObj is None and getattr(self, "Frame", False) is not False:
                SourceObj = self.Frame
            ImageObj = None
            if hasattr(SourceObj, "__class__") and getattr(type(SourceObj), "__module__", "").startswith("numpy"):
                self.Frame = SourceObj
                if getattr(self, "Image", None):
                    try:
                        self.Image.close()
                    except:
                        pass
                from PIL import Image as PILImage
                ImageObj = PILImage.fromarray(SourceObj)
            elif hasattr(SourceObj, "__class__") and str(type(SourceObj)).find("PIL.") != -1:
                self.Frame = False
                if getattr(self, "Image", None):
                    try:
                        self.Image.close()
                    except:
                        pass
                PilObj = SourceObj
                try:
                    if getattr(PilObj, "is_animated", False):
                        PilObj.seek(0)
                except:
                    pass
                ImageObj = PilObj.copy()
            else:
                try:
                    from PIL import ImageTk as PILImageTk
                    from PIL import Image as PILImage
                    PilFromTk = PILImageTk.getimage(SourceObj)
                    if str(type(PilFromTk)).find("PIL.") != -1:
                        self.Frame = False
                        if getattr(self, "Image", None):
                            try:
                                self.Image.close()
                            except:
                                pass
                        ImageObj = PilFromTk.copy()
                except:
                    ImageObj = None
            if ImageObj is None:
                from io import BytesIO as BytesIO
                import os as Os
                import urllib.parse as UrlParse
                import urllib.request as UrlRequest
                Data = None
                if isinstance(SourceObj, (bytes, bytearray, memoryview)):
                    Data = bytes(SourceObj)
                elif isinstance(SourceObj, str):
                    ParsedObj = UrlParse.urlparse(SourceObj)
                    if ParsedObj.scheme in ("http", "https"):
                        with UrlRequest.urlopen(SourceObj) as Response:
                            Data = Response.read()
                    elif Os.path.exists(SourceObj):
                        with open(SourceObj, "rb") as FileHandle:
                            Data = FileHandle.read()
                    else:
                        return
                else:
                    return
                from PIL import Image as PILImage
                with PILImage.open(BytesIO(Data)) as PilObj:
                    try:
                        if getattr(PilObj, "is_animated", False):
                            PilObj.seek(0)
                    except:
                        pass
                    ImageObj = PilObj.copy()
                self.Frame = False
                if getattr(self, "Image", None):
                    try:
                        self.Image.close()
                    except:
                        pass
            if not ImageObj:
                return
            self.Image = ImageObj
            self._Image = ImageObj
            self.ImageWidth, self.ImageHeight = self.Image.size
            self._Image_Width, self._Image_Height = self.Image.size
            NewImageWidth = float(self.ImageWidth or 0)
            NewImageHeight = float(self.ImageHeight or 0)
            self.ZoomScale = float(OldZoomScale or 1.0)
            self._Zoom_Scale = float(OldZoomScale or 1.0)
            MaxZoomScale = max(1.0, min(NewImageWidth, NewImageHeight))
            self.ZoomScale = max(1.0, min(float(self.ZoomScale), float(MaxZoomScale)))
            self._Zoom_Scale = max(1.0, min(float(self._Zoom_Scale), float(MaxZoomScale)))
            if OldZoomCenter is not None and OldImageWidth > 0 and OldImageHeight > 0 and NewImageWidth > 0 and NewImageHeight > 0:
                OldCenterX, OldCenterY = OldZoomCenter
                CenterRatioX = float(OldCenterX) / float(OldImageWidth)
                CenterRatioY = float(OldCenterY) / float(OldImageHeight)
                NewCenterX = CenterRatioX * float(NewImageWidth)
                NewCenterY = CenterRatioY * float(NewImageHeight)
                self.ZoomCenter = (NewCenterX, NewCenterY)
                self._Zoom_Center = (NewCenterX, NewCenterY)
            else:
                if getattr(self, "ZoomCenter", None) is None:
                    self.ZoomCenter = (self.ImageWidth * 0.5, self.ImageHeight * 0.5)
                CenterX, CenterY = self.ZoomCenter
                CenterX = max(0.0, min(float(CenterX), float(self.ImageWidth)))
                CenterY = max(0.0, min(float(CenterY), float(self.ImageHeight)))
                self.ZoomCenter = (CenterX, CenterY)
                self._Zoom_Center = (CenterX, CenterY)
            if OldImageWidth <= 0 or OldImageHeight <= 0:
                self._Zoom_Offset = None
            else:
                self._Zoom_Offset = OldZoomOffset
            self.Render()
        except Exception as E:
            GUI = getattr(self, "_GUI", getattr(self, "GUI", None))
            Type = getattr(self, "_Type", getattr(self, "Type", "Viewport"))
            if GUI:
                GUI.Error(f"{Type} -> Load -> {E}")

    def Convert(self, Frame_Width, Frame_Height):
        try:
            from PIL import Image as PILImage, ImageTk as PILImageTk
            Image = getattr(self, "_Image", None) if getattr(self, "_Image", None) is not None else getattr(self, "Image", None)
            if not Image:
                return None
            Padding = int(self.Inner_Padding()) if hasattr(self, "Inner_Padding") else int(self.InnerPadding())
            Inner_W = max(1, int(Frame_Width) - 2 * Padding)
            Inner_H = max(1, int(Frame_Height) - 2 * Padding)
            Image_W = float(getattr(self, "_Image_Width", 0) or getattr(self, "ImageWidth", 0) or 0)
            Image_H = float(getattr(self, "_Image_Height", 0) or getattr(self, "ImageHeight", 0) or 0)
            if Image_W <= 1 or Image_H <= 1:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", getattr(self, "ZoomScale", 1.0)) or 1.0)
            Fit_Scale = min(float(Inner_W) / max(1e-9, Image_W), float(Inner_H) / max(1e-9, Image_H))
            Cover_Scale = max(float(Inner_W) / max(1e-9, Image_W), float(Inner_H) / max(1e-9, Image_H))
            Fill_Zoom = max(1.0, Cover_Scale / max(1e-9, Fit_Scale))
            Max_Zoom = max(1.0, float(min(Inner_W, Inner_H)) / max(1e-9, Fit_Scale))
            Zoom_Scale = max(1.0, min(Max_Zoom, Zoom_Scale))
            setattr(self, "_Zoom_Scale", Zoom_Scale)
            setattr(self, "ZoomScale", Zoom_Scale)
            Display_Scale = Fit_Scale * Zoom_Scale
            if Zoom_Scale <= Fill_Zoom + 1e-12:
                New_W = int(max(1, round(Image_W * Display_Scale)))
                New_H = int(max(1, round(Image_H * Display_Scale)))
                Center_Left = float(Padding + (Inner_W - New_W) * 0.5)
                Center_Top = float(Padding + (Inner_H - New_H) * 0.5)
                Allow_X = (New_W > Inner_W + 0.5)
                Allow_Y = (New_H > Inner_H + 0.5)
                Off = getattr(self, "_Zoom_Offset", None)
                if Off is None:
                    Left = Center_Left
                    Top = Center_Top
                else:
                    Left = float(Off[0])
                    Top = float(Off[1])
                if Allow_X:
                    Min_Left = float(Padding + Inner_W - New_W)
                    Max_Left = float(Padding)
                    Left = max(Min_Left, min(Max_Left, Left))
                else:
                    Left = Center_Left
                if Allow_Y:
                    Min_Top = float(Padding + Inner_H - New_H)
                    Max_Top = float(Padding)
                    Top = max(Min_Top, min(Max_Top, Top))
                else:
                    Top = Center_Top
                if Zoom_Scale <= 1.0 + 1e-12:
                    setattr(self, "_Zoom_Offset", None)
                else:
                    if Allow_X or Allow_Y:
                        setattr(self, "_Zoom_Offset", (Left, Top))
                    else:
                        setattr(self, "_Zoom_Offset", None)
                Crop = Image.convert("RGBA").resize((New_W, New_H), PILImage.NEAREST)
                Image_Tk = PILImageTk.PhotoImage(Crop)
                return {"Image": Image_Tk, "Top": int(round(Top)), "Left": int(round(Left)), "Crop_Left": 0.0, "Crop_Top": 0.0, "Crop_Right": float(Image_W), "Crop_Bottom": float(Image_H), "Scale": float(Display_Scale), "Pad": int(Padding), "Inner_W": int(Inner_W), "Inner_H": int(Inner_H), "Canvas_W": int(New_W), "Canvas_H": int(New_H)}
            Center = getattr(self, "_Zoom_Center", getattr(self, "ZoomCenter", None))
            if Center is None:
                Center = (Image_W * 0.5, Image_H * 0.5)
            Cx = float(Center[0])
            Cy = float(Center[1])
            View_W = float(Inner_W) / max(1e-9, Display_Scale)
            View_H = float(Inner_H) / max(1e-9, Display_Scale)
            View_W = max(1.0, min(Image_W, View_W))
            View_H = max(1.0, min(Image_H, View_H))
            HW = View_W * 0.5
            HH = View_H * 0.5
            Cx = max(HW, min(Image_W - HW, Cx))
            Cy = max(HH, min(Image_H - HH, Cy))
            setattr(self, "_Zoom_Center", (Cx, Cy))
            setattr(self, "ZoomCenter", (Cx, Cy))
            setattr(self, "_Zoom_Offset", None)
            Left_F = Cx - HW
            Top_F = Cy - HH
            Right_F = Left_F + View_W
            Bottom_F = Top_F + View_H
            Crop_Left = int(max(0, min(Image_W - 1, Left_F)))
            Crop_Top = int(max(0, min(Image_H - 1, Top_F)))
            Crop_Right = int(max(Crop_Left + 1, min(Image_W, Right_F)))
            Crop_Bottom = int(max(Crop_Top + 1, min(Image_H, Bottom_F)))
            Crop_W = float(Crop_Right - Crop_Left)
            Crop_H = float(Crop_Bottom - Crop_Top)
            if Crop_W <= 0 or Crop_H <= 0:
                return None
            Crop = Image.crop((Crop_Left, Crop_Top, Crop_Right, Crop_Bottom)).convert("RGBA")
            Crop = Crop.resize((Inner_W, Inner_H), PILImage.NEAREST)
            Image_Tk = PILImageTk.PhotoImage(Crop)
            Scale = float(Inner_W) / max(1e-9, Crop_W)
            return {"Image": Image_Tk, "Top": int(Padding), "Left": int(Padding), "Crop_Left": float(Crop_Left), "Crop_Top": float(Crop_Top), "Crop_Right": float(Crop_Right), "Crop_Bottom": float(Crop_Bottom), "Scale": float(Scale), "Pad": int(Padding), "Inner_W": int(Inner_W), "Inner_H": int(Inner_H), "Canvas_W": int(Inner_W), "Canvas_H": int(Inner_H)}
        except Exception as E:
            GUI = getattr(self, "_GUI", getattr(self, "GUI", None))
            Type = getattr(self, "_Type", getattr(self, "Type", "Viewport"))
            if GUI:
                GUI.Error(f"{Type} -> Convert -> {E}")
            return None

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
            Fill = self._Rect_Fill.get(ID, "")
            Transparent = self._Rect_Transparent.get(ID, False)
            Stipple = "gray25" if Transparent else ""
            if not Item:
                Item = self._Canvas._Frame.create_polygon(
                    *Screen,
                    outline=Color,
                    fill=Fill,
                    stipple=Stipple,
                    width=Width_Draw
                )
                self._Rectangles[ID] = (Cx, Cy, Width, Height, Angle, Thickness, Color, Item)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(
                    Item,
                    outline=Color,
                    fill=Fill,
                    stipple=Stipple,
                    width=Width_Draw,
                    state="normal"
                )
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
            if ID not in self._Circles or not self._Render_Info:
                return
            Cx, Cy, Radius, Thickness, Color, Item = self._Circles[ID]
            Fill = self._Circle_Fill.get(ID, "")
            Transparent = self._Circle_Transparent.get(ID, False)
            Mode = getattr(self, "_Circle_Render_Mode", "auto")
            UsePoly = True if Mode == "polygon" else (False if Mode == "oval" else bool(Transparent))
            Width_Draw = Thickness * (2 if self._Selected_Circle_ID == ID else 1)
            Stipple = ("gray25" if Transparent else "")
            if UsePoly:
                Steps = self._Circle_Steps_For_Radius(Radius)
                Unit = self._Circle_Unit_Points(Steps)
                Screen = []
                for Ux, Uy in Unit:
                    P = self.Image_To_Canvas(Cx + Radius * Ux, Cy + Radius * Uy)
                    if not P:
                        return
                    Screen.append(P[0])
                    Screen.append(P[1])
                if Item:
                    try:
                        if self._Canvas._Frame.type(Item) != "polygon":
                            self._Canvas.Delete_Item(Item)
                            Item = None
                    except:
                        pass
                if not Item:
                    Item = self._Canvas._Frame.create_polygon(Screen, outline=Color, fill=Fill, stipple=Stipple, width=Width_Draw, smooth=True)
                    self._Circles[ID] = (Cx, Cy, Radius, Thickness, Color, Item)
                else:
                    self._Canvas._Frame.coords(Item, Screen)
                    self._Canvas._Frame.itemconfigure(Item, outline=Color, fill=Fill, stipple=Stipple, width=Width_Draw, state="normal")
            else:
                P1 = self.Image_To_Canvas(Cx - Radius, Cy - Radius)
                P2 = self.Image_To_Canvas(Cx + Radius, Cy + Radius)
                if not P1 or not P2:
                    return
                if Item:
                    try:
                        if self._Canvas._Frame.type(Item) != "oval":
                            self._Canvas.Delete_Item(Item)
                            Item = None
                    except:
                        pass
                if not Item:
                    Item = self._Canvas._Frame.create_oval(P1[0], P1[1], P2[0], P2[1], outline=Color, fill=Fill, stipple=Stipple, width=Width_Draw)
                    self._Circles[ID] = (Cx, Cy, Radius, Thickness, Color, Item)
                else:
                    self._Canvas._Frame.coords(Item, P1[0], P1[1], P2[0], P2[1])
                    self._Canvas._Frame.itemconfigure(Item, outline=Color, fill=Fill, stipple=Stipple, width=Width_Draw, state="normal")
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
            Fill = self._Quad_Fill.get(ID, "")
            Transparent = self._Quad_Transparent.get(ID, False)
            Stipple = "gray25" if Transparent else ""
            if not Item:
                Item = self._Canvas._Frame.create_polygon(
                    *Screen,
                    outline=Color,
                    fill=Fill,
                    stipple=Stipple,
                    width=Width_Draw
                )
                self._Quadrilaterals[ID] = (P1, P2, P3, P4, Angle, Thickness, Color, Item)
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(
                    Item,
                    outline=Color,
                    fill=Fill,
                    stipple=Stipple,
                    width=Width_Draw,
                    state="normal"
                )
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
            if self._Callback_Mode == "Continuous":
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
            if self._Callback_Mode == "Continuous":
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
                    if self._Callback_Mode == "Continuous":
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
            if self._Callback_Mode == "Continuous":
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
            Fill = self._Polygon_Fill.get(ID, "")
            Transparent = self._Polygon_Transparent.get(ID, False)
            Stipple = "gray25" if Transparent else ""
            if not Item:
                Item = self._Canvas._Frame.create_polygon(
                    *Screen,
                    outline=Color,
                    fill=Fill,
                    stipple=Stipple,
                    width=Width_Draw
                )
            else:
                self._Canvas._Frame.coords(Item, *Screen)
                self._Canvas._Frame.itemconfigure(
                    Item,
                    outline=Color,
                    fill=Fill,
                    stipple=Stipple,
                    width=Width_Draw,
                    state="normal"
                )
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
            if self._Callback_Mode == "Continuous":
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
            if self._Callback_Mode == "Continuous":
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
                    if self._Callback_Mode == "Continuous":
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
            if self._Callback_Mode == "Continuous":
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

    def Add_Polygon(self, Points=None, Angle=0, Thickness=2, Color="#5499c7", Fill="", Transparent=True):
        try:
            if not hasattr(self, "_Polygons"):
                self._Polygons = {}
            if not hasattr(self, "_Polygon_Disabled"):
                self._Polygon_Disabled = {}
            if not hasattr(self, "_Polygon_ID_Next"):
                self._Polygon_ID_Next = 1
            if not hasattr(self, "_Polygon_Fill"):
                self._Polygon_Fill = {}
            if not hasattr(self, "_Polygon_Transparent"):
                self._Polygon_Transparent = {}
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            Image_W = float(getattr(self, "_Image_Width", 0) or 0)
            Image_H = float(getattr(self, "_Image_Height", 0) or 0)
            View_W = Image_W / max(1e-9, Zoom_Scale)
            View_H = Image_H / max(1e-9, Zoom_Scale)
            Center = getattr(self, "_Zoom_Center", None)
            if Center is not None:
                CenterX, CenterY = float(Center[0]), float(Center[1])
            else:
                CenterX, CenterY = float(Image_W) * 0.5, float(Image_H) * 0.5
            D = min(float(View_W), float(View_H)) * 0.20
            Default = [(CenterX, CenterY - D), (CenterX + D, CenterY + D), (CenterX - D, CenterY + D)]
            if Points is None:
                Points = Default
            if not isinstance(Points, (list, tuple)) or len(Points) < 3:
                return None
            PointsOut = [(float(P[0]), float(P[1])) for P in Points]
            ID = int(self._Polygon_ID_Next)
            self._Polygon_ID_Next += 1
            self._Polygons[ID] = (PointsOut, float(Angle), float(Thickness), str(Color), None, [])
            self._Polygon_Fill[ID] = str(Fill)
            self._Polygon_Transparent[ID] = bool(Transparent)
            self.Render()
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Polygon", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Polygon -> {E}")
            return None
            
    def Update_Polygon(self, ID=None, Points=None, Angle=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None):
        try:
            if not hasattr(self, "_Polygon_Disabled"):
                self._Polygon_Disabled = {}
            if not hasattr(self, "_Polygon_Fill"):
                self._Polygon_Fill = {}
            if not hasattr(self, "_Polygon_Transparent"):
                self._Polygon_Transparent = {}
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
            PointsOut = [(float(P[0]), float(P[1])) for P in Points]
            Angle = float(Angle) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(C0)
            self._Polygons[ID] = (PointsOut, Angle, Thickness, Color, Item0, Handles0)
            if Fill is not None:
                self._Polygon_Fill[ID] = str(Fill)
            if Transparent is not None:
                self._Polygon_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Polygon_Disabled[ID] = bool(Disabled)
            self.Polygon_Draw(ID)
            if self._Callback_Mode == "Continuous":
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
                    Out_List.append({"ID": Each_ID, "Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": self._Polygon_Fill.get(Each_ID, ""), "Transparent": self._Polygon_Transparent.get(EachID, False)})
                return Out_List
            if ID is None:
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return None
            Points, Angle, Thickness, Color, Item, Handles = self._Polygons[ID]
            return {"Points": [[float(X), float(Y)] for (X, Y) in Points], "Angle": Angle, "Thickness": Thickness, "Color": Color, "Fill": self._Polygon_Fill.get(ID, ""), "Transparent": self._Polygon_Transparent.get(ID, False)}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Polygon -> {E}")
            
    def Remove_Polygon(self, ID=None):
        try:
            if not self._Polygons:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for EachID, Data in list(self._Polygons.items()):
                    if self._Callback_Mode == "Continuous":
                        self._Callback_Invoke("Polygon", ID=EachID, Event="Remove")
                    Item = Data[4]
                    Handles = Data[5]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    self._Clear_Handles(Handles)
                    self._Polygon_Fill.pop(EachID, None)
                    self._Polygon_Transparent.pop(EachID, None)
                    self._Polygon_Disabled.pop(EachID, None)
                self._Polygons.clear()
                self._Selected_Polygon_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Polygons.keys())[0]
            if ID not in self._Polygons:
                return
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Polygon", ID=ID, Event="Remove")
            Item = self._Polygons[ID][4]
            Handles = self._Polygons[ID][5]
            if Item:
                self._Canvas.Delete_Item(Item)
            self._Clear_Handles(Handles)
            self._Polygon_Fill.pop(ID, None)
            self._Polygon_Transparent.pop(ID, None)
            self._Polygon_Disabled.pop(ID, None)
            del self._Polygons[ID]
            if self._Selected_Polygon_ID == ID:
                self._Selected_Polygon_ID = None
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove_Polygon -> {E}")

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
            self._Selected_Polyline_ID = ID
            self.Polyline_Draw(ID)
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Polyline", ID=ID, Event="Update")
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
            self._Selected_Polygon_ID = ID
            self.Polygon_Draw(ID)
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Polygon", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Insert_Point_In_Polygon -> {E}")

    def Add_Quadrilateral(self, P1=None, P2=None, P3=None, P4=None, Angle=0, Thickness=2, Color="#45b39d", Fill="", Transparent=True):
        try:
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            Image_W = float(getattr(self, "_Image_Width", 0) or 0)
            Image_H = float(getattr(self, "_Image_Height", 0) or 0)
            View_W = Image_W / max(1e-9, Zoom_Scale)
            View_H = Image_H / max(1e-9, Zoom_Scale)
            Center = getattr(self, "_Zoom_Center", None)
            if Center is not None:
                CenterX, CenterY = float(Center[0]), float(Center[1])
            else:
                CenterX, CenterY = float(Image_W) * 0.5, float(Image_H) * 0.5
            DefaultW = float(View_W) * 0.25
            DefaultH = float(View_H) * 0.25
            DefaultP1 = (CenterX - DefaultW * 0.5, CenterY - DefaultH * 0.5)
            DefaultP2 = (CenterX + DefaultW * 0.5, CenterY - DefaultH * 0.5)
            DefaultP3 = (CenterX + DefaultW * 0.5, CenterY + DefaultH * 0.5)
            DefaultP4 = (CenterX - DefaultW * 0.5, CenterY + DefaultH * 0.5)
            if P1 is None: P1 = DefaultP1
            if P2 is None: P2 = DefaultP2
            if P3 is None: P3 = DefaultP3
            if P4 is None: P4 = DefaultP4
            P1 = (float(P1[0]), float(P1[1]))
            P2 = (float(P2[0]), float(P2[1]))
            P3 = (float(P3[0]), float(P3[1]))
            P4 = (float(P4[0]), float(P4[1]))
            ID = int(self._Quad_ID_Next)
            self._Quad_ID_Next += 1
            self._Quadrilaterals[ID] = (P1, P2, P3, P4, float(Angle), float(Thickness), str(Color), None)
            self._Quad_Fill[ID] = str(Fill)
            self._Quad_Transparent[ID] = bool(Transparent)
            self.Render()
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Quadrilateral", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Quadrilateral -> {E}")
            return None
            
    def Update_Quadrilateral(self, ID=None, P1=None, P2=None, P3=None, P4=None, Angle=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None):
        try:
            if not hasattr(self, "_Quad_Disabled"):
                self._Quad_Disabled = {}
            if not hasattr(self, "_Quad_Fill"):
                self._Quad_Fill = {}
            if not hasattr(self, "_Quad_Transparent"):
                self._Quad_Transparent = {}
            if not self._Quadrilaterals:
                return
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            P10, P20, P30, P40, A0, T0, Col0, Item0 = self._Quadrilaterals[ID]
            if P1 is None: P1 = P10
            if P2 is None: P2 = P20
            if P3 is None: P3 = P30
            if P4 is None: P4 = P40
            P1 = (float(P1[0]), float(P1[1]))
            P2 = (float(P2[0]), float(P2[1]))
            P3 = (float(P3[0]), float(P3[1]))
            P4 = (float(P4[0]), float(P4[1]))
            Angle = float(Angle) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(Col0)
            self._Quadrilaterals[ID] = (P1, P2, P3, P4, Angle, Thickness, Color, Item0)
            if Fill is not None:
                self._Quad_Fill[ID] = str(Fill)
            if Transparent is not None:
                self._Quad_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Quad_Disabled[ID] = bool(Disabled)
            self.Quad_Draw(ID)
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Quadrilateral", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Quadrilateral -> {E}")
            
    def Get_Quadrilateral(self, ID=None):
        try:
            if not self._Quadrilaterals:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out = []
                for EachID in sorted(self._Quadrilaterals.keys()):
                    P1, P2, P3, P4, Angle, Thickness, Color, _ = self._Quadrilaterals[EachID]
                    Out.append({
                        "ID": EachID,
                        "P1": [float(P1[0]), float(P1[1])],
                        "P2": [float(P2[0]), float(P2[1])],
                        "P3": [float(P3[0]), float(P3[1])],
                        "P4": [float(P4[0]), float(P4[1])],
                        "Angle": Angle,
                        "Thickness": Thickness,
                        "Color": Color,
                        "Fill": self._Quad_Fill.get(EachID, ""),
                        "Transparent": self._Quad_Transparent.get(EachID, False),
                    })
                return Out
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return None
            P1, P2, P3, P4, Angle, Thickness, Color, _ = self._Quadrilaterals[ID]
            return {
                "P1": [float(P1[0]), float(P1[1])],
                "P2": [float(P2[0]), float(P2[1])],
                "P3": [float(P3[0]), float(P3[1])],
                "P4": [float(P4[0]), float(P4[1])],
                "Angle": Angle,
                "Thickness": Thickness,
                "Color": Color,
                "Fill": self._Quad_Fill.get(ID, ""),
                "Transparent": self._Quad_Transparent.get(ID, False),
            }
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Quadrilateral -> {E}")
            return None
            
    def Remove_Quadrilateral(self, ID=None):
        try:
            if not self._Quadrilaterals:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for EachID, Data in list(self._Quadrilaterals.items()):
                    if self._Callback_Mode == "Continuous":
                        self._Callback_Invoke("Quadrilateral", ID=EachID, Event="Remove")
                    Item = Data[7]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Quad_Handles"):
                        Handles = self._Quad_Handles.pop(EachID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                    self._Quad_Fill.pop(EachID, None)
                    self._Quad_Transparent.pop(EachID, None)
                    self._Quad_Disabled.pop(EachID, None)
                self._Quadrilaterals.clear()
                self._Selected_Quad_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Quadrilaterals.keys())[0]
            if ID not in self._Quadrilaterals:
                return
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Quadrilateral", ID=ID, Event="Remove")
            Item = self._Quadrilaterals[ID][7]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Quad_Handles"):
                Handles = self._Quad_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)
            self._Quad_Fill.pop(ID, None)
            self._Quad_Transparent.pop(ID, None)
            self._Quad_Disabled.pop(ID, None)
            del self._Quadrilaterals[ID]
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

    def Add_Rectangle(self, X=None, Y=None, Width=None, Height=None, Angle=0, Thickness=2, Color="#dc7633", Fill="", Transparent=True):
        try:
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            Image_W = float(getattr(self, "_Image_Width", 0) or 0)
            Image_H = float(getattr(self, "_Image_Height", 0) or 0)
            View_W = Image_W / max(1e-9, Zoom_Scale)
            View_H = Image_H / max(1e-9, Zoom_Scale)
            if X is None or Y is None:
                Center = getattr(self, "_Zoom_Center", None)
                if Center is not None:
                    X = float(Center[0])
                    Y = float(Center[1])
                else:
                    X = float(Image_W) * 0.5
                    Y = float(Image_H) * 0.5
            if Width is None:
                Width = float(View_W) * 0.2
            if Height is None:
                Height = float(View_H) * 0.2
            ID = int(self._Rect_ID_Next)
            self._Rect_ID_Next += 1
            self._Rectangles[ID] = (float(X), float(Y), float(Width), float(Height), float(Angle), float(Thickness), str(Color), None)
            self._Rect_Fill[ID] = str(Fill)
            self._Rect_Transparent[ID] = bool(Transparent)
            self.Render()
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Rectangle", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Rectangle -> {E}")
            return None
            
    def Update_Rectangle(self, ID=None, X=None, Y=None, Width=None, Height=None, Angle=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None, Disable_Rotation=None):
        try:
            if not hasattr(self, "_Rect_Disabled"):
                self._Rect_Disabled = {}
            if not hasattr(self, "_Rect_Disable_Rotation"):
                self._Rect_Disable_Rotation = {}
            if not hasattr(self, "_Rect_Fill"):
                self._Rect_Fill = {}
            if not hasattr(self, "_Rect_Transparent"):
                self._Rect_Transparent = {}
            if not self._Rectangles:
                return
            if ID is None:
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            C0x, C0y, W0, H0, A0, T0, Col0, Item0 = self._Rectangles[ID]
            X = float(X) if X is not None else float(C0x)
            Y = float(Y) if Y is not None else float(C0y)
            Width = float(max(2.0, Width)) if Width is not None else float(W0)
            Height = float(max(2.0, Height)) if Height is not None else float(H0)
            Angle = float(self.Normalize_Angle(Angle)) if Angle is not None else float(A0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(Col0)
            self._Rectangles[ID] = (X, Y, Width, Height, Angle, Thickness, Color, Item0)
            if Fill is not None:
                self._Rect_Fill[ID] = str(Fill)
            if Transparent is not None:
                self._Rect_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Rect_Disabled[ID] = bool(Disabled)
            if Disable_Rotation is not None:
                self._Rect_Disable_Rotation[ID] = bool(Disable_Rotation)
            self.Rect_Draw(ID)
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Rectangle", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Rectangle -> {E}")
            
    def Get_Rectangle(self, ID=None):
        try:
            if not self._Rectangles:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out = []
                for EachID in sorted(self._Rectangles.keys()):
                    X, Y, Width, Height, Angle, Thickness, Color, _ = self._Rectangles[EachID]
                    Out.append({
                        "ID": EachID,
                        "X": X, "Y": Y,
                        "Width": Width, "Height": Height,
                        "Angle": Angle,
                        "Thickness": Thickness,
                        "Color": Color,
                        "Fill": self._Rect_Fill.get(EachID, ""),
                        "Transparent": self._Rect_Transparent.get(EachID, False),
                    })
                return Out
            if ID is None:
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return None
            X, Y, Width, Height, Angle, Thickness, Color, _ = self._Rectangles[ID]
            return {
                "X": X, "Y": Y,
                "Width": Width, "Height": Height,
                "Angle": Angle,
                "Thickness": Thickness,
                "Color": Color,
                "Fill": self._Rect_Fill.get(ID, ""),
                "Transparent": self._Rect_Transparent.get(ID, False),
            }
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Rectangle -> {E}")
            return None
            
    def Remove_Rectangle(self, ID=None):
        try:
            if not self._Rectangles:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for EachID, Data in list(self._Rectangles.items()):
                    if self._Callback_Mode == "Continuous":
                        self._Callback_Invoke("Rectangle", ID=EachID, Event="Remove")
                    Item = Data[7]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Rect_Handles"):
                        Handles = self._Rect_Handles.pop(EachID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                    self._Rect_Fill.pop(EachID, None)
                    self._Rect_Transparent.pop(EachID, None)
                    self._Rect_Disabled.pop(EachID, None)
                    self._Rect_Disable_Rotation.pop(EachID, None)
                self._Rectangles.clear()
                self._Selected_Rect_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Rectangles.keys())[0]
            if ID not in self._Rectangles:
                return
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Rectangle", ID=ID, Event="Remove")
            Item = self._Rectangles[ID][7]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Rect_Handles"):
                Handles = self._Rect_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)
            self._Rect_Fill.pop(ID, None)
            self._Rect_Transparent.pop(ID, None)
            self._Rect_Disabled.pop(ID, None)
            self._Rect_Disable_Rotation.pop(ID, None)
            del self._Rectangles[ID]
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

    def Add_Circle(self, X=None, Y=None, Radius=None, Thickness=2, Color="#a569bd", Fill="", Transparent=True):
        try:
            if not self._Image:
                return None
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", 1.0) or 1.0)
            Image_W = float(getattr(self, "_Image_Width", 0) or 0)
            Image_H = float(getattr(self, "_Image_Height", 0) or 0)
            View_W = Image_W / max(1e-9, Zoom_Scale)
            View_H = Image_H / max(1e-9, Zoom_Scale)
            if X is None or Y is None:
                Center = getattr(self, "_Zoom_Center", None)
                if Center is not None:
                    X = float(Center[0])
                    Y = float(Center[1])
                else:
                    X = float(Image_W) * 0.5
                    Y = float(Image_H) * 0.5
            if Radius is None:
                Radius = min(float(View_W), float(View_H)) * 0.1
            ID = int(self._Circle_ID_Next)
            self._Circle_ID_Next += 1
            self._Circles[ID] = (float(X), float(Y), float(Radius), float(Thickness), str(Color), None)
            self._Circle_Fill[ID] = str(Fill)
            self._Circle_Transparent[ID] = bool(Transparent)
            self.Render()
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Circle", ID=ID, Event="Add")
            return ID
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add_Circle -> {E}")
            return None
            
    def Update_Circle(self, ID=None, X=None, Y=None, Radius=None, Thickness=None, Color=None, Fill=None, Transparent=None, Disabled=None):
        try:
            if not hasattr(self, "_Circle_Disabled"):
                self._Circle_Disabled = {}
            if not hasattr(self, "_Circle_Fill"):
                self._Circle_Fill = {}
            if not hasattr(self, "_Circle_Transparent"):
                self._Circle_Transparent = {}
            if not self._Circles:
                return
            if ID is None:
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            C0x, C0y, R0, T0, Col0, Item0 = self._Circles[ID]
            X = float(X) if X is not None else float(C0x)
            Y = float(Y) if Y is not None else float(C0y)
            Radius = float(max(1.0, Radius)) if Radius is not None else float(R0)
            Thickness = float(Thickness) if Thickness is not None else float(T0)
            Color = str(Color) if Color is not None else str(Col0)
            self._Circles[ID] = (X, Y, Radius, Thickness, Color, Item0)
            if Fill is not None:
                self._Circle_Fill[ID] = str(Fill)
            if Transparent is not None:
                self._Circle_Transparent[ID] = bool(Transparent)
            if Disabled is not None:
                self._Circle_Disabled[ID] = bool(Disabled)
            self.Circle_Draw(ID)
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Circle", ID=ID, Event="Update")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Circle -> {E}")
            
    def Get_Circle(self, ID=None):
        try:
            if not self._Circles:
                return None
            if isinstance(ID, str) and ID.lower() == "all":
                Out = []
                for EachID in sorted(self._Circles.keys()):
                    X, Y, Radius, Thickness, Color, _ = self._Circles[EachID]
                    Out.append({
                        "ID": EachID,
                        "X": X, "Y": Y,
                        "Radius": Radius,
                        "Thickness": Thickness,
                        "Color": Color,
                        "Fill": self._Circle_Fill.get(EachID, ""),
                        "Transparent": self._Circle_Transparent.get(EachID, False),
                    })
                return Out
            if ID is None:
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return None
            X, Y, Radius, Thickness, Color, _ = self._Circles[ID]
            return {
                "X": X, "Y": Y,
                "Radius": Radius,
                "Thickness": Thickness,
                "Color": Color,
                "Fill": self._Circle_Fill.get(ID, ""),
                "Transparent": self._Circle_Transparent.get(ID, False),
            }
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get_Circle -> {E}")
            return None
            
    def Remove_Circle(self, ID=None):
        try:
            if not self._Circles:
                return
            if isinstance(ID, str) and ID.lower() == "all":
                for EachID, Data in list(self._Circles.items()):
                    if self._Callback_Mode == "Continuous":
                        self._Callback_Invoke("Circle", ID=EachID, Event="Remove")
                    Item = Data[5]
                    if Item:
                        self._Canvas.Delete_Item(Item)
                    if hasattr(self, "_Circle_Handles"):
                        Handles = self._Circle_Handles.pop(EachID, None)
                        if Handles:
                            self._Clear_Handles(Handles)
                    self._Circle_Fill.pop(EachID, None)
                    self._Circle_Transparent.pop(EachID, None)
                    self._Circle_Disabled.pop(EachID, None)
                self._Circles.clear()
                self._Selected_Circle_ID = None
                self.Render()
                return
            if ID is None:
                ID = sorted(self._Circles.keys())[0]
            if ID not in self._Circles:
                return
            if self._Callback_Mode == "Continuous":
                self._Callback_Invoke("Circle", ID=ID, Event="Remove")
            Item = self._Circles[ID][5]
            if Item:
                self._Canvas.Delete_Item(Item)
            if hasattr(self, "_Circle_Handles"):
                Handles = self._Circle_Handles.pop(ID, None)
                if Handles:
                    self._Clear_Handles(Handles)
            self._Circle_Fill.pop(ID, None)
            self._Circle_Transparent.pop(ID, None)
            self._Circle_Disabled.pop(ID, None)
            del self._Circles[ID]
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
            for _, Data in list(self._Polygons.items()):
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
            self._Rect_Fill.clear()
            self._Rect_Transparent.clear()
            self._Circle_Fill.clear()
            self._Circle_Transparent.clear()
            self._Quad_Fill.clear()
            self._Quad_Transparent.clear()
            self._Polygon_Fill.clear()
            self._Polygon_Transparent.clear()
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
            if hasattr(self, "_Circle_Handles"):
                for _, Handles in list(self._Circle_Handles.items()):
                    self._Clear_Handles(Handles)
                self._Circle_Handles.clear()
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Render(self):
        try:
            if not self._Image:
                return
            Box_Obj = getattr(self._Canvas, "Box", None)
            if callable(Box_Obj):
                FX, FY, FW, FH = Box_Obj()
            else:
                FX, FY, FW, FH = Box_Obj
            if FW <= 0 or FH <= 0:
                return
            Out = self.Convert(FW, FH)
            if not Out:
                return
            self._Render_Info = {"Left": Out["Left"], "Top": Out["Top"], "Scale": Out["Scale"], "Crop_Left": Out["Crop_Left"], "Crop_Top": Out["Crop_Top"], "Crop_Right": Out["Crop_Right"], "Crop_Bottom": Out["Crop_Bottom"], "Canvas_W": Out["Canvas_W"], "Canvas_H": Out["Canvas_H"]}
            Frame = getattr(self._Canvas, "Frame", None) or getattr(self._Canvas, "_Frame", None) or self._Canvas
            Create_Image = getattr(Frame, "createimage", None) or getattr(Frame, "create_image", None)
            Item_Config = getattr(Frame, "itemconfig", None) or getattr(Frame, "itemconfigure", None)
            Coords = getattr(Frame, "coords", None)
            Tag_Raise = getattr(Frame, "tagraise", None) or getattr(Frame, "tag_raise", None)
            Item_Configure = getattr(Frame, "itemconfigure", None) or getattr(Frame, "itemconfig", None)
            if not self._Image_Window:
                self._Image_Window = Create_Image(Out["Left"], Out["Top"], image=Out["Image"], anchor="nw")
                setattr(Frame, "Temp_Image", Out["Image"])
            else:
                Item_Config(self._Image_Window, image=Out["Image"])
                Coords(self._Image_Window, Out["Left"], Out["Top"])
                setattr(Frame, "Temp_Image", Out["Image"])
            Item_Configure(self._Image_Window, state="normal")
            Tag_Raise(self._Image_Window)
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

    def Motion(self, Event):
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
            self._GUI.Error(f"{self._Type} -> Motion -> {E}")

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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
                    self._Callback_Invoke("Circle", ID=self._Selected_Circle_ID, Event="Update")
                return

            if self._Drag_Mode == "circle_resize" and self._Resize_Info and self._Render_Info and not getattr(self, "_Circle_Disabled", {}).get(self._Resize_Info["ID"], False):
                ID = self._Resize_Info["ID"]
                Cx0, Cy0 = self._Resize_Info["Init_Center"]
                P = self.Canvas_To_Image(CX, CY)
                if not P:
                    return
                Dist_Current = math.hypot(P[0] - Cx0, P[1] - Cy0)
                New_R = max(1.0, Dist_Current)
                self.Update_Circle(ID=ID, X=Cx0, Y=Cy0, Radius=New_R)
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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
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
                if self._Callback_Mode == "Continuous":
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

            Zoom_Scale = float(getattr(self, "_Zoom_Scale", getattr(self, "ZoomScale", 1.0)) or 1.0)
            ImageW = float(getattr(self, "_Image_Width", 0) or getattr(self, "ImageWidth", 0) or 0)
            ImageH = float(getattr(self, "_Image_Height", 0) or getattr(self, "ImageHeight", 0) or 0)
            if Zoom_Scale <= 1.0 + 1e-12:
                setattr(self, "_Zoom_Offset", None)
                C0 = (ImageW * 0.5, ImageH * 0.5)
                setattr(self, "_Zoom_Center", C0)
                setattr(self, "ZoomCenter", C0)
                self.Render()
                return
            RenderInfo = getattr(self, "_Render_Info", getattr(self, "RenderInfo", None))
            if not RenderInfo:
                self.Render()
                return
            CanvasObj = getattr(self, "_Canvas", None) if getattr(self, "_Canvas", None) is not None else getattr(self, "Canvas", None)
            Box_Obj = getattr(CanvasObj, "Box", None)
            if callable(Box_Obj):
                FX, FY, FW, FH = Box_Obj()
            else:
                FX, FY, FW, FH = Box_Obj
            Pad = int(self.Inner_Padding()) if hasattr(self, "Inner_Padding") else int(self.InnerPadding())
            InnerW = max(1, int(FW) - 2 * Pad)
            InnerH = max(1, int(FH) - 2 * Pad)
            CW = float(RenderInfo.get("Canvas_W", RenderInfo.get("CanvasW", 0)) or 0)
            CH = float(RenderInfo.get("Canvas_H", RenderInfo.get("CanvasH", 0)) or 0)
            Allow_X = (CW > float(InnerW) + 0.5)
            Allow_Y = (CH > float(InnerH) + 0.5)
            if Allow_X or Allow_Y:
                Off = getattr(self, "_Zoom_Offset", None)
                if Off is None:
                    Left = float(RenderInfo.get("Left", 0))
                    Top = float(RenderInfo.get("Top", 0))
                else:
                    Left = float(Off[0])
                    Top = float(Off[1])
                Left = Left + float(DX)
                Top = Top + float(DY)
                Center_Left = float(Pad + (InnerW - CW) * 0.5)
                Center_Top = float(Pad + (InnerH - CH) * 0.5)
                if Allow_X:
                    Min_Left = float(Pad + InnerW - CW)
                    Max_Left = float(Pad)
                    Left = max(Min_Left, min(Max_Left, Left))
                else:
                    Left = Center_Left
                if Allow_Y:
                    Min_Top = float(Pad + InnerH - CH)
                    Max_Top = float(Pad)
                    Top = max(Min_Top, min(Max_Top, Top))
                else:
                    Top = Center_Top
                setattr(self, "_Zoom_Offset", (Left, Top))
                self.Render()
                return
            S = float(RenderInfo.get("Scale", 1.0) or 1.0)
            ViewW = float(InnerW) / max(1e-9, S)
            ViewH = float(InnerH) / max(1e-9, S)
            Center = getattr(self, "_Zoom_Center", getattr(self, "ZoomCenter", None))
            if Center is None:
                Center = (ImageW * 0.5, ImageH * 0.5)
            NCX = float(Center[0]) - float(DX) / max(1e-9, S)
            NCY = float(Center[1]) - float(DY) / max(1e-9, S)
            HW = ViewW * 0.5
            HH = ViewH * 0.5
            NCX = max(HW, min(ImageW - HW, NCX))
            NCY = max(HH, min(ImageH - HH, NCY))
            setattr(self, "_Zoom_Center", (NCX, NCY))
            setattr(self, "ZoomCenter", (NCX, NCY))
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
            elif self._Drag_Mode != "image":
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
            elif self._Drag_Mode != "image":
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
            Image = getattr(self, "_Image", None) if getattr(self, "_Image", None) is not None else getattr(self, "Image", None)
            ImageWindow = getattr(self, "_Image_Window", getattr(self, "ImageWindow", None))
            if not Image or not ImageWindow:
                return
            CanvasObj = getattr(self, "_Canvas", None) if getattr(self, "_Canvas", None) is not None else getattr(self, "Canvas", None)
            Box_Obj = getattr(CanvasObj, "Box", None)
            if callable(Box_Obj):
                FX, FY, FW, FH = Box_Obj()
            else:
                FX, FY, FW, FH = Box_Obj
            Padding = int(self.Inner_Padding()) if hasattr(self, "Inner_Padding") else int(self.InnerPadding())
            Inner_W = max(1, int(FW) - 2 * Padding)
            Inner_H = max(1, int(FH) - 2 * Padding)
            Image_W = float(getattr(self, "_Image_Width", 0) or getattr(self, "ImageWidth", 0) or 0)
            Image_H = float(getattr(self, "_Image_Height", 0) or getattr(self, "ImageHeight", 0) or 0)
            if Image_W <= 1 or Image_H <= 1:
                return
            Zoom_Scale = float(getattr(self, "_Zoom_Scale", getattr(self, "ZoomScale", 1.0)) or 1.0)
            Fit_Scale = min(float(Inner_W) / max(1e-9, Image_W), float(Inner_H) / max(1e-9, Image_H))
            Cover_Scale = max(float(Inner_W) / max(1e-9, Image_W), float(Inner_H) / max(1e-9, Image_H))
            Fill_Zoom = max(1.0, Cover_Scale / max(1e-9, Fit_Scale))
            Max_Zoom = max(1.0, float(min(Inner_W, Inner_H)) / max(1e-9, Fit_Scale))
            Delta = getattr(Event, "delta", 0) or 0
            ZF = 1.1 if Delta > 0 else 0.9
            New_Zoom = max(1.0, min(Max_Zoom, Zoom_Scale * ZF))
            if abs(New_Zoom - Zoom_Scale) <= 1e-12:
                return
            Frame = getattr(Event, "widget", None)
            if Frame is None or not hasattr(Frame, "canvasx"):
                Frame = getattr(CanvasObj, "Frame", None) or getattr(CanvasObj, "_Frame", None) or CanvasObj
            if Frame is not None and hasattr(Frame, "canvasx"):
                CX = Frame.canvasx(getattr(Event, "x", 0))
                CY = Frame.canvasy(getattr(Event, "y", 0))
            else:
                CX = float(getattr(Event, "x", 0))
                CY = float(getattr(Event, "y", 0))
            Canvas_To_Image = getattr(self, "Canvas_To_Image", getattr(self, "CanvasToImage", None))
            IXY = Canvas_To_Image(CX, CY) if Canvas_To_Image else None
            if IXY:
                MX, MY = float(IXY[0]), float(IXY[1])
            else:
                Center = getattr(self, "_Zoom_Center", getattr(self, "ZoomCenter", None))
                if Center is None:
                    Center = (Image_W * 0.5, Image_H * 0.5)
                MX, MY = float(Center[0]), float(Center[1])
            RenderInfo = getattr(self, "_Render_Info", getattr(self, "RenderInfo", None))
            if RenderInfo:
                CL = float(RenderInfo.get("Crop_Left", RenderInfo.get("CropLeft", 0.0)))
                CT = float(RenderInfo.get("Crop_Top", RenderInfo.get("CropTop", 0.0)))
                CR = float(RenderInfo.get("Crop_Right", RenderInfo.get("CropRight", Image_W)))
                CB = float(RenderInfo.get("Crop_Bottom", RenderInfo.get("CropBottom", Image_H)))
                CW = max(1e-9, CR - CL)
                CH = max(1e-9, CB - CT)
                RX = max(0.0, min(1.0, (MX - CL) / CW))
                RY = max(0.0, min(1.0, (MY - CT) / CH))
            else:
                RX, RY = 0.5, 0.5
            setattr(self, "_Zoom_Scale", New_Zoom)
            setattr(self, "ZoomScale", New_Zoom)
            if New_Zoom <= 1.0 + 1e-12:
                setattr(self, "_Zoom_Offset", None)
                Center0 = (Image_W * 0.5, Image_H * 0.5)
                setattr(self, "_Zoom_Center", Center0)
                setattr(self, "ZoomCenter", Center0)
                self.Render()
                return
            New_Display_Scale = Fit_Scale * New_Zoom
            if New_Zoom <= Fill_Zoom + 1e-12:
                New_W = int(max(1, round(Image_W * New_Display_Scale)))
                New_H = int(max(1, round(Image_H * New_Display_Scale)))
                Min_Left = float(Padding)
                Min_Top = float(Padding)
                Max_Left = float(Padding + Inner_W - New_W)
                Max_Top = float(Padding + Inner_H - New_H)
                Left = float(CX) - float(MX) * New_Display_Scale
                Top = float(CY) - float(MY) * New_Display_Scale
                if Max_Left >= Min_Left:
                    Left = max(Min_Left, min(Max_Left, Left))
                else:
                    Left = float(Padding + (Inner_W - New_W) * 0.5)
                if Max_Top >= Min_Top:
                    Top = max(Min_Top, min(Max_Top, Top))
                else:
                    Top = float(Padding + (Inner_H - New_H) * 0.5)
                setattr(self, "_Zoom_Offset", (Left, Top))
                self.Render()
                return
            setattr(self, "_Zoom_Offset", None)
            View_W = float(Inner_W) / max(1e-9, New_Display_Scale)
            View_H = float(Inner_H) / max(1e-9, New_Display_Scale)
            View_W = max(1.0, min(Image_W, View_W))
            View_H = max(1.0, min(Image_H, View_H))
            New_Left = MX - RX * View_W
            New_Top = MY - RY * View_H
            NCX = New_Left + View_W * 0.5
            NCY = New_Top + View_H * 0.5
            HW = View_W * 0.5
            HH = View_H * 0.5
            NCX = max(HW, min(Image_W - HW, NCX))
            NCY = max(HH, min(Image_H - HH, NCY))
            setattr(self, "_Zoom_Center", (NCX, NCY))
            setattr(self, "ZoomCenter", (NCX, NCY))
            self.Render()
        except Exception as E:
            GUI = getattr(self, "_GUI", getattr(self, "GUI", None))
            Type = getattr(self, "_Type", getattr(self, "Type", "Viewport"))
            if GUI:
                GUI.Error(f"{Type} -> Zoom -> {E}")

    def Reset(self, Event=False):
        try:
            Image_W = float(getattr(self, "_Image_Width", 0) or getattr(self, "ImageWidth", 0) or 0)
            Image_H = float(getattr(self, "_Image_Height", 0) or getattr(self, "ImageHeight", 0) or 0)
            setattr(self, "_Zoom_Scale", 1.0)
            setattr(self, "ZoomScale", 1.0)
            if Image_W > 0 and Image_H > 0:
                Center = (Image_W * 0.5, Image_H * 0.5)
                setattr(self, "_Zoom_Center", Center)
                setattr(self, "ZoomCenter", Center)
            setattr(self, "_Zoom_Offset", None)
            self.Render()
        except Exception as E:
            GUI = getattr(self, "_GUI", getattr(self, "GUI", None))
            Type = getattr(self, "_Type", getattr(self, "Type", "Viewport"))
            if GUI:
                GUI.Error(f"{Type} -> Reset -> {E}")

    def Resize(self, Event):
        try:
            self.Render()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
import os
import time
import threading
try:
    import cv2
except Exception:
    cv2 = None
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
from .N_GUI import GUI

PIL_Image.MAX_IMAGE_PIXELS = None

class Video:

    def __init__(self, Frame, *Args, **Kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Video"
            try:
                self._Frame = Frame
                self._Canvas = None
                self._Canvas_Widget = None
                self._Image_Window = None
                self._Temp_Image = None
                self._Path = False
                self._Path_Memory = False
                self._Pause = True
                self._Loop = False
                self._Rate = 1.0
                self._Queue = []
                self._Capture = None
                self._Fps = 0.0
                self._Frame_Count = 0
                self._Duration_Ms = 0
                self._Stop_Time_Ms = None
                self._Last_Frame_Bgr = None
                self._Target_Size = None
                self._Decode_Thread = None
                self._Decode_Stop = threading.Event()
                self._Decode_Wake = threading.Event()
                self._Capture_Lock = threading.RLock()
                self._Frame_Lock = threading.RLock()
                self._Pending_Frame_Bgr = None
                self._Render_Pending = False
                self._CV2_Available = cv2 is not None
                self._Bind_Window()
                self._Bind_Events()
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Video[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Video[]"

    def Close(self):
        try:
            self._Pause = True
            self._Decode_Stop_All()
            self._Capture_Close()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Close -> {E}")

    def __del__(self):
        try:
            self.Close()
        except:
            pass

    def Delete(self):
        try:
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def _After(self, Delay_Ms, Func):
        try:
            W = self._Canvas_Widget
            if W is not None and hasattr(W, "after"):
                return W.after(int(Delay_Ms), Func)
            F = self._Frame
            if F is not None and hasattr(F, "after"):
                return F.after(int(Delay_Ms), Func)
            if F is not None and hasattr(F, "_Frame") and hasattr(F._Frame, "after"):
                return F._Frame.after(int(Delay_Ms), Func)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _After -> {E}")

    def _Bind_Window(self):
        try:
            F = self._Frame
            if hasattr(F, "_Frame") and hasattr(F._Frame, "create_image") and hasattr(F._Frame, "itemconfig"):
                self._Canvas = F
                self._Canvas_Widget = F._Frame
                return
            if hasattr(F, "create_image") and hasattr(F, "itemconfig"):
                self._Canvas = None
                self._Canvas_Widget = F
                return
            self._Canvas = None
            self._Canvas_Widget = getattr(F, "_Frame", None)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Bind_Window -> {E}")

    def _Bind_Events(self):
        try:
            if hasattr(self._Frame, "Bind"):
                try:
                    self._Frame.Bind(On_Resize=self.Resize)
                except Exception:
                    pass
            W = self._Canvas_Widget
            if W is not None and hasattr(W, "bind"):
                try:
                    W.bind("<Configure>", lambda E: self.Resize(E))
                except Exception:
                    pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Bind_Events -> {E}")

    def Widget(self):
        try:
            return self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")

    def _Canvas_Box(self):
        try:
            if self._Canvas is not None and hasattr(self._Canvas, "Box"):
                FX, FY, FW, FH = self._Canvas.Box()
                return float(FW), float(FH)
            W = self._Canvas_Widget
            if W is not None and hasattr(W, "winfo_width") and hasattr(W, "winfo_height"):
                return float(W.winfo_width()), float(W.winfo_height())
            return 0.0, 0.0
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Canvas_Box -> {E}")
            return 0.0, 0.0

    def _Ensure_Image_Window(self):
        try:
            W = self._Canvas_Widget
            if W is None:
                return False
            if self._Image_Window is None:
                try:
                    self._Image_Window = W.create_image(0, 0, image=None, anchor="nw")
                except Exception:
                    return False
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Ensure_Image_Window -> {E}")
            return False

    def _Compute_Draw_Rect(self, Img_W, Img_H, Canvas_W, Canvas_H):
        if Canvas_W <= 1 or Canvas_H <= 1 or Img_W <= 1 or Img_H <= 1:
            return 0, 0, 1, 1
        IA = float(Img_W) / float(Img_H)
        CA = float(Canvas_W) / float(Canvas_H)
        if IA > CA:
            DW = int(Canvas_W)
            DH = int(Canvas_W / max(1e-9, IA))
        else:
            DH = int(Canvas_H)
            DW = int(Canvas_H * IA)
        L = int((Canvas_W - DW) * 0.5)
        T = int((Canvas_H - DH) * 0.5)
        return L, T, DW, DH

    def _Render_Frame_Main(self):
        try:
            self._Render_Pending = False
            W = self._Canvas_Widget
            if W is None:
                return
            if not self._Ensure_Image_Window():
                return
            with self._Frame_Lock:
                Frame_Bgr = self._Pending_Frame_Bgr
                self._Pending_Frame_Bgr = None
            if Frame_Bgr is None:
                return
            self._Last_Frame_Bgr = Frame_Bgr
            Canvas_W, Canvas_H = self._Canvas_Box()
            Canvas_W = int(max(1, Canvas_W))
            Canvas_H = int(max(1, Canvas_H))
            H, W0 = Frame_Bgr.shape[:2]
            L, T, DW, DH = self._Compute_Draw_Rect(W0, H, Canvas_W, Canvas_H)
            Frame_Rgb = cv2.cvtColor(Frame_Bgr, cv2.COLOR_BGR2RGB) if self._CV2_Available else Frame_Bgr
            Pil = PIL_Image.fromarray(Frame_Rgb)
            if DW > 1 and DH > 1:
                Pil = Pil.resize((int(DW), int(DH)), PIL_Image.NEAREST)
            Tk = PIL_ImageTk.PhotoImage(Pil)
            self._Temp_Image = Tk
            try:
                W.itemconfig(self._Image_Window, image=Tk)
            except Exception:
                try:
                    W.itemconfigure(self._Image_Window, image=Tk)
                except Exception:
                    return
            try:
                W.coords(self._Image_Window, int(L), int(T))
            except Exception:
                pass
            try:
                W.tag_raise(self._Image_Window)
            except Exception:
                pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Render_Frame_Main -> {E}")

    def _Schedule_Render(self, Frame_Bgr):
        try:
            with self._Frame_Lock:
                self._Pending_Frame_Bgr = Frame_Bgr
            if self._Render_Pending:
                return
            self._Render_Pending = True
            self._After(0, self._Render_Frame_Main)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Schedule_Render -> {E}")

    def _Capture_Open(self, Source):
        try:
            if not self._CV2_Available:
                raise Exception("cv2 not found")
            Cap = cv2.VideoCapture(Source)
            if not Cap or not Cap.isOpened():
                return None
            return Cap
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Capture_Open -> {E}")
            return None

    def _Capture_Close(self):
        try:
            with self._Capture_Lock:
                if self._Capture is not None:
                    try:
                        self._Capture.release()
                    except Exception:
                        pass
                self._Capture = None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Capture_Close -> {E}")

    def _Capture_Refresh_Info(self):
        try:
            with self._Capture_Lock:
                Cap = self._Capture
                if Cap is None:
                    self._Fps = 0.0
                    self._Frame_Count = 0
                    self._Duration_Ms = 0
                    return
                Fps = float(Cap.get(getattr(cv2, "CAP_PROP_FPS", 5)) or 0.0)
                Cnt = int(Cap.get(getattr(cv2, "CAP_PROP_FRAME_COUNT", 7)) or 0)
                if Fps <= 1e-6:
                    Fps = 30.0
                Dur = 0
                if Cnt > 0 and Fps > 1e-9:
                    Dur = int((Cnt / Fps) * 1000.0)
                self._Fps = float(Fps)
                self._Frame_Count = int(Cnt)
                self._Duration_Ms = int(Dur)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Capture_Refresh_Info -> {E}")

    def _Capture_Time_Get_Ms(self):
        try:
            with self._Capture_Lock:
                if self._Capture is None:
                    return 0
                V = self._Capture.get(getattr(cv2, "CAP_PROP_POS_MSEC", 0))
                return int(V or 0)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Capture_Time_Get_Ms -> {E}")
            return 0

    def _Capture_Time_Set_Ms(self, Value):
        try:
            with self._Capture_Lock:
                if self._Capture is None:
                    return False
                return bool(self._Capture.set(getattr(cv2, "CAP_PROP_POS_MSEC", 0), float(Value)))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Capture_Time_Set_Ms -> {E}")
            return False

    def _Capture_Pos_Get(self):
        try:
            with self._Capture_Lock:
                if self._Capture is None:
                    return 0.0
                Cnt = int(self._Frame_Count or 0)
                if Cnt <= 0:
                    F = float(self._Capture.get(getattr(cv2, "CAP_PROP_POS_MSEC", 0)) or 0.0)
                    D = float(self._Duration_Ms or 0.0)
                    return float(F / max(1e-9, D)) if D > 0 else 0.0
                Cur = float(self._Capture.get(getattr(cv2, "CAP_PROP_POS_FRAMES", 1)) or 0.0)
                return float(Cur / max(1.0, float(Cnt)))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Capture_Pos_Get -> {E}")
            return 0.0

    def _Capture_Pos_Set(self, Value):
        try:
            V = float(Value)
            V = max(0.0, min(1.0, V))
            with self._Capture_Lock:
                if self._Capture is None:
                    return False
                Cnt = int(self._Frame_Count or 0)
                if Cnt > 0:
                    Target = int(V * float(Cnt))
                    return bool(self._Capture.set(getattr(cv2, "CAP_PROP_POS_FRAMES", 1), float(Target)))
                D = int(self._Duration_Ms or 0)
                if D > 0:
                    return bool(self._Capture.set(getattr(cv2, "CAP_PROP_POS_MSEC", 0), float(V * D)))
                return False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Capture_Pos_Set -> {E}")
            return False

    def _Decode_Loop(self):
        try:
            Last_T = time.time()
            while not self._Decode_Stop.is_set():
                if self._Pause:
                    self._Decode_Wake.wait(0.05)
                    continue
                with self._Capture_Lock:
                    Cap = self._Capture
                if Cap is None:
                    time.sleep(0.02)
                    continue
                Fps = float(self._Fps or 30.0)
                Rate = float(self._Rate or 1.0)
                Step_S = (1.0 / max(1e-9, Fps)) / max(1e-9, Rate)
                Now = time.time()
                Dt = Now - Last_T
                if Dt < Step_S:
                    time.sleep(min(0.01, Step_S - Dt))
                    continue
                Last_T = Now
                Ok = False
                Frame = None
                with self._Capture_Lock:
                    if self._Capture is None:
                        continue
                    Ok, Frame = self._Capture.read()
                if not Ok or Frame is None:
                    if self._Loop:
                        self.Position_Set(0.0)
                        continue
                    self._Pause = True
                    self.Play_Next()
                    continue
                if self._Stop_Time_Ms is not None:
                    Cur_Ms = self._Capture_Time_Get_Ms()
                    if Cur_Ms >= int(self._Stop_Time_Ms):
                        if self._Loop:
                            self.Time_Set(0)
                            continue
                        self._Pause = True
                        self.Play_Next()
                        continue
                self._Schedule_Render(Frame)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Decode_Loop -> {E}")

    def _Decode_Start(self):
        try:
            if self._Decode_Thread is not None and self._Decode_Thread.is_alive():
                return
            self._Decode_Stop.clear()
            self._Decode_Wake.set()
            self._Decode_Thread = threading.Thread(target=self._Decode_Loop, daemon=True)
            self._Decode_Thread.start()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Decode_Start -> {E}")

    def _Decode_Stop_All(self):
        try:
            self._Decode_Stop.set()
            self._Decode_Wake.set()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Decode_Stop_All -> {E}")

    def Set(self, Path=''):
        try:
            if not self._CV2_Available:
                raise Exception("cv2 not found")
            if Path:
                self._Path = Path
                if self._Path != self._Path_Memory:
                    self._Path_Memory = self._Path
                    self.Open()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")

    def Open(self):
        try:
            if not self._CV2_Available:
                raise Exception("cv2 not found")
            if not self._Path:
                return
            self.Stop()
            Src = self._Path
            if isinstance(Src, str):
                if Src.isdigit():
                    Src = int(Src)
            Cap = self._Capture_Open(Src)
            if Cap is None:
                self._GUI.Error(f"{self._Type} -> Open -> Could not open: {self._Path}")
                return
            with self._Capture_Lock:
                self._Capture = Cap
            self._Stop_Time_Ms = None
            self._Capture_Refresh_Info()
            self._Decode_Start()
            self._Prime_Frame()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")

    def Open_With(self, Path, Start=0, Stop=None, Cache_Ms=300, Hw=True):
        try:
            if not self._CV2_Available:
                raise Exception("cv2 not found")
            if not Path:
                return
            self._Path = Path
            self._Path_Memory = Path
            self.Stop()
            Cap = self._Capture_Open(Path)
            if Cap is None:
                self._GUI.Error(f"{self._Type} -> Open_With -> Could not open: {Path}")
                return
            with self._Capture_Lock:
                self._Capture = Cap
            self._Capture_Refresh_Info()
            if Start:
                self.Time_Set(int(float(Start) * 1000.0))
            if Stop is not None:
                self._Stop_Time_Ms = int(float(Stop) * 1000.0)
            else:
                self._Stop_Time_Ms = None
            self._Decode_Start()
            self._Prime_Frame()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open_With -> {E}")

    def _Prime_Frame(self):
        try:
            with self._Capture_Lock:
                Cap = self._Capture
                if Cap is None:
                    return
                Ok, Frame = Cap.read()
                if Ok and Frame is not None:
                    self._Last_Frame_Bgr = Frame
                    self._Schedule_Render(Frame)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Prime_Frame -> {E}")

    def Playing(self):
        try:
            return bool((not self._Pause) and (self._Capture is not None))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Playing -> {E}")
            return False

    def State(self):
        try:
            if self._Capture is None:
                return "stopped"
            if self._Pause:
                return "paused"
            return "playing"
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> State -> {E}")
            return "unknown"

    def Stop(self):
        try:
            self._Pause = True
            self._Stop_Time_Ms = None
            self._Capture_Close()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Stop -> {E}")

    def Pause(self):
        try:
            self._Pause = True
            self._Decode_Wake.set()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pause -> {E}")

    def Play(self):
        try:
            if self._Capture is None and self._Path:
                self.Open()
            if self._Capture is None:
                return
            self._Pause = False
            self._Decode_Wake.set()
            self._Decode_Start()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Play -> {E}")

    def Play_BlockingStart(self, Timeout=2.0):
        try:
            T0 = time.time()
            self.Play()
            while time.time() - T0 < float(Timeout):
                if self._Capture is not None and not self._Pause:
                    return True
                time.sleep(0.02)
            return False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Play_BlockingStart -> {E}")
            return False

    def Length(self):
        try:
            return int(self._Duration_Ms or 0)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Length -> {E}")
            return 0

    def Time_Get(self):
        try:
            return int(self._Capture_Time_Get_Ms())
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Time_Get -> {E}")
            return 0

    def Time_Set(self, Value):
        try:
            Ok = self._Capture_Time_Set_Ms(int(Value))
            if Ok:
                self._Prime_Frame()
            return Ok
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Time_Set -> {E}")
            return False

    def Position_Get(self):
        try:
            return float(self._Capture_Pos_Get())
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position_Get -> {E}")
            return 0.0

    def Position_Set(self, Value):
        try:
            Ok = self._Capture_Pos_Set(float(Value))
            if Ok:
                self._Prime_Frame()
            return Ok
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position_Set -> {E}")
            return False

    def Frame_Step(self):
        try:
            if self._Capture is None:
                return False
            Was_Pause = bool(self._Pause)
            self._Pause = True
            with self._Capture_Lock:
                Cap = self._Capture
                if Cap is None:
                    return False
                Ok, Frame = Cap.read()
            if Ok and Frame is not None:
                self._Last_Frame_Bgr = Frame
                self._Schedule_Render(Frame)
                self._Pause = Was_Pause
                return True
            self._Pause = Was_Pause
            return False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Frame_Step -> {E}")
            return False

    def Rate_Set(self, Value):
        try:
            self._Rate = float(Value)
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rate_Set -> {E}")
            return False

    def Rate_Get(self):
        try:
            return float(self._Rate or 1.0)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rate_Get -> {E}")
            return 1.0

    def Loop(self, Enabled):
        try:
            self._Loop = bool(Enabled)
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Loop -> {E}")
            return False

    def Snapshot(self, Path, Width=0, Height=0):
        try:
            Frame = self._Last_Frame_Bgr
            if Frame is None:
                return False
            Out = Frame
            if int(Width) > 0 and int(Height) > 0 and self._CV2_Available:
                Out = cv2.resize(Out, (int(Width), int(Height)))
            Ok = False
            if self._CV2_Available:
                Ok = bool(cv2.imwrite(str(Path), Out))
            return Ok
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Snapshot -> {E}")
            return False

    def Queue(self, Paths):
        try:
            self._Queue = list(Paths) if Paths else []
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Queue -> {E}")

    def Play_Next(self):
        try:
            if self._Queue:
                Nxt = self._Queue.pop(0)
                self.Open_With(Nxt)
                self.Play()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Play_Next -> {E}")

    def Resize(self, Event=False):
        try:
            if self._Last_Frame_Bgr is None:
                return
            self._After(0, self._Render_Frame_Main)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
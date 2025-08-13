# IMPORT LIBRARIES
import os
import time
try:
    import vlc
except Exception:
    vlc = None
from .N_GUI import GUI

class Video:

    def __init__(self, Frame, *Args, **Kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Video"
            try:
                self._Frame = Frame
                self._VLC_Args = ['--quiet', '--no-xlib']
                self._VLC_Available = vlc is not None
                self._VLC = vlc.Instance(self._VLC_Args) if self._VLC_Available else None
                self._Player = self._VLC.media_player_new() if self._VLC_Available else None
                if self._Player:
                    self.Bind_Window()
                    self.Bind_Events()
                self._Media = False
                self._Pause = True
                self._Path = False
                self._Path_Memory = False
                self._Subtitle = False
                self._Queue = []
                self._EQ = None
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Video[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Video[]"
        
    def Delete(self):
        try:
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")
            
    def Set(self, Path=''):
        try:
            if not self._VLC_Available:
                raise Exception("python-vlc not found")
            if Path:
                self._Path = Path
                if self._Path!=self._Path_Memory:
                    self._Path_Memory = self._Path
                    self.Open()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Widget(self):
        try:
            return self._Player
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
    def Open(self):
        try:
            if not self._VLC_Available:
                raise Exception("python-vlc not found")
            if self._Path:
                self.Stop()
                if self._Subtitle:
                    self.Subtitle_Off()
                    self._Subtitle = False
                self._Media = self._VLC.media_new(self._Path)
                self._Player.set_media(self._Media)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")
            
    def Open_With(self, Path, Start=0, Stop=None, Cache_Ms=300, Hw=True):
        try:
            if not self._VLC_Available:
                raise Exception("python-vlc not found")
            if Path:
                self.Stop()
                if self._Subtitle:
                    self.Subtitle_Off()
                    self._Subtitle = False
                M = self._VLC.media_new(Path)
                M.add_option(f":network-caching={int(Cache_Ms)}")
                if Start:
                    M.add_option(f":start-time={int(Start)}")
                if Stop is not None:
                    M.add_option(f":stop-time={int(Stop)}")
                if Hw:
                    M.add_option(":hwdec=auto")
                self._Media = M
                self._Player.set_media(M)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open_With -> {E}")
            
    def Playing(self):
        try:
            return bool(self._Player.is_playing()) if self._Player else False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> State -> {E}")
            
    def State(self):
        try:
            return self._Player.get_state()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> State -> {E}")
            
    def Stop(self):
        try:
            if self._Player:
                self._Player.stop()
                self._Pause = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Stop -> {E}")
            
    def Pause(self):
        try:
            if self._Player:
                self._Player.pause()
                self._Pause = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pause -> {E}")
            
    def Play(self):
        try:
            if self._Player:
                self._Player.play()
                self._Pause = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Play -> {E}")
            
    def Play_BlockingStart(self, Timeout=2.0):
        try:
            T0 = time.time()
            self.Play()
            while time.time() - T0 < float(Timeout):
                if self._Player and self._Player.is_playing():
                    return True
                time.sleep(0.02)
            return False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Play_BlockingStart -> {E}")
            
    def Length(self):
        try:
            return self._Player.get_length()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Length -> {E}")
            
    def Time_Get(self):
        try:
            return self._Player.get_time()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Time_Get -> {E}")
            
    def Time_Set(self, Value):
        try:
            return self._Player.set_time(Value)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Time_Set -> {E}")
            
    def Position_Get(self):
        try:
            return self._Player.get_position()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position_Get -> {E}")
            
    def Position_Set(self, Value):
        try:
            return self._Player.set_position(float(Value))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position_Set -> {E}")
            
    def Frame_Step(self):
        try:
            return self._Player.next_frame()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Frame_Step -> {E}")
            
    def Rate_Set(self, Value):
        try:
            return self._Player.set_rate(float(Value))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rate_Set -> {E}")
            
    def Rate_Get(self):
        try:
            return self._Player.get_rate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rate_Get -> {E}")
            
    def Loop(self, Enabled):
        try:
            return self._Player.set_repeat(bool(Enabled))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Loop -> {E}")
            
    def Audio_Get(self):
        try:
            return self._Player.audio_get_track_description()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Get -> {E}")
            
    def Audio_Set(self, ID):
        try:
            return self._Player.audio_set_track(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Set -> {E}")
            
    def Audio_Tracks(self):
        try:
            Desc = self._Player.audio_get_track_description()
            return [(D.id, D.name) for D in Desc] if Desc else []
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Tracks -> {E}")
            
    def Audio_Set_ByName(self, Name):
        try:
            Tracks = self.Audio_Tracks()
            for Tid, N in Tracks:
                if N and str(N).lower() == str(Name).lower():
                    return self._Player.audio_set_track(Tid)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Set_ByName -> {E}")
            
    def Audio_Channel_Set(self, Channel):
        try:
            return self._Player.audio_set_channel(int(Channel))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Channel_Set -> {E}")
            
    def Audio_Delay_Set(self, Microseconds):
        try:
            return self._Player.audio_set_delay(int(Microseconds))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Delay_Set -> {E}")
            
    def Audio_Delay_Get(self):
        try:
            return self._Player.audio_get_delay()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Delay_Get -> {E}")
            
    def Audio_Equalizer_Enable(self, Bands=None, Preamp=0.0):
        try:
            Eq = vlc.AudioEqualizer() if self._VLC_Available else None
            if Eq is None:
                return
            if Bands:
                for I, Gain in enumerate(Bands):
                    Eq.set_amp_at_index(float(Gain), I)
            Eq.set_preamp(float(Preamp))
            self._Player.set_equalizer(Eq)
            self._EQ = Eq
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Equalizer_Enable -> {E}")
            
    def Audio_Devices(self):
        try:
            return self._Player.audio_output_device_get()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Devices -> {E}")
            
    def Mute(self, Value=None):
        try:
            if isinstance(Value, bool) or Value in (0, 1):
                self._Player.audio_set_mute(bool(Value))
            return self._Player.audio_get_mute()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Mute -> {E}")
            
    def Volume_Get(self):
        try:
            return self._Player.audio_get_volume()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Volume_Get -> {E}")
            
    def Volume_Set(self, Value):
        try:
            return self._Player.audio_set_volume(Value)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Volume_Set -> {E}")
            
    def Volume_Fade(self, Target, Duration=0.5, Steps=10):
        try:
            Start = self._Player.audio_get_volume()
            Steps_I = int(Steps)
            Dur = float(Duration)
            for I in range(1, Steps_I+1):
                V = Start + (int(Target) - Start)*I/Steps_I
                self._Player.audio_set_volume(int(V))
                time.sleep(Dur/Steps_I)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Volume_Fade -> {E}")
            
    def Subtitle(self, Path):
        try:
            if self._Subtitle:
                self.Subtitle_Off()
                self._Subtitle = False
            self._Player.add_slave(vlc.MediaSlaveType.subtitle, Path, True)
            self._Subtitle = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle -> {E}")
            
    def Subtitle_On(self):
        try:
            if self._Subtitle:
                self._Player.video_set_spu(0)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_On -> {E}")
            
    def Subtitle_Off(self):
        try:
            if self._Subtitle:
                self._Player.video_set_spu(-1)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_Off -> {E}")
            
    def Subtitle_Tracks(self):
        try:
            Desc = self._Player.video_get_spu_description()
            return [(D.id, D.name) for D in Desc] if Desc else []
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_Tracks -> {E}")
            
    def Subtitle_Set(self, Track_ID):
        try:
            return self._Player.video_set_spu(int(Track_ID))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_Set -> {E}")
            
    def Subtitle_Delay_Set(self, Microseconds):
        try:
            return self._Player.video_set_spu_delay(int(Microseconds))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_Delay_Set -> {E}")
            
    def Subtitle_Delay_Get(self):
        try:
            return self._Player.video_get_spu_delay()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_Delay_Get -> {E}")
            
    def Aspect_Set(self, Ratio):
        try:
            if Ratio is None:
                return self._Player.video_set_aspect_ratio(None)
            return self._Player.video_set_aspect_ratio(str(Ratio).encode())
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Aspect_Set -> {E}")
            
    def Scale_Set(self, Factor):
        try:
            if Factor is None:
                return self._Player.video_set_scale(-1)
            return self._Player.video_set_scale(float(Factor))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Scale_Set -> {E}")
            
    def Snapshot(self, Path, Width=0, Height=0):
        try:
            return self._Player.video_take_snapshot(0, Path, int(Width), int(Height))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Snapshot -> {E}")
            
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
            
    def Bind_Events(self):
        try:
            if not self._Player:
                return
            Em = self._Player.event_manager()
            Em.event_attach(vlc.EventType.MediaPlayerEndReached, self.On_End)
            Em.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.On_Err)
            Em.event_attach(vlc.EventType.MediaPlayerPlaying, self.On_Play)
            Em.event_attach(vlc.EventType.MediaPlayerPaused, self.On_Pause)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind_Events -> {E}")
            
    def On_End(self, Event):
        try:
            self.Play_Next()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_End -> {E}")
            
    def On_Err(self, Event):
        try:
            self._GUI.Error(f"{self._Type} -> VLC Error")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Err -> {E}")
            
    def On_Play(self, Event):
        try:
            self._Pause = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Play -> {E}")
            
    def On_Pause(self, Event):
        try:
            self._Pause = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Pause -> {E}")
            
    def Bind_Window(self):
        try:
            if hasattr(self._Frame, "_Frame") and hasattr(self._Frame._Frame, "winfo_id") and self._Player:
                Wid = self._Frame._Frame.winfo_id()
                try:
                    self._Player.set_hwnd(Wid)
                except Exception:
                    try:
                        self._Player.set_xwindow(Wid)
                    except Exception:
                        try:
                            self._Player.set_nsobject(int(Wid))
                        except Exception:
                            pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind_Window -> {E}")
            
    def Close(self):
        try:
            self.Stop()
            if self._Player:
                try:
                    self._Player.release()
                except Exception:
                    pass
            if self._Media:
                try:
                    self._Media.release()
                except Exception:
                    pass
            if self._VLC:
                try:
                    self._VLC.release()
                except Exception:
                    pass
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Close -> {E}")
            
    def __del__(self):
        try:
            self.Close()
        except:
            pass
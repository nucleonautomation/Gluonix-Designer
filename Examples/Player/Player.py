# -------------------------------------------------------------------------------------------------------------------------------
# Gluonix Runtime
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
if __name__=='__main__':
    from Nucleon.Runner import * ###!REQUIRED ------- Any Script Before This Won't Effect GUI Elements
#################################################################################################################################
#################################################################################################################################
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming Start
# -------------------------------------------------------------------------------------------------------------------------------

    import time
    from threading import Thread, Lock, Event
    
    Video_Path = 'Video.mp4'

    Seek_Lock = Lock()
    Seeking_Event = Event()
    Seeking_Hold_Seconds = 0.3

    Player = Root.Player.Video()
    Player.Volume_Set(160)

    Control = Root.Control
    Control.Play.Bind(On_Click=lambda E: Play())
    Control.Forward.Bind(On_Click=lambda E: Forward())
    Control.Backward.Bind(On_Click=lambda E: Backward())
    Control.Volume.Bind(On_Click=lambda E: Volume())
    Control.Volume_Bar.Bind(On_Click=lambda E: Volume_Bar(E), On_Drag=lambda E: Volume_Bar_Drag(E))
    Control.Volume_Bar.Set(80)
    Volume_Bar_Info = Control.Volume_Bar.Config_Get('Width', 'Height', 'Border_Size')
    Control.Progress_Bar.Bind(On_Click=lambda E: Progress_Bar(E), On_Drag=lambda E: Progress_Bar_Drag(E))
    Control.Progress_Bar.Set(0)
    Progress_Bar_Info = Control.Progress_Bar.Config_Get('Width', 'Height', 'Border_Size')
    
    def Play():
        if Player.Playing():
            Player.Pause()
            Control.Play.Set('./Icon/Play.png')
        else:
            Player.Set(Video_Path)
            Player.Play()
            Control.Play.Set('./Icon/Pause.png')

    def Forward():
        Current = int(Player.Time_Get()/1000)
        Player.Time_Set((Current+10)*1000)

    def Backward():
        Current = int(Player.Time_Get()/1000)
        Player.Time_Set((Current-10)*1000)
    
    def Volume():
        if Player.Mute():
            Player.Mute(False)
            Control.Volume.Set('./Icon/Volume.png')
        else:
            Player.Mute(True)
            Control.Volume.Set('./Icon/Mute.png')
            
    def Volume_Bar(E):
        Volume = int((E.x*100)/(Volume_Bar_Info['Width']-(Volume_Bar_Info['Border_Size'])))
        Volume = max(0, min(100, Volume))
        Control.Volume_Bar.Set(Volume)
        Player.Volume_Set(Volume*2)
        
    def Volume_Bar_Drag(E):
        Volume = int((E.x*100)/(Volume_Bar_Info['Width']-(Volume_Bar_Info['Border_Size'])))
        Volume = max(0, min(100, Volume))
        Control.Volume_Bar.Set(Volume)
        Player.Volume_Set(Volume*2)

    def Ms_From_Percent(Percent, Length_Raw):
        return int((Percent / 100.0) * Length_Raw)

    def Progress_From_X(Mouse_X):
        Width_Available = Progress_Bar_Info['Width'] - Progress_Bar_Info['Border_Size']
        Percent = max(0, min(100, (Mouse_X * 100) / Width_Available))
        return Percent

    def Release_Seek_After(Delay_Seconds=Seeking_Hold_Seconds):
        time.sleep(Delay_Seconds)
        Seeking_Event.clear()

    def Progress_Bar(Event_Data):
        if Player.Playing():
            Seeking_Event.set()
            with Seek_Lock:
                Length_Raw = Player.Length()
                Percent = Progress_From_X(Event_Data.x)
                Control.Progress_Bar.Set(Percent)
                Player.Time_Set(Ms_From_Percent(Percent, Length_Raw))
            Thread(target=Release_Seek_After, daemon=True).start()

    def Progress_Bar_Drag(Event_Data):
        if Player.Playing():
            Seeking_Event.set()
            with Seek_Lock:
                Length_Raw = Player.Length()
                Percent = Progress_From_X(Event_Data.x)
                Control.Progress_Bar.Set(Percent)
                Player.Time_Set(Ms_From_Percent(Percent, Length_Raw))
        
    def Format_Time(Seconds):
        Hours, rem = divmod(Seconds, 3600)
        Minutes, Seconds_Remaining = divmod(rem, 60)
        return f"{Hours}h {Minutes}m {Seconds_Remaining}s"

    def Running_Thread():
        while True:
            Current_Raw = Player.Time_Get()
            Length_Raw = Player.Length()
            if Length_Raw > 0:
                Percent = max(0, min(100, (Current_Raw / Length_Raw) * 100))
                if Player.Playing():
                    Current = int(Current_Raw / 1000)
                    Length = int(Length_Raw / 1000)
                    Control.Time_Elapsed.Set(Format_Time(Current))
                    Control.Time_Total.Set(Format_Time(Length))
                    if not Seeking_Event.is_set():
                        with Seek_Lock:
                            Control.Progress_Bar.Set(Percent)
                else:
                    if Percent >= 99.5:
                        Player.Stop()
                        Control.Play.Set('./Icon/Play.png')
                        Control.Progress_Bar.Set(0)
            time.sleep(0.1)

    Thread(target=Running_Thread, daemon=True).start()

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################
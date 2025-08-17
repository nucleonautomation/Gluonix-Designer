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

    Login = Root.Login
    Width, Height = Login.Size()
    Left, Top = Login.Position()
    
    Login.User.Value.Bind(On_Focus_In=lambda E: User_Focus_In(), On_Focus_Out=lambda E: User_Focus_Out())
    Login.Pass.Value.Bind(On_Focus_In=lambda E: Pass_Focus_In(), On_Focus_Out=lambda E: Pass_Focus_Out())
    Login.Pass.Value.Config(Secure=True)
    
    Trigger = Login.Trigger
    
    Trigger.Bind(On_Click=lambda E: Open_Login())
    
    def Open_Login():
        Trigger.Set('CLOSE ', './Icon/Up.png')
        Trigger.Bind(On_Click=lambda E: Close_Login())
        Login.Config(Animate_Left=Left, Animate_Top=-240)
        Login.Position(Top=-50)
        Login.Animate()
    
    def Close_Login():
        Trigger.Set('LOGIN ', './Icon/Down.png')
        Trigger.Bind(On_Click=lambda E: Open_Login())
        Login.Config(Animate_Left=Left, Animate_Top=-50)
        Login.Position(Top=-240)
        Login.Animate()
        
    def User_Focus_In():
        Login.User.ValueBackground.Config(Outline='#0000FF')
        Login.User.Logo.Show()
        
    def User_Focus_Out():
        Login.User.ValueBackground.Config(Outline='#000000')
        Login.User.Logo.Show()
        
    def Pass_Focus_In():
        Login.Pass.ValueBackground.Config(Outline='#0000FF')
        Login.Pass.Logo.Show()
        
    def Pass_Focus_Out():
        Login.Pass.ValueBackground.Config(Outline='#000000')
        Login.Pass.Logo.Show()

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################
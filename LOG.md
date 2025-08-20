# Change Log

## V(5.6)
- Root/Popup Icon Will Be Support In All OS (Windows, Linux, MacOS etc), & All Image File Are Accepted
- New Canvas_Text Support Justification For center, left, right, n, nw, ne, s, sw, se
- Designer Paste Action Can Be Performed On Non Container Widgets, Will Take The Parent As Copy ID

## V(5.5)
- GIF Support Included In Image Widgets (Except Interactive Image). GIF Will Run Automatically In Thread With Widget.Show() and Stop with Widget.Hide()
- Image Widgets, Two Separate Functions Added Widget.Run() & Widget.Stop() To Control GIF Images
- Update Canvas Text Using Image Rendering For More Options, i.e. Skew Options For Horizontal & Vertical Skew, Rotation, Vertical Text, Extensive Font Choice
- Legacy Canvas_Text Class Moves To Canvas_Text_Old

## V(5.4)
- Gluonix Library Optimized
- New Interactive Login Example Added Using Animations

## V(5.3)
- Canvas Item Image & RectangleR Has Skew Options For Horizontal & Vertical Skew
- On_Animate Bind Function Added To Widgets, As Animate() Triggers Inside A Thread
- Center() Method Added To All The Widgets, Which Changes The Position By Giving Center Coords & Return Values Of Current Center
- Video Player Directly Added To Frame & Canvas
- Group Widget Bug Fixes
- Canvas Item Move Bug Fixes
- New Example For Video Player
- New Example For Game Using Animations

## V(5.2)
- Animation Added To Widgets, All Widgets Support Predefined Starting Animate_Left, Animate_Top, Animate_Height, Animate_Width, Animate_Time, And Animate() To Trigger Animation
- Canvas Items Pie, Circle, Arc Use Animate_Radius Instead Of Animate_Height, Animate_Width
- Animate_Time Variable (In Seconds, e.g., 0.5) Defines Total Duration Of Widget Animation, Controls Speed From Slow To Fast
- New Example Added For Animation Setup
- RectangleR Added To Designer Items, With Extra Options For Angle And Radius
- Entry Added To Lite Widgets
- Foreground Option To Switch
- Switch, Check & Radio Changed To Non-Border Widgets
- Canvas Item Name Increment Bug Fix
- Widgets Bug Fixes
- Designer Bug Fixes

## V(5.1)
- Added New Widget 'Group', Can Add Multiple Items To Group. Group Has Basic Functionality Like, Show/Hide & Move
- Widgets Bug Fixes
- Designer Bug Fixes
- Introduced Get() Function In Label, Button, Compound & Roubel
- Move() Function Added To All Widgets, Which Moves Widget By Specific Offset

## V(5.0)
- Opening Designer In Project Folder Will Autoload Project
- Designer Bug Fixes

## V(4.7)
- Design/Edit Direct Runtime Applications
- Design Environment Bug Fixes
- Naming Increment Fixed For Copy/Paste

## V(4.6)
- Canvas Item Widgets Optimization & Bug Fix
- All Widget Optimization
- Design Mode Now Supports Hidden Widgets

## V(4.5)
- Canvas Item Widgets Bug Fix
- Canvas Image Item Width Heigth Config Fixed

## V(4.4)
- Canvas Item Widgets Bug Fix
- Design Glid Lock Fixed To Permanent Value
- Get Size Ratio With Root.Ratio()
- New Example Added For Interactive Horizontal Slider

## V(4.3)
- Widget Copy() -> Error Attribute Not Found Bug Fix

## V(4.2)
- Resizing & Dark Mode Bug Fix

## V(4.1)
- The Application Is Now Fully Optimized For Resizing. It Will Only Trigger A Resize Operation When The Window Is Actually Resized, Avoiding Any Unnecessary Processing

## V(4.0)
- Compare Tool Is Added. Compare Two Projects Side By Side & Copy Widgets From One Project To Other
- Designer Has Resizable Capabilities

## V(3.6)
- Left Right Top Bottom Anchoring Updated. Widgets Will Properly Relocated To Each Side Depending Upon The Position On Screen
- Minimize, Maximize & Restore Bug Fixes
- Grab Function To Screenshot Any Widget Will According To Windows Display Scaling

## V(3.5)
- Bug Fixes: Accidentally Introduced More Bugs In 3.4 In Color Updates :)
- Root Mode Changes Will Apply To Popups Too

## V(3.4)
- Bug Fixes In Dark Color Updates and Hover Color Updates.
- Bug Fixes In Interactive Zoom Image

## V(3.3)
- Interactive Image Zoom & Pan Are Updated For Better Performance With Large Images & In Depth Zoom

## V(3.2)
- Update Color Functionality Is Changed To Update Colors i.e. Root.Update_Colors() Or Popup1.Update_Colors(). Update Color Method Introduced To Each Widget To Update Color For One Corresponding Widget Only i.e. Widget.Update_Color(). This Is Only Required If The Widget Auto_Dark Is Set To False
- Auto_Dark Config Introduced, While It Is True, Widget Will Automatically Adjust Dark Colors Based On Changed Values

## V(3.1)
- Update Color Function Introduced In Root To Update Light & Dark Mode Colors For All Widgets Automatically
- Usage: Root.Update_Color() Or Popup1.Update_Color()
- Note: Check Switching From Dark To Light Or Vice Versa, It Only Work For Each Main Window. Has To be Done Separately For Root & Popups

## V(3.0)
- Dark & Light Modes. Software Automatically Configures Colors By Inverting Values
- Custom Colors Can Be Set Through Config, i.e. Background, Light_Background, Dark_Background
- Mode Trigger From Root, i.e. Root.Light_Mode() Root.Dark_Mode()

## V(2.8)
- Full APP Resize Adjustment Option When Changing Display Size In Pixels.
- Widgets Can Be Added To Container Even Other Widget Is Selected. Adds To Parent Container

## V(2.7)
- Widget Copy Fixed. All Widgets Retain Their Names.
- Transparent Image Conversion Changed To RGBA

## V(2.6)
- Project on Pypi. "pip install GluonixDesigner"

## V(2.5)
- Relative Paths Fixed For Linux. Tested Design & Deployment On Ubuntu Linux

## V(2.4)
- All Widgets Can Use Hover Colors Depending Upon Config List For Background, Foreground, Border_Color & Shadow_Color
- E.G.: Hover_Background='#FF0000'

## V(2.3)
- Relative Paths Fixed, Designer & Deployed Projects Can be Started From Any Directory Using Relative Or Absolute Path

## V(2.2)
- List, Entry & Button Widget Configs Updates

## V(2.1)
- Deployment To Runtime Changed To Single Nucleon Folder Instead Of Nucleon & Data Separate Folders
- Design Environment Updates

## V(2.0)
- Tree Add Function Takes Image Path To Append An Image Before Text
- Initial Function Added To Image So It Can Be Reset To Initial Image Assigned At Design Time

## V(1.8)
- Fixed: Naming While Copying A Widget. New Object Will Have Be Independent Object With Different Name

## V(1.7)
- Translucent Config For Canvas Item Rectangle, Rectangle2, Circle, Oval, Arc, Pie, & Polygon
- Fixed: Canvas Items Accessible Using Names

## V(1.6)
- Display Alignment To Percentage Will Require Left, Top, Width, & Height as Percent Value For Non-Full_Screen Window

## V(1.5)
- Fixed: Tree Height Issues Caused By Horizontal Scrollbar
- Fixed: Scroll Movement & Size In Designer

## V(1.4)
- Global Option To Choose Pixel Or Percentage Alignment For Display In Project Overview

## V(1.3)
- Bind Functions For On_Show And On_Hide

## V(1.2)
- Fixed: Show() For Check, Radio & Switch

## V(1.1) - Extra
- Fixed: Interactive Image For Display & Zoom Error

## V(1.1)
- Initial Upload

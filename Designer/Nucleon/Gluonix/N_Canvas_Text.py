# IMPORT LIBRARIES
import threading, math, time
from PIL import Image as PIL_Image, ImageDraw as PIL_ImageDraw, ImageFont as PIL_ImageFont

class Canvas_Text:
    
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Width', 'Height', 'Left', 'Top', 'Color', 'Background', 'Size', 'Value', 'Weight', 'Font', 'Resize', 'Justify', 'Anchor', 'Resize_Font', 'Vertical', 'Rotate', 'Skew_Horizontal', 'Skew_Vertical']
        self._Display = True
        self._Resize_Index = 0
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Resize_Font = True
        self._Type = 'Canvas_Text'
        self._Left, self._Top, self._Width, self._Height = 0, 0, 0, 0
        self._Value = ''
        self._Color = '#000000'
        self._Background = False
        self._Size = 20
        self._Weight = 'normal'
        self._Font = 'Helvetica'
        self._Anchor = 'nw'
        self._Justify = 'center'
        self._Vertical = False
        self._Rotate = 0
        self._Skew_Horizontal = 0
        self._Skew_Vertical = 0
        self._Widget = self._Canvas.Image()
        self._Widget.Config(Name = False, Transparent = True)
        self._Resizable = self._Canvas._Resizable

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_Text[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_Text[]"

    def Delete(self):
        try:
            self._Widget.Delete()
            if self in self._Canvas._Widget:
                self._Canvas._Widget.remove(self)
            if self:
                del self
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Delete -> {Error}")

    def Hide(self):
        try:
            self._Widget.Hide()
            self._Display = False
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Hide -> {Error}")

    def Show(self):
        try:
            self._Widget.Show()
            self._Display = True
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Show -> {Error}")

    def Display(self):
        try:
            self._Widget.Display()
            self._Display = True
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Display -> {Error}")

    def Set(self, Value):
        try:
            self._Value = Value
            self.Create()
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Set -> {Error}")
            
    def Animate(self):
        try:
            self._Widget.Animate()
            self.Show()
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Animate -> {Error}")
            self.Animate_Cancel()
            
    def Animate_Cancel(self):
        try:
            self._Widget.Animate_Cancel()
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Animate_Cancel -> {Error}")
            
    def Config_Get(self, *Input):
        try:
            Return = {}
            for Each in self._Config:
                if Each in Input:
                    Return[Each] = getattr(self, "_" + Each)
            return Return
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Config_Get -> {Error}")

    def Config(self, **Input):
        try:
            Run = False
            for Each in self._Config:
                if Each in Input:
                    Value = Input[Each]
                    setattr(self, "_" + Each, Value)
                    setattr(self, "_" + Each + "_Current", Value)
                    Run = True
            Forward = {Key: Val for Key, Val in Input.items() if Key not in ('Name', 'Transparent')}
            if Forward:
                self._Widget.Config(**Forward)
            if Run:
                self.Relocate()
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Config -> {Error}")

    def Move(self, Left = None, Top = None):
        try:
            if Left is not None:
                self._Left += Left
            if Top is not None:
                self._Top += Top
            if Left is not None or Top is not None:
                self.Position(Left = self._Left, Top = self._Top)
            return True
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Move -> {Error}")
            
    def Center(self, Left = None, Top = None):
        try:
            if Left is not None:
                self._Left = Left - self._Width / 2
            if Top is not None:
                self._Top = Top - self._Height / 2
            if Left is not None or Top is not None:
                self.Position(Left = self._Left, Top = self._Top)
            return [self._Left + self._Width / 2, self._Top + self._Height / 2]
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Center -> {Error}")
        
    def Position(self, Left = None, Top = None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self._Widget.Position(self._Left, self._Top)
                self.Relocate()
            return [self._Left, self._Top]
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Position -> {Error}")
            
    def Size(self, Width = False, Height = False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self._Widget.Size(self._Width, self._Height)
                self.Relocate()
            return [self._Width, self._Height]
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Size -> {Error}")

    def Bind(self, **Input):
        try:
            self._Widget.Bind(**Input)
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Bind -> {Error}")

    def Create(self):
        try:
            Image_Object = self.Render()
            self._Widget._Pil = True
            self._Widget.Set(Image_Object)
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Canvas.__dict__:
                        del self._Canvas.__dict__[self._Last_Name]
                if self._Name:
                    self._Canvas.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Create -> {Error}")

    def Relocate(self, Direct = False):
        try:
            if self._Resize and self._Resizable:
                Width_Ratio = self._Canvas._Width_Current / self._Canvas._Width
                Height_Ratio = self._Canvas._Height_Current / self._Canvas._Height
                self._X_Current = self._Left * Width_Ratio
                self._Y_Current = self._Top * Height_Ratio
                self._Width_Current = self._Width * Width_Ratio
                self._Height_Current = self._Height * Height_Ratio
            else:
                self._X_Current = self._Left
                self._Y_Current = self._Top
                self._Width_Current = self._Width
                self._Height_Current = self._Height
            if self._Resize_Font:
                Width_Ratio = self._Canvas._Width_Current / self._Canvas._Width
                Height_Ratio = self._Canvas._Height_Current / self._Canvas._Height
                Size_Value = math.floor(self._Size * (Width_Ratio if Width_Ratio < Height_Ratio else Height_Ratio))
            else:
                Size_Value = self._Size
            self._Size_Current = Size_Value
            self.Create()
            if self._Display:
                self.Display()
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Relocate -> {Error}")

    def Resize(self):
        try:
            self._Resize_Index = self._Canvas._GUI._Resize_Index
            self.Relocate()
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Resize -> {Error}")

    def Render(self):
        try:
            Text_Value = self._Value if isinstance(self._Value, str) else str(self._Value)
            if self._Vertical:
                S = Text_Value.replace('\t', '    ')
                S = ''.join('\u00A0' if ch == ' ' else ch for ch in S)
                Text_Value = '\n'.join(list(S))
            try:
                Font_Object = PIL_ImageFont.truetype(self._Font.lower() + '.ttf', int(max(1, self._Size_Current if hasattr(self, '_Size_Current') else self._Size)))
            except:
                Font_Object = PIL_ImageFont.truetype('arial.ttf', int(max(1, self._Size_Current if hasattr(self, '_Size_Current') else self._Size)))
            Weight_Value = (self._Weight or 'normal').strip().lower()
            Is_Bold = Weight_Value in ('bold', 'b', '700', 'semibold', 'demibold', 'heavy', 'black')
            Stroke_Width = 1 if Is_Bold else 0
            Width_Target = int(self._Width if self._Width else 1)
            Height_Target = int(self._Height if self._Height else 1)
            Temp_Image = PIL_Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            Draw = PIL_ImageDraw.Draw(Temp_Image)
            def Measure_Width(S):
                B = Draw.textbbox((0, 0), S, font = Font_Object, stroke_width = Stroke_Width)
                return max(1, B[2] - B[0])
            Paragraphs = Text_Value.split('\n') if '\n' in Text_Value else [Text_Value]
            Lines = []
            for Paragraph in Paragraphs:
                if not self._Width:
                    Lines.append(Paragraph)
                    continue
                Words = Paragraph.split(' ')
                if len(Words) == 1:
                    Current = ''
                    for Char in Paragraph:
                        Test = Current + Char
                        if Measure_Width(Test) <= Width_Target or not Current:
                            Current = Test
                        else:
                            Lines.append(Current)
                            Current = Char
                    if Current:
                        Lines.append(Current)
                    continue
                Current = ''
                for Word in Words:
                    Test = Current + (' ' if Current else '') + Word
                    if Measure_Width(Test) <= Width_Target or not Current:
                        Current = Test
                    else:
                        Lines.append(Current)
                        Current = Word
                if Current:
                    Lines.append(Current)
            if not Lines:
                Lines = ['']
            Para_Text = '\n'.join(Lines)
            B_All = Draw.multiline_textbbox((0, 0), Para_Text, font = Font_Object, align = (self._Justify or 'left'), spacing = 0, stroke_width = Stroke_Width)
            Text_Width = max(1, B_All[2] - B_All[0])
            Text_Height = max(1, B_All[3] - B_All[1])
            if not self._Width:
                Width_Target = Text_Width
            if not self._Height:
                Height_Target = Text_Height
            Background_Color = self._Background if self._Background else (0, 0, 0, 0)
            Image_Object = PIL_Image.new('RGBA', (max(1, Width_Target), max(1, Height_Target)), Background_Color)
            Draw = PIL_ImageDraw.Draw(Image_Object)
            Fill_Color = self._Color if self._Color else (0, 0, 0, 0)
            Justify_Value = (self._Justify or 'left').strip().lower()
            Draw.multiline_text((Width_Target / 2, Height_Target / 2), Para_Text, fill = Fill_Color, font = Font_Object, align = Justify_Value, spacing = 0, anchor = 'mm', stroke_width = Stroke_Width, stroke_fill = Fill_Color)
            self._Size_Rendered = int(max(1, self._Size_Current if hasattr(self, '_Size_Current') else self._Size))
            return Image_Object
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Render -> {Error}")
            return PIL_Image.new('RGBA', (max(1, int(self._Width or 1)), max(1, int(self._Height or 1))), (0, 0, 0, 0))
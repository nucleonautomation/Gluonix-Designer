import Variable

Global = Variable.Global
Root = Variable.Root

Total = '$ 0.00'

Root.Scan.Label.Hide()
Root.Scan.Item.Hide()
Root.Scan.Items.Hide()

Root.Home.Order.Bind(On_Click=lambda E: Root.Scan.Show())
Root.Home.Order.Image.Bind(On_Click=lambda E: Root.Scan.Show())
Root.Home.Order.Label.Bind(On_Click=lambda E: Root.Scan.Show())

Root.Scan.Search.Bind(On_Click=lambda E: Root.Search.Show())
Root.Scan.Search.Image.Bind(On_Click=lambda E: Root.Search.Show())
Root.Scan.Search.Label.Bind(On_Click=lambda E: Root.Search.Show())

Root.Search.No_Scan.Bind(On_Click=lambda E: Root.No_Scan.Show())
Root.Search.No_Scan.Label.Bind(On_Click=lambda E: Root.No_Scan.Show())

Root.No_Scan.Brewed.Bind(On_Click=lambda E: Brewed())
Root.No_Scan.Brewed.Image.Bind(On_Click=lambda E: Brewed())
Root.No_Scan.Brewed.Label.Bind(On_Click=lambda E: Brewed())

Root.No_Scan.Folgers.Bind(On_Click=lambda E: Folger())
Root.No_Scan.Folgers.Image.Bind(On_Click=lambda E: Folger())
Root.No_Scan.Folgers.Label.Bind(On_Click=lambda E: Folger())

Root.No_Scan.Tea.Bind(On_Click=lambda E: Tea())
Root.No_Scan.Tea.Image.Bind(On_Click=lambda E: Tea())
Root.No_Scan.Tea.Label.Bind(On_Click=lambda E: Tea())

Root.Scan.Credit.Bind(On_Click=lambda E: Payment())
Root.Scan.Credit.Image.Bind(On_Click=lambda E: Payment())
Root.Scan.Credit.Label.Bind(On_Click=lambda E: Payment())

Root.Confirm.Exit.Bind(On_Click=lambda E: Exit())
Root.Confirm.Exit.Image.Bind(On_Click=lambda E: Exit())
Root.Confirm.Exit.Label.Bind(On_Click=lambda E: Exit())

def Brewed():
    global Total
    Total = '$ 2.49'
    Root.Scan.Item.Set('(1 item)')
    Root.Scan.Items.Ietm.Name.Set('BUILT AND BREWED')
    Root.Scan.Items.Ietm.Quantity.Set('1')
    Root.Scan.Items.Ietm.Price.Set(Total)
    Root.Scan.Total.Subtotal_Value.Set(Total)
    Root.Scan.Total.Total_Value.Set(Total)
    Root.Scan.Label.Show()
    Root.Scan.Item.Show()
    Root.Scan.Items.Ietm.Show()
    Root.Scan.Items.Show()
    Root.Scan.Card.Show()
    Root.Scan.Credit.Show()
    Root.Scan.Show()

def Folger():
    global Total
    Total = '$ 1.79'
    Root.Scan.Item.Set('(1 item)')
    Root.Scan.Items.Ietm.Name.Set('FOLGERS')
    Root.Scan.Items.Ietm.Quantity.Set('1')
    Root.Scan.Items.Ietm.Price.Set(Total)
    Root.Scan.Total.Subtotal_Value.Set(Total)
    Root.Scan.Total.Total_Value.Set(Total)
    Root.Scan.Label.Show()
    Root.Scan.Item.Show()
    Root.Scan.Items.Ietm.Show()
    Root.Scan.Items.Show()
    Root.Scan.Card.Show()
    Root.Scan.Credit.Show()
    Root.Scan.Show()

def Tea():
    global Total
    Total = '$ 1.79'
    Root.Scan.Item.Set('(1 item)')
    Root.Scan.Items.Ietm.Name.Set('HOT TEA')
    Root.Scan.Items.Ietm.Quantity.Set('1')
    Root.Scan.Items.Ietm.Price.Set(Total)
    Root.Scan.Total.Subtotal_Value.Set(Total)
    Root.Scan.Total.Total_Value.Set(Total)
    Root.Scan.Label.Show()
    Root.Scan.Item.Show()
    Root.Scan.Items.Ietm.Show()
    Root.Scan.Items.Show()
    Root.Scan.Card.Show()
    Root.Scan.Credit.Show()
    Root.Scan.Show()
    
def Payment():
    global Total
    Root.Payment.Amount.Set(Total)
    Root.Payment.Show()
    Root.After(2000, lambda: Root.Confirm.Show())
    
def Exit():
    global Total
    Root.Home.Show()
    Total = '$ 0.00'
    Root.Scan.Total.Subtotal_Value.Set(Total)
    Root.Scan.Total.Total_Value.Set(Total)
    Root.Scan.Label.Hide()
    Root.Scan.Item.Hide()
    Root.Scan.Items.Ietm.Hide()
    Root.Scan.Items.Hide()
    Root.Scan.Card.Hide()
    Root.Scan.Credit.Hide()
    
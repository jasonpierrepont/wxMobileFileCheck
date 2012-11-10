'''
Created on Nov 1, 2012

@author: Jason
'''
import wx
import wx.grid as gridlib
import matchEmUp
import os
import shelve

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="File Checker",
                          pos=wx.DefaultPosition, size=(1000, 600))   
        self.MinSize=((600, 300))     
        self.main_panel = wx.Panel(self, wx.ID_ANY)
        
        self.match = matchEmUp.Matcher()        
        self.settings = shelve.open('settings/config')
        try:
            self.directory = self.settings["working_dir"]
        except KeyError:
            self.settings["working_dir"] = 'C:/'
            self.directory = self.settings["working_dir"]            
        try:
            self.copy_dir = self.settings["copy_dir"]
        except KeyError:
            self.settings["copy_dir"] = 'C:/'
            self.copy_dir = self.settings["copy_dir"]
            
        
        # Menu/Status Bars
        self.status = self.CreateStatusBar()
        self.menubar = wx.MenuBar()
        first = wx.Menu()
        second = wx.Menu()
        first.Append(-1, "File", "File")
        second.Append(-1, "Help", "Help")
        self.menubar.Append(first, "File")
        self.menubar.Append(second, "Help")
        self.SetMenuBar(self.menubar)
        
        
        # Left Side
        self.left = wx.Panel(self.main_panel)
        self.left.SetBackgroundColour('white')
        self.left_szr = wx.BoxSizer(wx.VERTICAL)
        self.left.SetSizer(self.left_szr)
        
        
        # Top Buttons
        self.btn_panel = wx.Panel(self.left)
        self.left_szr.Add(self.btn_panel, 0, wx.EXPAND)
        
        self.choose_btn = wx.Button(self.btn_panel, wx.ID_ANY, "Choose Working Directory", size=(150, 40))
        self.choose_btn.Bind(wx.EVT_BUTTON, self.choose_dir)
        self.load_btn = wx.Button(self.btn_panel, wx.ID_ANY, "Reload Files", size=(150, 40))
        self.load_btn.Bind(wx.EVT_BUTTON, self.reload_lists)
        self.dir = wx.StaticText(self.btn_panel, wx.ID_ANY, self.directory)

        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer.Add(self.choose_btn, 0, wx.EXPAND)
        self.btn_sizer.Add(self.load_btn, 0, wx.EXPAND)
        self.btn_sizer.Add(self.dir, 0,)
        
        # List Grid
        self.grid_panel = wx.Panel(self.left)
        self.left_szr.Add(self.grid_panel, 2 , wx.EXPAND)
        
        self.ad_list = gridlib.Grid(self.grid_panel, wx.ID_ANY)
        self.ad_list.CreateGrid(25,6)
        self.ad_list.EnableGridLines(False)

        self.ad_list.SetColLabelValue(0, "Advertiser")
        self.ad_list.SetColLabelValue(1, "Banner")
        self.ad_list.SetColLabelValue(2, "Landing 01")
        self.ad_list.SetColLabelValue(3, "Landing 02")
        self.ad_list.SetColLabelValue(4, "Landing 03")
        self.ad_list.SetColLabelValue(5, "URLs")
        
        self.ad_list.SetRowLabelSize(25)
        self.ad_list.AutoSizeColumns()

                
        self.list_szr = wx.BoxSizer(wx.HORIZONTAL)
        self.list_szr.Add(self.ad_list, 2, wx.EXPAND|wx.TOP, border=5)        
        self.grid_panel.SetSizer(self.list_szr)
        
        # URL Display
        self.url_panel = wx.Panel(self.left)
        self.left_szr.Add(self.url_panel, 0, wx.EXPAND)
                
        self.url_text = wx.TextCtrl(self.url_panel)        
        self.url_btn = wx.Button(self.url_panel, wx.ID_ANY, "Load Website")
        
        self.url_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.url_sizer.Add(self.url_text, 1, wx.EXPAND)
        self.url_sizer.Add(self.url_btn, 0, wx.RIGHT)
        self.url_panel.SetSizer(self.url_sizer)
        
        
        # Image
        self.image_panel = wx.Panel(self.left)
        self.image_panel.SetBackgroundColour((240, 240, 255))
        self.image_panel.SetMinSize((200,200))
        self.emptyimage = wx.EmptyImage(1, 1)
        self.image = wx.StaticBitmap(self.image_panel, wx.ID_ANY, wx.BitmapFromImage(self.emptyimage))
        self.left_szr.Add(self.image_panel, 3, wx.EXPAND|wx.TOP|wx.RIGHT, 5)
        
        #self.image_panel.Bind(wx.EVT_SIZE, self.OnResize)

        
        #---------------------------------------------------#    
        # Right Side                                        #
        #___________________________________________________#
        self.right = wx.Panel(self.main_panel)
        self.right.SetMinSize((200, -1))
        self.right_szr = wx.BoxSizer(wx.VERTICAL)
        
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        
        self.choose_copy_btn = wx.Button(self.right, wx.ID_ANY, "Choose Copy Source")
        self.copy_txt =wx.StaticText(self.right, wx.ID_ANY, self.copy_dir)
        
        self.capture_txt = wx.StaticText(self.right, wx.ID_ANY, "Capture File(s)")
        self.capture_txt.SetFont(font)
        self.capture_list = wx.ListBox(self.right)
        self.capture_list.Bind(wx.EVT_LISTBOX_DCLICK, self.capture_dclick)
        #self.capture_list.SetMaxSize((-1, 30))
        
        self.other_txt = wx.StaticText(self.right, wx.ID_ANY, "Other Files")
        self.other_txt.SetFont(font)
        self.other_list = wx.ListBox(self.right, wx.ID_ANY)
        self.other_list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_dclick)
        self.other_list.Bind(wx.EVT_LISTBOX, self.load_file)
        
        self.right_szr.Add(self.choose_copy_btn, 0, wx.EXPAND)
        self.right_szr.Add(self.copy_txt, 0)
        self.right_szr.Add(self.capture_txt, 0, wx.ALIGN_CENTER)
        self.right_szr.Add(self.capture_list, 0, flag=wx.EXPAND)        
        self.right_szr.Add(self.other_txt, 0, wx.ALIGN_CENTER)
        self.right_szr.Add(self.other_list, 1, flag=wx.EXPAND)        
        
        self.right.SetSizer(self.right_szr)
        self.right_szr.Layout()

            
        # Main Layout
        self.main_size = wx.BoxSizer(wx.HORIZONTAL)
        self.main_size.Add(self.left, 1, wx.EXPAND)
        self.main_size.Add(self.right, 0, wx.EXPAND|wx.LEFT, border=5)
        self.main_panel.SetSizer(self.main_size)
        self.main_panel.Layout()
        self.btn_panel.SetSizer(self.btn_sizer)
        self.btn_panel.Layout()
        
    def load_file(self, event):
        '''Load Image or text into the appropriate area.'''
        fdir = self.directory
        file_name = self.other_list.GetStringSelection()
        ld_file = fdir + '\\' + file_name
        if file_name.lower().endswith('png') or \
                file_name.lower().endswith('bmp') or \
                file_name.lower().endswith('jpg'):
            self.url_text.Clear()           
            replacement_img = wx.Image(ld_file, wx.BITMAP_TYPE_ANY)
            w, h = self.get_image_size(self.image_panel, replacement_img)
            
            self.image.SetBitmap(wx.BitmapFromImage(replacement_img.Scale(w, h)))
            self.image_panel.Refresh()
        elif file_name.lower().endswith('txt'):
            self.image.SetBitmap(wx.BitmapFromImage(self.emptyimage))
            f = open(ld_file, 'rb')
            url = f.read()
            self.url_text.ChangeValue(url)            
        else:
            pass
        
    def OnResize(self, event):
        w, h = self.get_image_size(self.image_panel, self.image )
        self.image.SetSize((w, h))
        self.image_panel.Refresh()
        
    def get_image_size(self, control, image):
        maxw, maxh = control.GetClientSize()
        w = image.GetWidth()
        h = image.GetHeight()
        if h > maxh:
            div = float(h) / maxh
            new_w = int(w / div)
            new_h = int(h / div)
        elif w > maxw:
            div = float(w) / maxw
            new_w = int(w / div)
            new_h = int(h / div)
        else:
            new_w = w
            new_h = h
        return new_w, new_h
        
    def choose_dir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.directory = dlg.GetPath()
            self.settings["working_dir"] = self.directory
            self.dir.SetLabel(self.directory)
        dlg.Destroy()
        self.load_lists()
        
    def load_lists(self):
        self.populate_lists(self.directory)
        self.show_main_list()
        self.show_other_files()
        self.show_capture_file()
        self.color_rows()
        
    def reload_lists(self, event):
        self.load_lists()
        
    def populate_lists(self, path):
        self.match.clear_lists()
        self.match.listall(path)
        
    # Grid Methods
    # Show File names, Resize columns, set colors, fonts etc.
    ##################################################################
        
    def show_main_list(self):
        self.ad_list.ClearGrid()
        fdict =self.match.file_dict
        keys = fdict.keys()
        sorted_keys = sorted(keys)
        line = 0
        for key in sorted_keys:
            column =0
            self.ad_list.SetCellValue(line, column, key)
            column += 1
            for item in fdict[key]:
                self.ad_list.SetCellValue(line, column, item)
                self.ad_list.Refresh()
                column += 1
            line += 1
        self.ad_list.AutoSizeColumns()
        self.grid_row_colors()
        
    def grid_row_colors(self):
        cols = self.ad_list.GetNumberCols()
        rows = self.ad_list.GetNumberRows()
        row = 1
        for x in range(row, rows + 1, 2):
            for y in range(0, cols + 1):
                self.ad_list.SetCellBackgroundColour(x, y, (240, 240, 240))
            x += 1
                
    
    def show_other_files(self):
        self.other_list.Clear()
        for item in self.match.other:
            self.other_list.Append(item)
            
    def color_rows(self):
        total = self.other_list.GetCount()
        start = 1
        while start <= total:
            self.other_list.SetItemBackgroundColour(start, "blue")
            start += 2
            
    def show_capture_file(self):
        self.capture_list.Clear()
        for item in self.match.capture:
            self.capture_list.Append(item)
            
    def on_dclick(self, event):
        select = self.other_list.GetSelection()
        text = self.other_list.GetString(select)
        renamed = wx.GetTextFromUser('Rename Item', 'Rename Dialog', text)
        if renamed != '':
            os.chdir(self.directory)
            os.rename(text, renamed)
        else:
            msg = wx.MessageDialog(self, "Must Enter a new filename", "Error", style=wx.OK)
            msg.ShowModal()
        self.load_lists()
        
    def capture_dclick(self, event):
        select = self.capture_list.GetSelection()
        text = self.capture_list.GetString(select)
        renamed = wx.GetTextFromUser('Rename Item', 'Rename Dialog', text)
        if renamed != '':
            os.chdir(self.directory)
            os.rename(text, renamed)
        else:
            msg = wx.MessageDialog(self, "Must Enter a new filename", "Error", style=wx.OK)
            msg.ShowModal()
        self.load_lists()
        
app = wx.App(False)
mainframe = MainFrame().Show()
app.MainLoop()
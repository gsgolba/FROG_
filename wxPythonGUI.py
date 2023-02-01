import spectrometer
import wx
def main():
    app = wx.App(redirect=False)
    frm = wx.Frame(None, title='Hello World')
    frm.Show(True)
    app.Mainloop()

if __name__ == '__main__':
    main()
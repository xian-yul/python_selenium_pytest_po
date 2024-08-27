import win32clipboard as WC
import win32con


class ClipBoard(object):
    '''设置剪切板内容和获取剪切板内容'''

    @staticmethod
    def getText():
        '''获取剪切板内容'''
        WC.OpenClipboard()
        value = WC.GetClipboardData(win32con.CF_TEXT)
        WC.CloseClipboard()
        return value

    @staticmethod
    def setText(value):
        '''设置剪切板内容'''
        WC.OpenClipboard()
        WC.EmptyClipboard()
        WC.SetClipboardData(win32con.CF_UNICODETEXT, value)
        WC.CloseClipboard()


if __name__ == '__main__':
    pass

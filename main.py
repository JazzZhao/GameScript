import time
import win32gui
from typing import Union
import win32con
import win32api
import random

"""
获取句柄

"""
def _get_all_handles():
    """获取当前所所有窗口的句柄"""
    parent_hwnd_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), parent_hwnd_list)
    return parent_hwnd_list

def _get_title(window: Union[int, list]):
    """获取窗口标题"""
    if isinstance(window, int):
        return win32gui.GetWindowText(window)
    elif isinstance(window, list):
        return [win32gui.GetWindowText(hwnd) for hwnd in window]
    
def _get_class(window: Union[int, list]):
    """获取窗口类名"""
    if isinstance(window, int):
        return win32gui.GetClassName(window)
    elif isinstance(window, list):
        return [win32gui.GetClassName(hwnd) for hwnd in window]
    
def _get_all_child_handles(parent_handle):
    """
    获取指定
    """
    if isinstance(parent_handle, int):
        child_hwnd_list = []
        win32gui.EnumChildWindows(parent_handle, lambda hwnd, param: param.append(hwnd), child_hwnd_list)
        return child_hwnd_list
    elif isinstance(parent_handle, list):
        child_hwnd_lists = []
        for handle in parent_handle:
            child_hwnd_list = []
            win32gui.EnumChildWindows(handle, lambda hwnd, param: param.append(hwnd), child_hwnd_list)
            child_hwnd_lists.append(child_hwnd_list)
        return child_hwnd_lists

def _get_current_handle():
    """获取当前最前置的窗口的句柄"""
    return win32gui.GetForegroundWindow()


"""
控制鼠标
"""

def single_click(handle, x, y, button='left'):
    if button == 'left':
        button_down = win32con.WM_LBUTTONDOWN
        button_up = win32con.WM_LBUTTONUP
        key = win32con.MK_LBUTTON
    elif button == 'right':
        button_down = win32con.WM_RBUTTONDOWN
        button_up = win32con.WM_RBUTTONUP
        key = win32con.MK_RBUTTON
    else:
        button_down = win32con.WM_MBUTTONDOWN
        button_up = win32con.WM_MBUTTONUP
        key = win32con.MK_MBUTTON
    pos = win32api.MAKELONG(x, y)
    win32api.SendMessage(handle, button_down, key, pos)
    win32api.SendMessage(handle, button_up, key, pos)

def double_click(handle, x, y):
    single_click(handle, x, y, 'left')
    #这里写一个随机数，范围是0.01到0.03
    time.sleep(random.uniform(0.01, 0.03))
    single_click(handle, x, y, 'left')


def move_mouse_back(handle, x, y):
    win32gui.SendMessage(handle, win32con.WM_MOUSEMOVE, 0, (y<<16) + x)

"""
模拟鼠标拖拽
"""
def drag_back(handle, start_x, start_y, end_x, end_y):
    move_mouse_back(handle, start_x, start_y)
    win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(start_x, start_y))
    time.sleep(0.5)
    move_mouse_back(handle, end_x, end_y)
    win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.WM_LBUTTONUP, win32api.MAKELONG(end_x, end_y))

"""
模拟鼠标滚轮
"""
def scroll_back(handle, amount, x, y):
    win32api.SendMessage(handle, win32con.WM_MOUSEWHEEL, amount, win32api.MAKELONG(x, y))
    

def get_pixel(hwnd, x, y):
    """获取指定位置的像素值"""
    hdc = win32gui.GetWindowDC(hwnd)
    color = win32gui.GetPixel(hdc, x, y)
    # win32gui.ReleaseDC(hwnd, hdc)
    red = color & 0xFF
    green = (color >> 8) & 0xFF
    blue = (color >> 16) & 0xFF
    return red, green, blue

if __name__ == "__main__":
    for handle in _get_all_handles():
        if "倩女" in _get_title(handle):
            # print(handle)
            # print(_get_title(handle))
            # rect = win32gui.GetWindowRect(handle)
            # width = rect[2] - rect[0]
            # height = rect[3] - rect[1]
            # print(width, height)
            # center_x = rect[0] + width // 2
            # center_y = rect[1] + height // 2
            # print(center_x, center_y)
            single_click(handle,100,100)
            # scroll_back(handle, -100, 100, 100)
            print(get_pixel(handle,100, 100))
            break
    
# csgo_yolov3_aimbot

基于yolov3的csgo自瞄ai

**关于权重和配置**

你可以在[这里](https://pjreddie.com/darknet/yolo/)下载模型权重和配置文件, 你可以在aimbot.py更具你的需要更改它

```py
CONFIG_FILE = './yolov3_416.cfg'
WEIGHT_FILE = './yolov3_416.weights'
```

**关于模型**

网络模型来自opencv库，但是opencv默认无GPU版本，如果你已经配置好了GPU版本的版本的opencv，你可以将如下的代码第一行注释，剩下的两行解注释

```py
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
```

提示，你可以使用如下代码检查opencv是否使用GPU

```py
import cv2
count = cv2.cuda.getCudaEnabledDeviceCount()
print(count)
```

**关于win32api**

如果你配置不好win32api，你可以使用pyautogui，但是要**注意**：

使用win32api移动鼠标并射击的时间是5-10ms，使用pyautogui则是200ms

```py
win32api.SetCursorPos((x, y))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
# pyautogui.moveTo(x,y)
# pyautogui.click()
```

**改进中......**

目前我使用CPU，跑网络+框人大约要600ms，如下。。。持续优化ing

```
get_window_time:0.0
get_screen_time:0.06599998474121094
run net time:0.5547058582305908
get enemy box time:0.07999610900878906
Detected animies:4
get front sight axis time0.001001596450805664
move mouse and shoot time:0.003999948501586914
tortoal time:0.7057034969329834
```




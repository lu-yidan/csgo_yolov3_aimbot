import keyboard
import numpy as np
import pyautogui
import win32api, win32con, win32gui,win32ui
import cv2
import math
import time

'''
Fastest way to take a screenshot with python on windows
https://blog.csdn.net/jokerzhanglin/article/details/117201541
https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows
'''
def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

CONFIG_FILE = './yolov3_416.cfg'
WEIGHT_FILE = './yolov3_416.weights'
net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHT_FILE)
#如果你使用的cv2支持GPU
if cv2.cuda.getCudaEnabledDeviceCount():    
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
#如果你使用的opencv只支持CPU
else:   
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)


# 获取网络所有层的名称
ln = net.getLayerNames()
# yolov3有3个输出层（82，94，106），获得这3个输出层的索引后，放入ln
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

# 找到csgo窗口的句柄
hwnd = win32gui.FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')
size_scale = 2
while True:
    start_time = time.time()

    # 获得窗口矩形框的大小（left,top,right,bottom）->（left,top,w,h）
    rect = win32gui.GetWindowRect(hwnd)
    region = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

    get_window_rect_time  = time.time()
    print(f"\nget_window_time:{get_window_rect_time-start_time}")

    # 获得此窗口矩形区域下的屏幕快照，这个矩形的区域不会随着你调整分辨率而改变
    frame = np.array(pyautogui.screenshot(region=region))
    frame_height, frame_width = frame.shape[:2]

    get_screen_time = time.time()
    print(f"get_screen_time:{get_screen_time-get_window_rect_time}")

    # 喂网络
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    get_net_time = time.time()
    print(f"run net time:{get_net_time-get_screen_time}")

    boxes = []
    confidences = []

    # 处理得到的结果
    for output in layerOutputs:
        # 对于所有识别到的框，检测其坐标，置信度，类别
        for detection in output:
            # [x,y,w,h,conf,score1,socre2,...score80]
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > 0.7 and classID == 0:
                box = detection[:4] * np.array([frame_width, frame_height, frame_width, frame_height])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                box = [x, y, int(width), int(height)]
                boxes.append(box)
                confidences.append(float(confidence))

    # 非极大值抑制，得到需要的框及其置信度
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.7, 0.6)

    get_enemy_box_time = time.time()
    print(f"get enemy box time:{get_enemy_box_time-get_net_time}")

    # Calculate distance for picking the closest enemy from crosshair
    # 计算距离准星最近的敌人的距离
    if len(indices) > 0:
        print(f"Detected animies:{len(indices)}")
        min = 99999
        min_at = 0
        for i in indices.flatten():
            # [x,y]是框的左上角的坐标
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

            dist = math.sqrt(math.pow(frame_width/2 - (x+w/2), 2) + math.pow(frame_height/2 - (y+h/2), 2))
            if dist < min:
                min = dist
                min_at = i

        # boxes[min_at] = [x,y,w,h]; 这里x,y是框左上角的坐标
        # 经过如下重新计算，获得人物头的坐标。x = x + w/2 + left_top; y = y + h/7 + right_top
        # 注意，此时获得的坐标是相对于游戏窗口的左上角而言的，
        x = int(boxes[min_at][0] + boxes[min_at][2]/2) + rect[0]
        y = int(boxes[min_at][1] + boxes[min_at][3]/7) + rect[1]# For head shot

        get_front_sight_axis = time.time()
        print(f"get front sight axis time{get_front_sight_axis-get_enemy_box_time}")
        # 使用win32api移动鼠标并射击的时间是5-10ms，使用pyautogui则是200ms
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        # pyautogui.moveTo(x,y)
        # pyautogui.click()
        end_time = time.time()
        print(f"move mouse and shoot time:{end_time-get_front_sight_axis}")
        print(f"tortoal time:{end_time-start_time}")
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (int(frame.shape[1] / size_scale), int(frame.shape[0] / size_scale)))
    cv2.imshow("frame", frame)
    cv2.waitKey(1)

    # 接收到q时，程序终止
    if keyboard.is_pressed('q'):  # if key 'q' is pressed
        print('QUIT!')
        cv2.destroyAllWindows()
        break  # finishing the loop
    # 接收到p时，暂停3s
    if keyboard.is_pressed('p'):  # if key 'q' is pressed
        print('PARSE 3S')
        time.sleep(3)
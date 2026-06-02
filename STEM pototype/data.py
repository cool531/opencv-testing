import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import os
import time

# --- 1. สร้างโฟลเดอร์สำหรับเก็บรูปเทรน ถ้ายังไม่มี ---
output_dir = "my_dataset"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f":file_folder: สร้างโฟลเดอร์ {output_dir} ให้เรียบร้อยแล้วมึง")

print("กำลังตามล่าหาหน้าต่างโปรแกรม Iriun Webcam...")
while True:
    windows = gw.getWindowsWithTitle('Iriun Webcam')
    if windows and not windows[0].isMinimized:
        iriun_win = windows[0]
        break
    cv2.waitKey(1000)

print(":white_check_mark: เริ่มระบบเก็บข้อมูลรัวๆ!")
print(":video_game: [วิธีเล่น]: เอาของที่จะเทรนมาวนหน้ากล้อง แล้วกดปุ่ม 's' บนคีย์บอร์ดเพื่อเซฟภาพ")
print(":octagonal_sign: กดปุ่ม 'q' เพื่อเลิกเก็บภาพ")

img_counter = 1

while True:
    x, y, width, height = iriun_win.left, iriun_win.top, iriun_win.width, iriun_win.height
    if width <= 0 or height <= 0: continue

    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # วาดหน้าต่างโชว์ภาพสด
    preview_frame = frame.copy()
    cv2.putText(preview_frame, f"Saved Images: {img_counter-1}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow('Dataset Collector Mode', preview_frame)

    key = cv2.waitKey(1) & 0xFF
    
    # :camera_with_flash: กด 's' เพื่อเซฟภาพวัตถุนั้นๆ ในมุมปัจจุบัน
    if key == ord('s'):
        img_name = os.path.join(output_dir, f"target_obj_{img_counter}.jpg")
        cv2.imwrite(img_name, frame)
        print(f":camera_with_flash: เซฟรูปที่ {img_counter} สำเร็จ -> {img_name}")
        img_counter += 1
        time.sleep(0.1) # ป้องกันการกดเบิ้ลรัวเกินไป

    # กด 'q' เพื่อออก
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
print(f":checkered_flag: เก็บภาพเสร็จสิ้น! มึงได้รูปทั้งหมด {img_counter-1} รูป ไปเช็กดูในโฟลเดอร์ {output_dir} ได้เลย")
import subprocess


def inject_to_wireshark(filter_text: str):
  # ---  เอาข้อความใส่ Clipboard ---
  # ปกติใน Terminal เราพิมพ์: xclip -selection clipboard
  
  subprocess.run(
      ["xclip", "-selection", "clipboard"],  # <-- เติมคำสั่ง xclip แยกทีละคำ
      input=filter_text,  # <-- ใส่ชื่อตัวแปรข้อความที่รับเข้ามา
      text=True,
      check=True,
  )

  # ---  xdotool ควบคุมหน้าต่าง Wireshark ---
  subprocess.run(
      [
          "xdotool",
          "search",
          "--onlyvisible",
          "--class",
          "wireshark",  
          "windowactivate",
          "--sync",
          "key",
          "ctrl+/",  # <-- 2. คีย์ลัดกระโดดไปช่อง Filter
          "ctrl+a",  # <-- 3. คีย์ลัดคลุมดำของเก่า (ctrl+a)
          "ctrl+v",  # <-- 4. คีย์ลัดวางข้อความ
          "Return",  # <-- 5. ปุ่ม Enter
      ],
      check=True,
  )


if __name__ == "__main__":
  try:
   
    inject_to_wireshark("ip.addr == 192.168.200.21")
    print("ส่งคำสั่งเข้า Wireshark สำเร็จ!")
  except subprocess.CalledProcessError:
    print("Error: หาหน้าต่าง Wireshark ไม่เจอ (เปิดโปรแกรมทิ้งไว้หรือยัง?)")
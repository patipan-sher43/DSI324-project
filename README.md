# DSI324-project
CIS-Curriculum Checking System
คู่มือการติดตั้ง
สำหรับผู้ที่ต้องการจะนำไปใช้ ขอให้ศึกษารายละเอียดการใช้งานดังต่อไปนี้
1. ส่วนประกอบใน reposity ccstu นี้ จะประกอบไปด้วย
  - ไฟล์ main.py ซึ่งเป็นไฟล์หลักในการรันงาน
  - Dockerfile สำหรับการเซ็ต Container
  - requirements.txt สำหรับการติดตั้ง Library ที่จำเป็นต่อการใช้งาน
  - subjects_text.csv และ curriculum_format-DSI.csv ใช้สำหรับการะนำเข้าข้อมูลรายวิชาและแผนการเรียนลงใน Database
  - โฟลเดอร์ website จะรวบรวมไฟล์ที่ใช้รันหน้าเว็บต่างๆ รวมถึงการทำ authentication และมี templates ที่รวบรวมหน้าเว็บทุกหน้าที่เกี่ยวข้องกับระบบ และ static ที่เก็บรูปภาพต่างๆ
2. การรัน Project
สำหรับการรันเบื้องต้น จะใช้ Azure Virtual Machine มาช่วยในการ Deploy เว็บเป็น public โดยจะต้องสร้าง Virtual Machine และทำการเข้าระบบโดยใช้ SSH จากนั้นทำการรันโค้ดดังต่อไปนี้
  - <code>sudo apt-get update</code>

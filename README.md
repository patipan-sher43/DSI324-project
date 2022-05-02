# DSI324-project
## CIS-Curriculum Checking System
คู่มือการติดตั้ง <br>
สำหรับผู้ที่ต้องการจะนำไปใช้ ขอให้ศึกษารายละเอียดการใช้งานดังต่อไปนี้
1. ส่วนประกอบใน reposity ccstu นี้ จะประกอบไปด้วย
  - ไฟล์ main.py ซึ่งเป็นไฟล์หลักในการรันงาน
  - Dockerfile สำหรับการเซ็ต Container
  - requirements.txt สำหรับการติดตั้ง Library ที่จำเป็นต่อการใช้งาน
  - subjects_text.csv และ curriculum_format-DSI.csv ใช้สำหรับการะนำเข้าข้อมูลรายวิชาและแผนการเรียนลงใน Database
  - โฟลเดอร์ website จะรวบรวมไฟล์ที่ใช้รันหน้าเว็บต่างๆ รวมถึงการทำ authentication และมี templates ที่รวบรวมหน้าเว็บทุกหน้าที่เกี่ยวข้องกับระบบ และ static ที่เก็บรูปภาพต่างๆ

2. การรัน Project เบื้องต้น
สำหรับการรันเบื้องต้น จะใช้ Azure Virtual Machine มาช่วยในการ Deploy เว็บเป็น public โดยจะต้องสร้าง Virtual Machine และทำการเข้าระบบโดยใช้ SSH จากนั้นทำการรันโค้ดดังต่อไปนี้
  - <code>sudo apt-get update</code>
  - <code>sudo apt-get upgrade</code>
  - <code>sudo apt-get install docker.io</code>
ในส่วนนี้ ผู้ใช้จะต้องทำการสร้าง group ใหม่ที่ชื่อ docker ก่อน เพื่อการเรียกใช้งานที่สะดวก ดังนี้
  - สร้าง <code>docker</code> group
    <code>sudo groupadd docker</code>
  - เพิ่ม user ของคุณไปยัง <code>docker</code>
    <code>sudo usermod -aG docker $USER</code>
  - Activate ตัว group
    <code>newgrp docker</code>
  - ทดสอบการใช้ <code>docker</code>
    <code>docker run hello-world</code>
  
3. การนำไฟล์ Github มาใช้และ Deploy
ก่อนการ Deploy จะต้องติดตั้ง <code>docker-compose</code> ลงบน Virtual Machine ของตน โดยใช้ <code>sudo apt-get install docker-compose</code>
แล้วทำการนำไฟล์ Github เข้าสู่ Virtual Machine โดยใช้ <code>git clone <Your Github Link></code> เมื่อนำเข้าแล้ว ใช้คำสั่ง <code>cd <Your Project Name></code> เพื่อเข้าไปยัง Reposity ของ Github ที่ได้สร้างไว้
จากนั้นใช้คำสั่ง <code>docker-compose up</code> เพื่อทำการ Deploy ตัวเว็บไซต์ต่อไป
  
<b>ปัญหาที่พบ</b>
- Google Login ถึงแม้จะเลือก Account เพื่อเข้าสู่ระบบได้ แต่มีปัญหาในส่วน Callback ที่ไม่สามารถดึงเอา Public IP Address มาใช้ได้ ซึ่งถ้าจะแก้ไขปัญหานี้ ต้องใช้วิธีการสร้าง Web App ใน Azure Web Service เพื่อเอา Domain ที่เราสร้าง ไปใช้

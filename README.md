# คู่มือการติดตั้ง CIS-Curriculum Checking System

สำหรับผู้ที่ต้องการจะนำไปใช้ ขอให้ศึกษารายละเอียดการใช้งานดังต่อไปนี้
1. ส่วนประกอบใน Directory ซึ่งจะใช้ Branch <code>main</code> ในการอัปเดตไฟล์เป็นหลัก

    1.1 โฟลเดอร์ web ประกอบด้วย
      - ไฟล์ <code>main.py</code> ซึ่งเป็นไฟล์หลักในการรันงาน
      - <code>Dockerfile</code> สำหรับการเซ็ต Container
      - <code>requirements.txt</code> สำหรับการติดตั้ง Library ที่จำเป็นต่อการใช้งาน
      - <code>subjects_text.csv</code> และ <code>curriculum_format-DSI.csv</code> ใช้สำหรับการนำเข้าข้อมูลรายวิชาและแผนการเรียนลงใน Database
      - โฟลเดอร์ website จะรวบรวมไฟล์ที่ใช้รันหน้าเว็บต่างๆ รวมถึงการทำ Authentication และมี templates ที่รวบรวมหน้าเว็บทุกหน้าที่เกี่ยวข้องกับระบบ และ static ที่เก็บรูปภาพต่างๆ

    1.2 โฟลเดอร์ mysql ซึ่งเก็บไฟล์ script ในการสร้าง Database ชื่อ <code>curriculum_dataset</code> และ <code>db_custom_init.sh</code> ในการเรียกใช้ไฟล์ script ไปสร้างใน Docker container
  
    1.3 <code>docker-compose.yml</code> เป็นไฟล์ในการ Deploy ตัว web และ Database (mysql) ขึ้นสู่ Services

2. การรัน Project เบื้องต้น
    
    2.1 การรันบน localhost
    
      ผู้ใช้สามารถทำการรันคำสั่ง <code>git clone \<link from GitHub\></code> เพื่อทำการดึงมาใส่ในโฟลเดอร์ของผู้ใช้ได้ และทำการกดรันหน้า <code>main.py</code> ได้เลย ซึ่งในที่นี้ขอแนะนำให้ใช้โปรแกรม Visual Studio Code ในการรัน
        
    2.2 การรันบน Azure Virtual Machine (โดยใช้ Windows Powershell)

    สำหรับการรันเบื้องต้น จะใช้ Azure Virtual Machine มาช่วยในการ Deploy เว็บเป็น Public โดยจะต้องสร้าง Virtual Machine และทำการเข้าระบบโดยใช้ SSH จากนั้นทำการรันโค้ดดังต่อไปนี้
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
แล้วทำการนำไฟล์ Github เข้าสู่ Virtual Machine โดยใช้ <code>git clone \<Your Github Link\></code> เมื่อนำเข้าแล้ว ใช้คำสั่ง <code>cd \<Your Project Name\></code> เพื่อเข้าไปยัง Reposity ของ Github ที่ได้สร้างไว้
จากนั้นใช้คำสั่ง <code>docker-compose up</code> เพื่อทำการ Deploy ตัวเว็บไซต์ต่อไป
  
    ในการรัน <code>docker-compose up</code> <b>จะต้องรัน 2 ครั้ง</b> ครั้งแรกเป็นการเรียกเพื่อสร้าง Database โดยใช้คำสั่ง <code>docker-compose up --build</code> เมื่อสร้างแล้ว จึงทำการสิ้นสุดการทำงานโดยใช้คำสั่ง <code>CTRL + C</code> ส่วนครั้งที่ 2 จะเป็นการเรียกใช้ Web โดยใช้คำสั่ง <code>docker-compose up</code> แบบปกติ
  
<b>ปัญหาที่พบ</b>
- Google Login ถึงแม้จะเลือก Account เพื่อเข้าสู่ระบบได้ แต่มีปัญหาในส่วน Callback ที่ไม่สามารถดึงเอา Public IP Address มาใช้ได้ ซึ่งถ้าจะแก้ไขปัญหานี้ ต้องใช้วิธีการสร้าง Web App ใน Azure Web Service เพื่อเอา Domain ที่เราสร้าง ไปใช้

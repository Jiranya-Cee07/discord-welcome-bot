import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
import threading

# ============================
# 1️⃣ โหลด .env
# ============================
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # ช่องที่ bot ส่งข้อความ

# ============================
# 2️⃣ ตั้งค่า Intents
# ============================
intents = discord.Intents.default()
intents.members = True           # ต้องเปิดเพื่อจับสมาชิกเข้าร่วม
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ============================
# 3️⃣ ตัวแปรเก็บสมาชิกใหม่
# ============================
new_members = []

# ============================
# 4️⃣ Event เมื่อ bot พร้อมใช้งาน
# ============================
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    print("Bot พร้อมแล้ว 🎉")

# ============================
# 5️⃣ Event เมื่อมีสมาชิกใหม่เข้ามา
# ============================
@bot.event
async def on_member_join(member):
    global new_members
    # ป้องกันสมาชิกซ้ำ
    if member.id not in new_members:
        new_members.append(member.id)
        print(f"New member joined: {member} | Current list: {new_members}")

    # ส่งข้อความเมื่อครบ 3 คน
    if len(new_members) >= 3:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            message = f"""
<:wohhh:1429073221050957916> ˚ ༘♡ ·˚꒰𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐌𝐚𝐞𝐦𝐢꒱ ₊˚ˑ༄ <:wohhh:1429073221050957916>
**ยินดีต้อนรับคุณ <@{new_members[0]}> <@{new_members[1]}> <@{new_members[2]}> ด้วยนะคะ ว่างๆเหงาๆแวะมาพูดคุยหน้าแชทด้วยกันได้น้าหรือจะลงห้องก็ด้าย**
**เเต่อย่าลืมอ่านกฏที่ห้อง <#1428939262832672925> ด้วยนะคะ**

**↶ೃ✧˚.ทางดิสเรามีการรับสมัครทีมงาน ❃ ↷ ˊ-**

**สามารถอ่านเกณฑ์การรับสมัครได้ที่ <#1439484355767697581>**

**รายละเอียดเเต่ละตำเหน่งที่ <#1439484305280733214>**

**เเละหากสนใจมาร่วมงานสามารถมากรอกใบสมัครได้ที่ <#1439484389682839632>**

**เเล้วมาร่วมงานกันเยอะๆน้าขอให้เป็นวันที่ดีค่ะ <:nommm:1429075604875120680>**
───✱.｡:｡✱↶ೃ ❃ ↷ ˊ-.:｡✧*.｡✰ ───
"""
            await channel.send(message)
            print("Message sent:", message)

        # ล้าง list หลังส่ง → เริ่มรอบใหม่
        new_members.clear()

# ============================
# 6️⃣ Fake HTTP server สำหรับ Render
# ============================
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=1000)

# รัน Flask ใน Thread แยก
threading.Thread(target=run_flask).start()

# ============================
# 7️⃣ Run Discord bot
# ============================
bot.run(TOKEN)


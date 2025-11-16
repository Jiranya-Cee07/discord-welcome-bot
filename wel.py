import os
import threading
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask

# ============================
# 1️⃣ โหลด .env
# ============================
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# ============================
# 2️⃣ ตั้งค่า Intents
# ============================
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

new_members = []

# ============================
# 3️⃣ Discord Events
# ============================
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}! Bot พร้อมแล้ว 🎉')


@bot.event
async def on_member_join(member):
    global new_members

    if member.id not in new_members:
        new_members.append(member.id)

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

        new_members.clear()

# ============================
# 4️⃣ Flask Server (ให้ Render Detect Port)
# ============================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    print("Running Flask on port", port)
    app.run(host="0.0.0.0", port=port)


# ============================
# 5️⃣ Run Discord Bot + Flask
# ============================
if __name__ == "__main__":
    # รัน Flask แบบ background thread
    threading.Thread(target=run_flask).start()

    # รันบอท
    bot.run(TOKEN)


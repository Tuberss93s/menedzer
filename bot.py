import discord
import re
import os
import asyncio

# --- KONFIGURACJA (ZMIEŃ TYLKO TO) ---
TOKEN = os.getenv('DISCORD_TOKEN') 
KANAL_PARTNERSTWA_ID = 1476971697507795177
KANAL_KORE_LOGS_ID = 1480639848862716185 
ADMIN_ID = 1347691963008286781

class UltimateKore(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ostatni_serwer = "ᴡᴄᴢʏᴛʏᴡᴀɴɪᴇ..."
        self.uzyte_serwery = {}
        self.zablokowani_uzytkownicy = set()
        self.aktywne_sesje = {} 
        self.manual_offset = 0 

    async def load_db_from_discord(self):
        await self.wait_until_ready()
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)
        
        if log_ch:
            found_last = False
            async for msg in log_ch.history(limit=1000):
                if "⚙️ MANUAL_OFFSET:" in msg.content:
                    m_off = re.search(r'MANUAL_OFFSET: (-?\d+)', msg.content)
                    if m_off: self.manual_offset = int(m_off.group(1))

                m_srv = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if m_srv:
                    srv_id = m_srv.group(1)
                    m_part_msg = re.search(r'MSG_PART_ID: (\d+)', msg.content)
                    part_id = int(m_part_msg.group(1)) if m_part_msg else None
                    self.uzyte_serwery[srv_id] = [msg.id, part_id]
                    if not found_last:
                        n_match = re.search(r'🏠 sᴇʀᴡᴇʀ: (.+)', msg.content)
                        if n_match: self.ostatni_serwer, found_last = n_match.group(1), True

        if part_ch:
            async for msg in part_ch.history(limit=300):
                inv = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', msg.content)
                if inv:
                    try:
                        invite = await self.fetch_invite(inv.group(0))
                        sid = str(invite.guild.id)
                        if sid not in self.uzyte_serwery: self.uzyte_serwery[sid] = ["EXISTING", msg.id]
                    except: continue
        
        if self.ostatni_serwer == "ᴡᴄᴢʏᴛʏᴡᴀɴɪᴇ...": self.ostatni_serwer = "Brak"

    async def status_rotator(self):
        await self.wait_until_ready()
        while not self.is_closed():
            curr_count = len(self.uzyte_serwery) + self.manual_offset
            msgs = [
                "⚙️ ᴅᴇᴠᴇʟᴏᴘᴇʀ @ᴋɪᴛsᴜɴᴇ_𝟸𝟻𝟸𝟶ᴢᴀᴘᴀs",
                "✅ ᴄᴢᴇᴋᴀɴɪᴇ ɴᴀ ᴘᴀʀᴛɴᴇʀsᴛᴡᴀ",
                "🛠️ ᴍᴀᴅᴇ ɪɴ ᴋᴏʀᴇ sʜ𝟶ᴘ",
                "💎 discord.gg/9jUSJcT2PF",
                f"🤝 ᴏsᴛᴀᴛɴɪᴇ: {self.ostatni_serwer}",
                f"📊 ᴘᴀʀᴛɴᴇʀsᴛᴡ: {curr_count}",
                "🚀 ɴᴀᴊsᴢʏʙsᴢᴀ ʀᴇᴀʟɪᴢᴀᴄᴊᴀ"
            ]
            for m in msgs:
                try:
                    await self.change_presence(activity=discord.CustomActivity(name=m))
                    await asyncio.sleep(12) 
                except: pass

    async def on_ready(self):
        print("🚀 BOT GOTOWY"); self.loop.create_task(self.status_rotator()); self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)

        # ADMIN CMDS
        if message.author.id == ADMIN_ID:
            if message.content.startswith("!ustaw"):
                try:
                    val = int(message.content.split()[1])
                    self.manual_offset = val - len(self.uzyte_serwery)
                    if log_ch: await log_ch.send(f"⚙️ MANUAL_OFFSET: {self.manual_offset}")
                    await message.channel.send(f"✅ Ustawiono na `{val}`"); return
                except: pass

        # DM SYSTEM
        if not isinstance(message.channel, discord.DMChannel): return
        
        if "@everyone" in message.content.lower() or "@here" in message.content.lower():
            await message.channel.send("⚠️ **Zakaz używania pingów!**"); return

        if "PARTNERSTWO" in message.content.upper():
            self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()
            reklama = (
                "# 💎 **ᴋᴏʀᴇ sʜ0ᴘ — ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇs** 💎\n\n"
                "🎮 **ᴏғᴇʀᴛᴀ:**\n"
                "┕ 〢📱 **ᴅ𝟷sᴄᴏʀᴅ:** Nitro, Boosty\n"
                "┕ 〢🕹️ **ɢʀʏ:** Minecraft (60zł), Roblox (20zł), Valorant (30zł)\n"
                "┕ 〢⚡ **ᴍᴇᴍʙᴇʀs:** 1k (20zł), 5k (35zł), 10k (80zł)\n\n"
                "🔗 **ᴅᴏᴌᴀ̨ᴄᴢ:** https://discord.gg/9jUSJcT2PF\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )
            await message.channel.send(reklama)
            await message.channel.send("🤝 **ᴋᴚᴏᴋɪ:**\n1. Skopiuj reklamę wyżej i wstaw u siebie.\n2. Wklej swoją reklamę tutaj.\n3. Napisz **GOTOWE**.")

        if "GOTOWE" in message.content.upper():
            if message.author.id not in self.aktywne_sesje: return
            t_rek, i_url = None, None
            async for m in message.channel.history(limit=10):
                if "@everyone" in m.content.lower() or "@here" in m.content.lower(): continue
                inv = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', m.content)
                if inv and "9jUSJcT2PF" not in inv.group(0): t_rek, i_url = m.content, inv.group(0); break
            
            if t_rek:
                try:
                    inv_obj = await self.fetch_invite(i_url)
                    sid = str(inv_obj.guild.id)
                    if sid in self.uzyte_serwery:
                        await message.channel.send("❌ Serwer już istnieje!"); return
                    
                    p_msg = await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\n{t_rek}")
                    if log_ch: await log_ch.send(f"📂 **LOG**\nID_SERWERA: {sid}\n🏠 sᴇʀᴡᴇʀ: {inv_obj.guild.name}\nID_USER: {message.author.id}")
                    
                    self.uzyte_serwery[sid] = ["NEW", p_msg.id]
                    self.ostatni_serwer = inv_obj.guild.name
                    await message.channel.send("✅ **Gotowe!**")
                except: await message.channel.send("❌ Błędny link.")

client = UltimateKore(); client.run(TOKEN)

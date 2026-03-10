import discord
import re
import os
import asyncio
from datetime import datetime

# --- KONFIGURACJA ---
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
        """Wczytywanie logów i bazy z historii kanałów"""
        await self.wait_until_ready()
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)
        
        if log_ch:
            async for msg in log_ch.history(limit=2000):
                # Wczytywanie offsetu
                if "⚙️ MANUAL_OFFSET:" in msg.content:
                    m_off = re.search(r'MANUAL_OFFSET: (-?\d+)', msg.content)
                    if m_off: self.manual_offset = int(m_off.group(1))

                # Wczytywanie serwerów
                m_srv = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if m_srv:
                    srv_id = m_srv.group(1)
                    self.uzyte_serwery[srv_id] = ["LOADED", msg.id]
                    if self.ostatni_serwer == "ᴡᴄᴢʏᴛʏᴡᴀɴɪᴇ...":
                        n_match = re.search(r'🏠 sᴇʀᴡᴇʀ: (.+)', msg.content)
                        if n_match: self.ostatni_serwer = n_match.group(1)
                
                # Wczytywanie blokad
                if "🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ:" in msg.content:
                    uid = re.search(r'🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ: (\d+)', msg.content)
                    if uid: self.zablokowani_uzytkownicy.add(int(uid.group(1)))

        print(f"✅ System gotowy. Baza: {len(self.uzyte_serwery)}, Offset: {self.manual_offset}")

    async def status_rotator(self):
        """Dynamiczny status bota"""
        await self.wait_until_ready()
        while not self.is_closed():
            curr_count = len(self.uzyte_serwery) + self.manual_offset
            msgs = [
                "⚙️ ᴅᴇᴠᴇʟᴏᴘᴇʀ @ᴋɪᴛsᴜɴᴇ_𝟸𝟻𝟸𝟶ᴢᴀᴘᴀs",
                "✅ ᴏɴʟɪɴᴇ 𝟸𝟺/𝟽",
                "🛠️ ᴍᴀᴅᴇ ɪɴ ᴋᴏʀᴇ sʜ𝟶ᴘ",
                "💎 discord.gg/9jUSJcT2PF",
                f"🤝 ᴏsᴛᴀᴛɴɪᴇ: {self.ostatni_serwer}",
                f"📊 ᴘᴀʀᴛɴᴇʀsᴛᴡ: {curr_count}",
                "🚀 sᴢʏʙᴋᴀ ᴡᴇʀʏꜰɪᴋᴀᴄᴊᴀ"
            ]
            for m in msgs:
                try:
                    await self.change_presence(activity=discord.CustomActivity(name=m))
                    await asyncio.sleep(10) 
                except: pass

    async def on_ready(self):
        print(f"🚀 Połączono jako {self.user}"); self.loop.create_task(self.status_rotator()); self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)

        # --- PANEL ADMINA ---
        if message.author.id == ADMIN_ID:
            if message.content.startswith("!ustaw"):
                try:
                    val = int(message.content.split()[1])
                    self.manual_offset = val - len(self.uzyte_serwery)
                    if log_ch: await log_ch.send(f"⚙️ MANUAL_OFFSET: {self.manual_offset}")
                    await message.channel.send(f"✅ Licznik skorygowany na `{val}`."); return
                except: pass

            if message.content == "!status":
                total = len(self.uzyte_serwery) + self.manual_offset
                await message.channel.send(f"📊 **sᴛᴀᴛʏsᴛʏᴋɪ**\n┕ ʟɪᴄᴢɴɪᴋ: `{total}`\n┕ ᴡ ʙᴀᴢɪᴇ: `{len(self.uzyte_serwery)}` \n┕ ʙʟᴏᴋᴀᴅʏ: `{len(self.zablokowani_uzytkownicy)}` osób"); return

        # --- SYSTEM DM ---
        if not isinstance(message.channel, discord.DMChannel): return
        
        content_lower = message.content.lower()
        
        # ANTY-PING Z LOGOWANIEM
        if "@everyone" in content_lower or "@here" in content_lower:
            await message.channel.send("⚠️ **ᴛᴏ ɴɪᴇ ᴅᴢɪᴀᴌᴀ!**\nUżywanie pingów jest zablokowane. Wyślij reklamę bez nich."); 
            if log_ch: await log_ch.send(f"🚨 **PRÓBA PINGU:** {message.author} ({message.author.id})"); return

        # START PARTNERSTWA
        if "partnerstwo" in content_lower:
            if message.author.id in self.zablokowani_uzytkownicy:
                await message.channel.send("❌ Twoje konto jest zablokowane u nas."); return
            
            self.aktywne_sesje[message.author.id] = datetime.now()
            reklama_to_copy = (
                "# 💎 **ᴋᴏʀᴇ sʜ0ᴘ — ᴘʀᴇᴍɪᴜᴍ ᴅɪsᴄᴏʀᴅ sᴇʀᴠɪᴄᴇs** 💎\n\n"
                "🎮 **ɴᴀsᴢᴀ ᴏғᴇʀᴛᴀ:**\n"
                "┕ 〢📱 **ᴅ𝟷sᴄᴏʀᴅ:** Nitro, Boosty\n"
                "┕ 〢🕹️ **ɢʀʏ:** Minecraft (60zł), Roblox (20zł), Valorant (30zł)\n"
                "┕ 〢⚡ **ᴍᴇᴍʙᴇʀs:** 1k (20zł), 5k (35zł), 10k (80zł)\n\n"
                "🔗 **ᴅᴏᴌᴀ̨ᴄᴢ:** https://discord.gg/9jUSJcT2PF\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )
            await message.channel.send(reklama_to_copy)
            await message.channel.send("🤝 **ᴋᴚᴏᴋɪ:**\n1️⃣ Skopiuj reklamę wyżej i wstaw na swój kanał.\n2️⃣ Wklej **tutaj** swoją reklamę.\n3️⃣ Napisz **GOTOWE**.")

        # FINALIZACJA
        if "gotowe" in content_lower:
            if message.author.id not in self.aktywne_sesje:
                await message.channel.send("❌ Najpierw napisz `Partnerstwo`!"); return
            
            t_rek, i_url = None, None
            async for m in message.channel.history(limit=10):
                if m.author.id == self.user.id: continue
                if "@everyone" in m.content.lower() or "@here" in m.content.lower(): continue
                
                inv = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', m.content)
                if inv and "9jUSJcT2PF" not in inv.group(0): 
                    t_rek, i_url = m.content.strip(), inv.group(0); break
            
            if not t_rek:
                await message.channel.send("❌ Nie znalazłem Twojej reklamy (pamiętaj: bez pingów!)."); return
            
            try:
                inv_obj = await self.fetch_invite(i_url)
                sid = str(inv_obj.guild.id)
                
                if sid in self.uzyte_serwery:
                    await message.channel.send("❌ Ten serwer już z nami współpracuje!"); return
                
                # Wysłanie na kanał partnerstw
                p_msg = await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nᴏᴅ: {message.author.mention}\n\n{t_rek}")
                
                # Logowanie
                time_diff = (datetime.now() - self.aktywne_sesje[message.author.id]).seconds
                if log_ch:
                    await log_ch.send(f"📂 **LOG PARTNERSTWA**\n🏠 sᴇʀᴡᴇʀ: **{inv_obj.guild.name}**\n🆔 ID_SERWERA: {sid}\n👤 ᴜᴢʏᴛᴋᴏᴡɴɪᴋ: {message.author}\n⏱️ ᴄᴢᴀs: {time_diff}s\n🔗 ʟɪɴᴋ: {i_url}")
                
                self.uzyte_serwery[sid] = ["NEW", p_msg.id]
                self.ostatni_serwer = inv_obj.guild.name
                del self.aktywne_sesje[message.author.id]
                
                await message.channel.send(f"✅ **Sukces!** Partnerstwo zawarte w {time_diff} sekund. Dzięki!")
            except:
                await message.channel.send("❌ Link do serwera jest nieprawidłowy lub wygasł."); return

client = UltimateKore(); client.run(TOKEN)

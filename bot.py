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
        await self.wait_until_ready()
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        if log_ch:
            async for msg in log_ch.history(limit=2000):
                if "⚙️ MANUAL_OFFSET:" in msg.content:
                    m_off = re.search(r'MANUAL_OFFSET: (-?\d+)', msg.content)
                    if m_off: self.manual_offset = int(m_off.group(1))

                m_srv = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if m_srv:
                    srv_id = m_srv.group(1)
                    self.uzyte_serwery[srv_id] = ["LOADED", msg.id]
                    if self.ostatni_serwer == "ᴡᴄᴢʏᴛʏᴡᴀɴɪᴇ...":
                        n_match = re.search(r'🏠 sᴇʀᴡᴇʀ: (.+)', msg.content)
                        if n_match: self.ostatni_serwer = n_match.group(1)
                
                if "🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ:" in msg.content:
                    uid = re.search(r'🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ: (\d+)', msg.content)
                    if uid: self.zablokowani_uzytkownicy.add(int(uid.group(1)))
                
                if "🔓 ᴜɴʙʟᴏᴄᴋᴇᴅ_ᴜsᴇʀ:" in msg.content:
                    uid = re.search(r'🔓 ᴜɴʙʟᴏᴄᴋᴇᴅ_ᴜsᴇʀ: (\d+)', msg.content)
                    if uid:
                        u_id_int = int(uid.group(1))
                        if u_id_int in self.zablokowani_uzytkownicy: self.zablokowani_uzytkownicy.remove(u_id_int)

    async def status_rotator(self):
        await self.wait_until_ready()
        while not self.is_closed():
            curr_count = len(self.uzyte_serwery) + self.manual_offset
            msgs = [
                "⚙️ ᴅᴇᴠᴇʟᴏᴘᴇʀ @ᴋɪᴛsᴜɴᴇ_𝟸𝟻𝟸𝟶ᴢᴀᴘᴀs",
                "🛠️ ᴍᴀᴅᴇ ɪɴ ᴋᴏʀᴇ sʜ𝟶ᴘ",
                "💎 discord.gg/9jUSJcT2PF",
                f"🤝 ᴏsᴛᴀᴛɴɪᴇ: {self.ostatni_serwer}",
                f"📊 ᴘᴀʀᴛɴᴇʀsᴛᴡ: {curr_count}",
                "🚀 sᴢʏʙᴋᴀ ᴡᴇʀʏꜰɪᴋᴀᴄᴊᴀ"
            ]
            for m in msgs:
                try:
                    await self.change_presence(activity=discord.CustomActivity(name=m))
                    await asyncio.sleep(12) 
                except: pass

    async def on_ready(self):
        print(f"🚀 KORE ONLINE"); self.loop.create_task(self.status_rotator()); self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)

        # --- PEŁNY PANEL ADMINA ---
        if message.author.id == ADMIN_ID:
            if message.content == "!help":
                h = (
                    "🛠️ **ᴋᴏʀᴇ sᴇʟғ-ʙᴏᴛ | ᴘᴀɴᴇʟ ᴀᴅᴍɪɴᴀ**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "┕ `!status` - Statystyki bazy i licznika\n"
                    "┕ `!ustaw [liczba]` - Ustawia licznik partnerstw\n"
                    "┕ `!usun [ID_SERWERA]` - Usuwa serwer z bazy\n"
                    "┕ `!potwierdz [ID_USER]` - Odblokowuje użytkownika\n"
                    "┕ `!blokuj [ID_USER]` - Ręczne blokowanie oszusta\n"
                    "━━━━━━━━━━━━━━━━━━━━"
                )
                await message.channel.send(h); return

            if message.content.startswith("!ustaw"):
                try:
                    val = int(message.content.split()[1])
                    self.manual_offset = val - len(self.uzyte_serwery)
                    if log_ch: await log_ch.send(f"⚙️ MANUAL_OFFSET: {self.manual_offset}")
                    await message.channel.send(f"✅ Licznik ustawiony na `{val}`."); return
                except: pass

            if message.content == "!status":
                total = len(self.uzyte_serwery) + self.manual_offset
                await message.channel.send(f"📊 **sᴛᴀᴛʏsᴛʏᴋɪ**\n┕ ʟɪᴄᴢɴɪᴋ: `{total}`\n┕ ʙᴀᴢᴀ: `{len(self.uzyte_serwery)}` \n┕ ʙʟᴏᴋᴀᴅʏ: `{len(self.zablokowani_uzytkownicy)}` osób"); return

            if message.content.startswith("!usun"):
                parts = message.content.split()
                if len(parts) > 1:
                    sid = parts[1]
                    if sid in self.uzyte_serwery:
                        del self.uzyte_serwery[sid]
                        await message.channel.send(f"✅ Serwer `{sid}` usunięty z pamięci bota."); return
                    else:
                        await message.channel.send("❌ Nie znaleziono tego ID w bazie."); return

            if message.content.startswith("!potwierdz"):
                try:
                    uid = int(message.content.split()[1])
                    if uid in self.zablokowani_uzytkownicy:
                        self.zablokosani_uzytkownicy.remove(uid)
                        if log_ch: await log_ch.send(f"🔓 ᴜɴʙʟᴏᴄᴋᴇᴅ_ᴜsᴇʀ: {uid}")
                        await message.channel.send(f"✅ Użytkownik `{uid}` został odblokowany."); return
                except: pass

            if message.content.startswith("!blokuj"):
                try:
                    uid = int(message.content.split()[1])
                    self.zablokowani_uzytkownicy.add(uid)
                    if log_ch: await log_ch.send(f"🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ: {uid}")
                    await message.channel.send(f"✅ Zablokowano `{uid}`."); return
                except: pass

        # --- SYSTEM DM ---
        if not isinstance(message.channel, discord.DMChannel): return
        content_up = message.content.upper()
        
        if "@EVERYONE" in content_up or "@HERE" in content_up:
            await message.channel.send("⚠️ **Zakaz używania pingów!**"); return

        if "PARTNERSTWO" in content_up:
            if message.author.id in self.zablokowani_uzytkownicy:
                await message.channel.send("❌ Twoje konto jest zablokowane."); return
            
            self.aktywne_sesje[message.author.id] = datetime.now()
            reklama = (
                "# 💎 **ᴋᴏʀᴇ sʜ0ᴘ — ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇs** 💎\n\n"
                "🎮 **ᴏғᴇʀᴛᴀ:**\n"
                "┕ 〢📱 **ᴅ𝟷sᴄᴏʀᴅ:** Nitro, Boosty\n"
                "┕ 〢🕹️ **ɢʀʏ:** Minecraft, Roblox, Valorant\n"
                "┕ 〢⚡ **ᴍᴇᴍʙᴇʀs:** 1k (20zł), 5k (35zł), 10k (80zł)\n\n"
                "🔗 **ᴅᴏᴌᴀ̨ᴄᴢ:** https://discord.gg/9jUSJcT2PF\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )
            await message.channel.send(reklama)
            await message.channel.send("🤝 **ᴋᴚᴏᴋɪ:**\n1. Skopiuj reklamę wyżej i wstaw u siebie.\n2. Wklej swoją reklamę tutaj.\n3. Napisz **GOTOWE**.")

        if "GOTOWE" in content_up:
            if message.author.id not in self.aktywne_sesje:
                await message.channel.send("❌ Napisz najpierw `Partnerstwo`!"); return
            
            t_rek, i_url = None, None
            async for m in message.channel.history(limit=10):
                if m.author.id == self.user.id: continue
                inv = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', m.content)
                if inv and "9jUSJcT2PF" not in inv.group(0): 
                    t_rek, i_url = m.content.strip(), inv.group(0); break
            
            if not t_rek:
                await message.channel.send("❌ Nie widzę reklamy bez pingu!"); return
            
            try:
                inv_obj = await self.fetch_invite(i_url)
                sid = str(inv_obj.guild.id)
                if sid in self.uzyte_serwery:
                    await message.channel.send("❌ Ten serwer już z nami współpracuje!"); return
                
                p_msg = await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\n{t_rek}")
                if log_ch:
                    await log_ch.send(f"📂 **LOG**\n🏠 sᴇʀᴡᴇʀ: **{inv_obj.guild.name}**\n🆔 ID_SERWERA: {sid}\n👤 ᴜᴢʏᴛᴋᴏᴡɴɪᴋ: {message.author}")
                
                self.uzyte_serwery[sid] = ["NEW", p_msg.id]
                self.ostatni_serwer = inv_obj.guild.name
                del self.aktywne_sesje[message.author.id]
                await message.channel.send(f"✅ **Sukces!** Partnerstwo zawarte."); 
            except:
                await message.channel.send("❌ Link nie działa."); return

client = UltimateKore(); client.run(TOKEN)

import discord
import re
import os
import asyncio

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

    async def load_db_from_discord(self):
        await self.wait_until_ready()
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)
        
        if log_ch:
            found_last = False
            async for msg in log_ch.history(limit=500):
                m_srv = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if m_srv:
                    srv_id = m_srv.group(1)
                    m_part_msg = re.search(r'MSG_PART_ID: (\d+)', msg.content)
                    part_id = int(m_part_msg.group(1)) if m_part_msg else None
                    self.uzyte_serwery[srv_id] = [msg.id, part_id]
                    if not found_last:
                        n_match = re.search(r'🏠 sᴇʀᴡᴇʀ: (.+)', msg.content)
                        if n_match: self.ostatni_serwer, found_last = n_match.group(1), True
                
                if "🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ:" in msg.content:
                    uid = re.search(r'🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ: (\d+)', msg.content)
                    if uid: self.zablokowani_uzytkownicy.add(int(uid.group(1)))

    async def status_rotator(self):
        await self.wait_until_ready()
        while not self.is_closed():
            msgs = [
                "⚙️ ᴅᴇᴠᴇʟᴏᴘᴇʀ @ᴋɪᴛsᴜɴᴇ_𝟸𝟻𝟸𝟶ᴢᴀᴘᴀs",
                "✅ ᴄᴢᴇᴋᴀɴɪᴇ ɴᴀ ᴘᴀʀᴛɴᴇʀsᴛᴡᴀ",
                "🛠️ ᴍᴀᴅᴇ ɪɴ ᴋᴏʀᴇ sʜ𝟶ᴘ",
                "💎 discord.gg/9jUSJcT2PF",
                f"🤝 ᴏsᴛᴀᴛɴɪᴇ: {self.ostatni_serwer}",
                f"📊 ᴘᴀʀᴛɴᴇʀsᴛᴡ: {len(self.uzyte_serwery)}",
                "📦 ɴᴏᴡᴇ ᴅᴏsᴛᴀᴡʏ ᴡʟᴇᴄɪᴀᴌʏ!",
                "💳 ᴘᴌᴀᴛɴᴏsᴄɪ: ᴛʏʟᴋᴏ ᴘsᴄ 🎫",
                "🛡️ 𝟷𝟶𝟶% ʟᴇɢɪᴛ & ᴠᴇʀɪғɪᴇᴅ",
                "🎫 ᴏᴛᴡᴏ́ʀᴢ ᴛɪᴄᴋᴇᴛ ʙʏ ᴋᴜᴘɪᴄ́",
                "🚀 ɴᴀᴊsᴢʏʙsᴢᴀ ʀᴇᴀʟɪᴢᴀᴄᴊᴀ"
            ]
            for m in msgs:
                try:
                    await self.change_presence(activity=discord.CustomActivity(name=m))
                    await asyncio.sleep(12) 
                except: pass

    async def on_ready(self):
        print(f"🚀 KORE SELF-BOT ONLINE"); self.loop.create_task(self.status_rotator()); self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)
        
        if message.author.id in self.aktywne_sesje:
            self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()

        if message.author.id == ADMIN_ID:
            if message.content.startswith("!usun"):
                parts = message.content.split(' ', 2)
                if len(parts) < 2: return
                srv_id, powód = parts[1], parts[2] if len(parts) > 2 else "ʙʀᴀᴋ ʀᴇᴋʟᴀᴍʏ/ᴅᴇᴄʏ𝑧ᴊᴀ ᴀᴅᴍɪɴᴀ"
                if srv_id in self.uzyte_serwery:
                    ids = self.uzyte_serwery[srv_id]
                    if ids[1]:
                        try:
                            m_p = await part_ch.fetch_message(ids[1]); await m_p.delete()
                        except: pass
                    if ids[0] != "EXISTING":
                        try:
                            m_l = await log_ch.fetch_message(ids[0])
                            u_match = re.search(r'ID_USER: (\d+)', m_l.content)
                            if u_match:
                                uid = int(u_match.group(1))
                                self.zablokowani_uzytkownicy.add(uid)
                                await log_ch.send(f"🚫 ʙʟᴏᴋᴀᴅᴀ_ʀᴇᴛʀʏ: {uid}")
                            await m_l.delete()
                        except: pass
                    del self.uzyte_serwery[srv_id]
                    await message.channel.send(f"✅ ᴜsᴜɴɪᴇ̨ᴛᴏ ɪ ᴢᴀʙʟᴏᴋᴏᴡᴀɴᴏ `{srv_id}`.")
                return

        if not isinstance(message.channel, discord.DMChannel): return
        
        content = message.content.upper()
        if "PARTNERSTWO" in content:
            if message.author.id in self.zablokowani_uzytkownicy:
                await message.channel.send("❌ **ʙᴚᴀᴋ ᴜᴘᴚᴀᴡɴɪᴇɴ́**\nᴊᴇsᴛᴇś ᴢᴀʙʟᴏᴋᴏᴡᴀɴʏ ᴡ sʏsᴛᴇᴍɪᴇ."); return
            
            self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()
            
            reklama_msg = (
                "# 💎 **ᴋᴏʀᴇ sʜ0ᴘ — ᴘʀᴇᴍɪᴜᴍ ᴅɪsᴄᴏʀᴅ sᴇʀᴠɪᴄᴇs** 💎\n\n"
                "Szukasz profesjonalnych usług, kont do gier lub boostów? **ᴋᴏʀᴇ sʜ0ᴘ** to Twoje centrum wszystkiego!\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🎮 **ɴᴀsᴢᴀ ᴏғᴇʀᴛᴀ (ᴋᴀᴛᴇɢᴏʀɪᴇ):**\n"
                "┕ 〢📱 **ᴅ𝟷sᴄᴏʀᴅ:** Nitro, Boosty, Konta\n"
                "┕ 〢👤 **ᴋᴏɴᴛᴀ:** Premium, Waluty, Subskrypcje\n"
                "┕ 〢🕹️ **ɢʀʏ:**\n"
                "   • ᴍɪɴᴇᴄʀᴀꜰᴛ (ᴊᴀᴠᴀ & ʙᴇᴅʀᴏᴄᴋ) — **60 ᴢᴌ**\n"
                "   • ʀᴏʙʟᴏx (2009 | 15 ʏᴇᴀʀs) — **20 ᴢᴌ**\n"
                "   • ᴠᴀʟᴏʀᴀɴᴛ — **30 ᴢᴌ** | ʟᴏʟ — **65 ᴢᴌ**\n"
                "┕ 〢🛠️ **ᴍᴇᴍʙᴇʀsʜɪᴘ ᴘᴀᴄᴋs:**\n"
                "   • ⚡ **𝟷𝟶,𝟶𝟶𝟶 ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs** — **80 ᴢᴌ**\n"
                "   • ⚡ **𝟻,𝟶𝟶𝟶 ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs** — **35 ᴢᴌ**\n"
                "   • ⚡ **𝟷,𝟶,𝟶𝟶 ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs** — **20 ᴢᴌ**\n\n"
                "💳 **ᴘᴌᴀᴛɴᴏśᴄɪ ɪ ʀᴇᴀʟɪᴢᴀᴄᴊᴀ:**\n"
                "┕ 〢🎫 **ᴘᴀʏsᴀғᴇᴄᴀʀᴅ (ᴘsᴄ)** — Szybko i anonimowo\n"
                "┕ 〢🛡️ **ʟᴇɢɪᴛ:** Opinie na <#1476961244463239180>\n\n"
                "🔗 **ᴅᴏᴌᴀ̨ᴄᴢ:** https://discord.gg/9jUSJcT2PF\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )
            await message.channel.send(reklama_msg)
            await message.channel.send("🤝 **ᴋᴚᴏᴋɪ ᴅᴏ ᴢᴀᴋᴏɴ́ᴄᴢᴇɴɪᴀ:**\n𝟷. ᴡsᴛᴀᴡ ʀᴇᴋʟᴀᴍᴇ̨ ᴘᴏᴡʏᴢ̇ᴇᴊ.\n𝟸. ᴡᴋʟᴇᴊ sᴡᴏᴊᴀ̨ ᴛᴜᴛᴀᴊ.\n𝟹. ɴᴀᴘɪsᴢ **ɢᴏᴛᴏᴡᴇ**.")

        if "GOTOWE" in content:
            if message.author.id not in self.aktywne_sesje: return
            t_rek, i_url = None, None
            async for m in message.channel.history(limit=10):
                inv = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', m.content)
                if inv and "9jUSJcT2PF" not in inv.group(0): t_rek, i_url = m.content, inv.group(0); break
            
            if not t_rek:
                await message.channel.send("❌ **ɴɪᴇ ᴡᴋʟᴇɪᴌᴇś ʀᴇᴋʟᴀᴍʏ!**"); return
            
            try:
                inv_obj = await self.fetch_invite(i_url)
                if str(inv_obj.guild.id) in self.uzyte_serwery:
                    await message.channel.send("❌ **sᴇʀᴡᴇʀ ᴊᴜᴢ̇ ɪsᴛɴɪᴇᴊᴇ ᴡ ʙᴀᴢɪᴇ!**"); return
                
                p_msg = await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nᴏᴅ: {message.author.mention}\n\n{t_rek}")
                new_log = await log_ch.send(f"📂 **LOG**\nID_SERWERA: {inv_obj.guild.id}\nID_USER: {message.author.id}\nMSG_PART_ID: {p_msg.id}\n🏠 sᴇʀᴡᴇʀ: {inv_obj.guild.name}\n🔗 Link: {i_url}")
                
                self.uzyte_serwery[str(inv_obj.guild.id)] = [new_log.id, p_msg.id]
                self.ostatni_serwer = inv_obj.guild.name
                del self.aktywne_sesje[message.author.id]
                await message.channel.send("✅ **ɢᴏᴛᴏᴡᴇ!** ʀᴇᴋʟᴀᴍᴀ ᴢᴏsᴛᴀᴌᴀ ᴡʏsᴌᴀɴᴀ ɴᴀ ᴋᴀɴᴀᴌ.")
            except:
                await message.channel.send("❌ **ʟɪɴᴋ ᴊᴇsᴛ ɴɪᴇᴘᴏᴘᴚᴀᴡɴʏ ʟᴜʙ ᴡʏɢᴀsᴌ.**")

client = UltimateKore(); client.run(TOKEN)

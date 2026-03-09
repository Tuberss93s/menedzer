import discord
import re
import os
import asyncio
from datetime import datetime

# --- KONFIGURACJA ---
TOKEN = os.getenv('DISCORD_TOKEN') 
KANAL_PARTNERSTWA_ID = 1476971697507795177
KANAL_KORE_LOGS_ID = 1480639848862716185 
MOJE_ID_SERWERA = 1476957231034663153
ADMIN_ID = 1347691963008286781
KOLOR_KORE = 0x00d9ff 

class UltimateKore(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ostatni_serwer = "Wczytywanie..."
        self.uzyte_serwery = {} # ID_GUILD: [LOG_MSG_ID, PART_MSG_ID]
        self.zablokowani_uzytkownicy = set()
        self.aktywne_sesje = {} 

    async def send_kore_embed(self, destination, title, description, color=KOLOR_KORE, footer=True):
        embed = discord.Embed(title=title, description=description, color=color)
        if footer:
            embed.set_footer(text="ᴋᴏʀᴇ sʜ0ᴘ — ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇs", icon_url=self.user.avatar.url if self.user.avatar else None)
        return await destination.send(embed=embed)

    async def check_timeout(self, user_id):
        await asyncio.sleep(900)
        if user_id in self.aktywne_sesje:
            now = asyncio.get_event_loop().time()
            if now - self.aktywne_sesje[user_id] >= 900:
                try:
                    user = await self.fetch_user(user_id)
                    await self.send_kore_embed(user, "⌛ Sesja wygasła", "Twoja sesja partnerstwa wygasła po 15 minutach bezczynności.", color=0xff0000)
                except: pass
                del self.aktywne_sesje[user_id]

    async def load_db_from_discord(self):
        await self.wait_until_ready()
        log_ch, part_ch = self.get_channel(KANAL_KORE_LOGS_ID), self.get_channel(KANAL_PARTNERSTWA_ID)
        
        # Skanowanie historii logów (najważniejsze dla usuwania)
        if log_ch:
            print("🔍 Skanowanie bazy logów...")
            found_last = False
            async for msg in log_ch.history(limit=1000):
                m_srv = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if m_srv:
                    srv_id = m_srv.group(1)
                    # Szukamy ID wiadomości partnerstwa w logu
                    m_part_msg = re.search(r'MSG_PART_ID: (\d+)', msg.content)
                    part_msg_id = int(m_part_msg.group(1)) if m_part_msg else None
                    
                    self.uzyte_serwery[srv_id] = [msg.id, part_msg_id]
                    
                    if not found_last:
                        n_match = re.search(r'🏠 Serwer: (.+)', msg.content)
                        if n_match: self.ostatni_serwer, found_last = n_match.group(1), True
                
                m_block = re.search(r'BLOKADA_RETRY: (\d+)', msg.content)
                if m_block: self.zablokowani_uzytkownicy.add(int(m_block.group(1)))
                m_unblock = re.search(r'UNBLOCKED_USER: (\d+)', msg.content)
                if m_unblock:
                    u_id = int(m_unblock.group(1))
                    if u_id in self.zablokowani_uzytkownicy: self.zablokowani_uzytkownicy.remove(u_id)

        # Skanowanie kanału partnerstw dla starych wpisów (tylko ID)
        if part_ch:
            async for msg in part_ch.history(limit=500):
                inv = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', msg.content)
                if inv:
                    try:
                        invite = await self.fetch_invite(inv.group(0))
                        sid = str(invite.guild.id)
                        if sid not in self.uzyte_serwery:
                            self.uzyte_serwery[sid] = ["EXISTING", msg.id]
                    except: pass
        if self.ostatni_serwer == "Wczytywanie...": self.ostatni_serwer = "Brak"

    async def status_rotator(self):
        await self.wait_until_ready()
        while not self.is_closed():
            msgs = ["⚙️ Developer @kitsune_2520zapas", "✅ Czekanie na partnerstwa", "🛠️ MADE IN KORE SH0P", "💎 discord.gg/9jUSJcT2PF", f"🤝 OSTATNIE: {self.ostatni_serwer}", f"📊 Partnerstw: {len(self.uzyte_serwery)}", "📦 Nowe dostawy wleciały!", "💳 Płatności: TYLKO PSC 🎫", "🛡️ 100% Legit & Verified", "🎫 Otwórz Ticket by kupić", "🚀 Najszybsza realizacja"]
            for m in msgs:
                await self.change_presence(activity=discord.CustomActivity(name=m))
                await asyncio.sleep(3)

    async def on_ready(self):
        print(f"🚀 KORE ULTIMATE PRO ONLINE"); self.loop.create_task(self.status_rotator()); self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        log_ch, part_ch = self.get_channel(KANAL_KORE_LOGS_ID), self.get_channel(KANAL_PARTNERSTWA_ID)
        if message.author.id in self.aktywne_sesje: self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()

        # --- PANEL ADMINA ---
        if message.author.id == ADMIN_ID:
            if message.content.startswith("!usun"):
                parts = message.content.split(' ', 2)
                if len(parts) < 2: return
                srv_id, powód = parts[1], parts[2] if len(parts) > 2 else "Brak reklamy/Decyzja admina"
                
                if srv_id in self.uzyte_serwery:
                    log_msg_id, part_msg_id = self.uzyte_serwery[srv_id]
                    
                    # 1. Usuwanie reklamy z kanału partnerstw
                    if part_msg_id:
                        try:
                            p_msg = await part_ch.fetch_message(part_msg_id)
                            await p_msg.delete()
                        except: pass
                    
                    # 2. Usuwanie logu i blokowanie usera
                    if log_msg_id != "EXISTING":
                        try:
                            l_msg = await log_ch.fetch_message(log_msg_id)
                            u_match = re.search(r'ID_USER: (\d+)', l_msg.content)
                            if u_match:
                                u_id = int(u_match.group(1))
                                self.zablokowani_uzytkownicy.add(u_id)
                                await log_ch.send(f"🚫 BLOKADA_RETRY: {u_id}")
                                try:
                                    user = await self.fetch_user(u_id)
                                    await self.send_kore_embed(user, "⚠️ Partnerstwo Zakończone", f"Twoje partnerstwo zostało usunięte.\n\n**Powód:** {powód}", color=0xff0000)
                                except: pass
                            await l_msg.delete()
                        except: pass
                    
                    del self.uzyte_serwery[srv_id]
                    await message.channel.send(f"✅ Usunięto reklamę i zablokowano serwer `{srv_id}`.")
                return

            if message.content == "!status":
                await self.send_kore_embed(message.channel, "📊 Statystyki", f"Partnerstwa: `{len(self.uzyte_serwery)}` \nBlokady: `{len(self.zablokowani_uzytkownicy)}`")
                return

            if message.content.startswith("!potwierdz"):
                try:
                    u_id = int(message.content.split()[1])
                    if u_id in self.zablokowani_uzytkownicy:
                        self.zablokowani_uzytkownicy.remove(u_id); await log_ch.send(f"🔓 UNBLOCKED_USER: {u_id}"); await message.channel.send(f"✅ Odblokowano {u_id}.")
                except: pass
                return

        # --- SYSTEM DM ---
        if not isinstance(message.channel, discord.DMChannel): return
        if "PARTNERSTWO" in message.content.upper():
            if message.author.id in self.zablokowani_uzytkownicy:
                await self.send_kore_embed(message.channel, "❌ Blokada", "Jesteś zablokowany.", color=0xff0000); return
            self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()
            embed_reklama = discord.Embed(title="💎 ᴋᴏʀᴇ sʜ0ᴘ", description="Oferta Premium", color=KOLOR_KORE)
            embed_reklama.add_field(name="💳 PSC", value="Tylko PSC!", inline=False)
            await message.channel.send(embed=embed_reklama)
            await self.send_kore_embed(message.channel, "🤝 Kroki:", "1. Wstaw reklamę.\n2. Wklej swoją.\n3. Napisz **GOTOWE**.")
            self.loop.create_task(self.check_timeout(message.author.id))

        if "GOTOWE" in message.content.upper():
            if message.author.id not in self.aktywne_sesje: return
            t_rek, i_url = None, None
            async for m in message.channel.history(limit=10):
                inv = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', m.content)
                if inv and "9jUSJcT2PF" not in inv.group(0): t_rek, i_url = m.content, inv.group(0); break
            if not t_rek: return
            try:
                inv_obj = await self.fetch_invite(i_url)
                if str(inv_obj.guild.id) in self.uzyte_serwery:
                    await self.send_kore_embed(message.channel, "❌ Duplikat", "Serwer już istnieje!", color=0xff0000); return
                
                # WYSYŁKA REKLAMY
                p_msg = await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nOd: {message.author.mention}\n\n{t_rek}")
                
                # LOGOWANIE Z ID REKLAMY
                new_log = await log_ch.send(f"📂 **LOG**\nID_SERWERA: {inv_obj.guild.id}\nID_USER: {message.author.id}\nMSG_PART_ID: {p_msg.id}\n🏠 Serwer: {inv_obj.guild.name}\n🔗 Link: {i_url}")
                
                self.uzyte_serwery[str(inv_obj.guild.id)] = [new_log.id, p_msg.id]
                self.ostatni_serwer = inv_obj.guild.name
                del self.aktywne_sesje[message.author.id]
                await self.send_kore_embed(message.channel, "✅ Sukces!", "Partnerstwo zaakceptowane!")
            except: pass

client = UltimateKore(); client.run(TOKEN)
 

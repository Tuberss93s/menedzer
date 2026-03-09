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
ADMIN_ID = 1347691963008286781  # Twoje ID

# --- TWOJA PEŁNA REKLAMA ---
MOJA_REKLAMA = """
# 💎 **ᴋᴏʀᴇ sʜ0ᴘ — ᴘʀᴇᴍɪᴜᴍ ᴅɪsᴄᴏʀᴅ sᴇʀᴠɪᴄᴇs** 💎

Szukasz profesjonalnych usług, kont do gier lub boostów? **ᴋᴏʀᴇ sʜ0ᴘ** to Twoje centrum wszystkiego, czego potrzebujesz na Discordzie! Najlepsza jakość i stałe ceny. 🚀

---

### 🎮 **ɴᴀsᴢᴀ ᴏғᴇʀᴛᴀ (ᴋᴀᴛᴇɢᴏʀɪᴇ):**

* 〢📱 **ᴅ𝟷sᴄᴏʀᴅ:** Nitro, Server Boosty oraz gotowe konta Discord.
* 〢👤 **ᴋᴏɴᴛᴀ:** Konta Premium, waluty w grach, subskrypcje i licencje.
* 〢🕹️ **ɢʀʏ:**
    * ᴍɪɴᴇᴄʀᴀꜰᴛ (ᴊᴀᴠᴀ & ʙᴇᴅʀᴏᴄᴋ) — **60 ᴢᴌ**
    * ʀᴏʙʟᴏx (2009 | 15 ʏᴇᴀʀs) — **20 ᴢᴌ**
    * ᴠᴀʟᴏʀᴀɴᴛ — **30 ᴢᴌ** | ʟᴏʟ — **65 ᴢᴌ**
* 〢🛠️ **ɪɴɴᴇ (ᴍᴇᴍʙᴇʀsʜɪᴘ ᴘᴀᴄᴋs):**
    * ⚡ **𝟷𝟶,𝟶𝟶𝟶 ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs + ʙᴏᴏsᴛ** — **80 ᴢᴌ**
    * ⚡ **𝟻,𝟶𝟶𝟶 ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs + ʙᴏᴏsᴛ** — **35 ᴢᴌ**
    * ⚡ **𝟷,𝟶𝟶𝟶 Western ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs + ʙᴏᴏsᴛ** — **20 ᴢᴌ**
    * ᴄʜᴇᴀᴛʏ, sᴄʀɪᴘᴛʏ ᴏʀᴀᴢ ᴅᴇsɪɢɴ/ɢʀᴀꜰɪᴋᴀ!

---

### 💳 **ᴘᴌᴀᴛɴᴏśᴄɪ ɪ ʀᴇᴀʟɪᴢᴀᴄᴊᴀ:**
* 〢🎫 **ᴘᴀʏsᴀғᴇᴄᴀʀᴅ (ᴘsᴄ)** — Jedyna akceptowana metoda płatności.
* 〢⚡ **ᴛɪᴄᴋᴇᴛ 1:1:** Wszystko ustalamy indywidualnie na tickecie.
* 〢🛡️ **ʟᴇɢɪᴛ:** Sprawdź nasze opinie na kanale <#1476961244463239180>.

---

🔗 **ᴅᴏᴌᴀ̨ᴄᴢ ᴅᴏ ɴᴀs:** https://discord.gg/9jUSJcT2PF
"""

class UltimateKore(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ostatni_serwer = "Wczytywanie..."
        self.uzyte_serwery = {} 
        self.zablokowani_uzytkownicy = set()
        self.aktywne_sesje = {}

    async def load_db_from_discord(self):
        await self.wait_until_ready()
        baza_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        if baza_ch:
            print("⏳ Synchronizacja bazy danych...")
            found_last = False
            async for msg in baza_ch.history(limit=1000):
                match_srv = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if match_srv:
                    self.uzyte_serwery[match_srv.group(1)] = msg.id
                    if not found_last:
                        name_match = re.search(r'🏠 Serwer: (.+)', msg.content)
                        if name_match:
                            self.ostatni_serwer = name_match.group(1)
                            found_last = True

                match_block = re.search(r'BLOKADA_RETRY: (\d+)', msg.content)
                if match_block:
                    self.zablokowani_uzytkownicy.add(int(match_block.group(1)))
                
                match_unblock = re.search(r'UNBLOCKED_USER: (\d+)', msg.content)
                if match_unblock:
                    u_id = int(match_unblock.group(1))
                    if u_id in self.zablokowani_uzytkownicy:
                        self.zablokowani_uzytkownicy.remove(u_id)

            if not found_last: self.ostatni_serwer = "Brak"
            print(f"✅ Baza gotowa. Ostatni: {self.ostatni_serwer}")

    async def status_rotator(self):
        await self.wait_until_ready()
        while not self.is_closed():
            messages = [
                "⚙️ Developer @kitsune_2520zapas",
                "✅ Czekanie na partnerstwa",
                "🛠️ MADE IN KORE SH0P",
                "💎 discord.gg/9jUSJcT2PF",
                f"🤝 OSTATNIE: {self.ostatni_serwer}",
                "📦 Nowe dostawy wleciały!",
                "💳 Płatności: TYLKO PSC 🎫",
                "🛡️ 100% Legit & Verified",
                "🎫 Otwórz Ticket by kupić",
                "🚀 Najszybsza realizacja"
            ]
            for msg in messages:
                await self.change_presence(activity=discord.CustomActivity(name=msg))
                await asyncio.sleep(3)

    async def on_ready(self):
        print(f"🚀 KORE ULTIMATE ONLINE | Zalogowano: {self.user}")
        self.loop.create_task(self.status_rotator())
        self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)

        # --- PANEL ADMINISTRATORA (TYLKO TY) ---
        if message.author.id == ADMIN_ID:
            # Komenda: !help
            if message.content == "!help":
                help_text = (
                    "🛠️ **PANEL ADMINISTRATORA KORE SHOP**\n\n"
                    "🔹 `!usun [ID_SERWERA]` - Usuwa partnerstwo z logów i blokuje użytkownika.\n"
                    "🔹 `!potwierdz [ID_USERA]` - Odblokowuje osobę, by mogła znów zrobić partnerstwo.\n"
                    "🔹 `!status` - Pokazuje aktualną liczbę partnerstw w bazie i blokad.\n\n"
                    "💡 *ID serwera i ID użytkownika znajdziesz na kanale logów.*"
                )
                await message.channel.send(help_text)
                return

            # Komenda: !status (Dodatkowa)
            if message.content == "!status":
                await message.channel.send(f"📊 **STATYSTYKI:**\nPartnerstw w bazie: `{len(self.uzyte_serwery)}` \nZablokowanych: `{len(self.zablokowani_uzytkownicy)}` \nOstatni serwer: `{self.ostatni_serwer}`")
                return

            # Komenda: !usun
            if message.content.startswith("!usun"):
                try:
                    srv_id = message.content.split()[1]
                    if srv_id in self.uzyte_serwery:
                        msg_log = await log_ch.fetch_message(self.uzyte_serwery[srv_id])
                        user_match = re.search(r'ID_USER: (\d+)', msg_log.content)
                        if user_match:
                            u_id = int(user_match.group(1))
                            self.zablokowani_uzytkownicy.add(u_id)
                            await log_ch.send(f"🚫 **BLOKADA**\nBLOKADA_RETRY: {u_id}\nSerwer: {srv_id}")
                            try:
                                user = await self.fetch_user(u_id)
                                await user.send("⚠️ **ɪɴғᴏʀᴍᴀᴄᴊᴀ sʏsᴛᴇᴍᴏᴡᴀ — ᴋᴏʀᴇ sʜ0ᴘ**\nTwoje partnerstwo zostało zakończone, a reklama usunięta.\n\n**Powód:** Brak reklamy / zamknięcie przez właściciela / usunięcie wpisu.\n\nJeśli chcesz odnowić współpracę, upewnij się, że nasza reklama jest widoczna i napisz ponownie Partnerstwo w DM lub zgłoś to do właściciela.")
                            except: pass
                        await msg_log.delete()
                        del self.uzyte_serwery[srv_id]
                        await message.channel.send(f"✅ Usunięto `{srv_id}` i zablokowano użytkownika.")
                    else: await message.channel.send("❌ Brak ID w bazie.")
                except: await message.channel.send("❌ Użycie: `!usun [ID]`")
                return

            # Komenda: !potwierdz
            if message.content.startswith("!potwierdz"):
                try:
                    u_id = int(message.content.split()[1])
                    if u_id in self.zablokowani_uzytkownicy:
                        self.zablokowani_uzytkownicy.remove(u_id)
                        await log_ch.send(f"🔓 **ODBLOKOWANIE**\nUNBLOCKED_USER: {u_id}")
                        await message.channel.send(f"✅ Użytkownik `{u_id}` odblokowany.")
                    else: await message.channel.send("❌ Ten użytkownik nie ma blokady.")
                except: await message.channel.send("❌ Użycie: `!potwierdz [ID_USERA]`")
                return

        # --- SYSTEM DLA UŻYTKOWNIKÓW (DM) ---
        if not isinstance(message.channel, discord.DMChannel): return
        content_upper = message.content.upper()

        if "PARTNERSTWO" in content_upper:
            if message.author.id in self.zablokowani_uzytkownicy:
                await message.channel.send("❌ Twoja możliwość zawierania partnerstw została zablokowana przez właściciela. Skontaktuj się z administratorem.")
                return
            self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()
            await message.channel.send(MOJA_REKLAMA)
            await message.channel.send("🤝 **KROKI:**\n1. Wstaw reklamę u siebie.\n2. Wklej tutaj swoją reklamę.\n3. Napisz **GOTOWE**.")
            
            await asyncio.sleep(900)
            if message.author.id in self.aktywne_sesje:
                if asyncio.get_event_loop().time() - self.aktywne_sesje[message.author.id] >= 900:
                    await message.channel.send("⌛ Przykro mi, ale musisz zacząć od nowa ponieważ trzeba było za długo czekać (15 minut).")
                    del self.aktywne_sesje[message.author.id]
            return

        if "GOTOWE" in content_upper:
            if message.author.id not in self.aktywne_sesje:
                await message.channel.send("❌ Sesja wygasła. Napisz `Partnerstwo` ponownie.")
                return

            target_reklama, invite_url = None, None
            async for msg in message.channel.history(limit=15):
                inv_match = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', msg.content)
                if inv_match and "9jUSJcT2PF" not in inv_match.group(0):
                    target_reklama, invite_url = msg.content, inv_match.group(0)
                    break

            if not target_reklama:
                await message.channel.send("❌ Nie znalazłem Twojej reklamy. Wklej ją i napisz GOTOWE.")
                return

            try:
                invite = await self.fetch_invite(invite_url)
                guild_id_str = str(invite.guild.id)
                if guild_id_str in self.uzyte_serwery:
                    await message.channel.send("❌ Ten serwer już u nas jest!")
                    return

                if part_ch and log_ch:
                    await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nOd: {message.author.mention}\n\n{target_reklama}")
                    new_log = await log_ch.send(f"📂 **NOWE DANE**\nID_SERWERA: {guild_id_str}\nID_USER: {message.author.id}\n🏠 Serwer: {invite.guild.name}\n🔗 Link: {invite_url}\n📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                    self.uzyte_serwery[guild_id_str] = new_log.id
                    self.ostatni_serwer = invite.guild.name
                    del self.aktywne_sesje[message.author.id]
                    await message.channel.send(f"✅ **Sukces!** Partnerstwo zaakceptowane.")
            except: await message.channel.send("❌ Błąd linku zaproszenia.")

if __name__ == "__main__":
    client = UltimateKore()
    client.run(TOKEN)

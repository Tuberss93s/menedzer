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
        self.uzyte_serwery = {} # ID_GUILD: ID_MSG_LOGS
        self.zablokowani_uzytkownicy = set()
        self.aktywne_sesje = {}

    async def load_db_from_discord(self):
        """Pobiera historię logów i buduje bazę danych w pamięci"""
        await self.wait_until_ready()
        baza_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        if baza_ch:
            print("⏳ Analizowanie historii logów...")
            found_last = False
            async for msg in baza_ch.history(limit=1000):
                # Szukanie ID serwerów
                match_srv = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if match_srv:
                    self.uzyte_serwery[match_srv.group(1)] = msg.id
                    if not found_last:
                        name_match = re.search(r'🏠 Serwer: (.+)', msg.content)
                        if name_match:
                            self.ostatni_serwer = name_match.group(1)
                            found_last = True

                # Szukanie aktywnych blokad
                match_block = re.search(r'BLOKADA_RETRY: (\d+)', msg.content)
                if match_block:
                    self.zablokowani_uzytkownicy.add(int(match_block.group(1)))
                
                # Usuwanie blokady jeśli w logach jest potwierdzenie
                match_unblock = re.search(r'UNBLOCKED_USER: (\d+)', msg.content)
                if match_unblock:
                    u_id = int(match_unblock.group(1))
                    if u_id in self.zablokowani_uzytkownicy:
                        self.zablokowani_uzytkownicy.remove(u_id)

            if not found_last: self.ostatni_serwer = "Brak"
            print(f"✅ Baza załadowana. Zablokowanych: {len(self.zablokowani_uzytkownicy)}")

    async def status_rotator(self):
        """Dynamiczna pętla statusów co 3 sekundy"""
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
        print(f"🚀 KORE ULTIMATE ONLINE | Admin: {ADMIN_ID}")
        self.loop.create_task(self.status_rotator())
        self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)

        # --- PANEL ADMINA ---
        if message.author.id == ADMIN_ID:
            # Komenda: !usun [ID_SERWERA]
            if message.content.startswith("!usun"):
                try:
                    srv_id = message.content.split()[1]
                    if srv_id in self.uzyte_serwery:
                        msg_log = await log_ch.fetch_message(self.uzyte_serwery[srv_id])
                        user_match = re.search(r'ID_USER: (\d+)', msg_log.content)
                        
                        if user_match:
                            u_id = int(user_match.group(1))
                            self.zablokowani_uzytkownicy.add(u_id)
                            await log_ch.send(f"🚫 **BLOKADA ADMINISTRACYJNA**\nBLOKADA_RETRY: {u_id}\nPOWÓD: Usunięte partnerstwo {srv_id}")
                            
                            try:
                                user = await self.fetch_user(u_id)
                                await user.send("⚠️ **ɪɴғᴏʀᴍᴀᴄᴊᴀ sʏsᴛᴇᴍᴏᴡᴀ — ᴋᴏʀᴇ sʜ0ᴘ**\nTwoje partnerstwo zostało właśnie zakończone, a reklama usunięta z naszego kanału.\n\n**Powód:** Wykryto brak naszej reklamy na Twoim serwerze / zamkniecie przez wlasciciela / usunięcie wpisu.\n\nJeśli uważasz, że to błąd lub chcesz odnowić współpracę, upewnij się, że nasza reklama jest widoczna i napisz ponownie Partnerstwo w DM bota lub zgłoś to do własciciela.")
                            except: pass

                        await msg_log.delete()
                        del self.uzyte_serwery[srv_id]
                        await message.channel.send(f"✅ Usunięto partnerstwo `{srv_id}` i zablokowano użytkownika.")
                    else:
                        await message.channel.send("❌ To ID nie istnieje w bazie.")
                except: await message.channel.send("❌ Użycie: `!usun [ID_SERWERA]`")
                return

            # Komenda: !potwierdz [ID_UZYTKOWNIKA]
            if message.content.startswith("!potwierdz"):
                try:
                    u_id = int(message.content.split()[1])
                    if u_id in self.zablokowani_uzytkownicy:
                        self.zablokowani_uzytkownicy.remove(u_id)
                        await log_ch.send(f"🔓 **DECYZJA ADMINISTRATORA**\nUNBLOCKED_USER: {u_id}")
                        await message.channel.send(f"✅ Użytkownik `{u_id}` został odblokowany.")
                    else:
                        await message.channel.send("❌ Ten użytkownik nie ma blokady.")
                except: await message.channel.send("❌ Użycie: `!potwierdz [ID_UZYTKOWNIKA]`")
                return

        # --- SYSTEM DM ---
        if not isinstance(message.channel, discord.DMChannel): return
        content_upper = message.content.upper()

        if "PARTNERSTWO" in content_upper:
            if message.author.id in self.zablokowani_uzytkownicy:
                await message.channel.send("❌ Twoja możliwość zawierania partnerstw została zablokowana przez właściciela. Skontaktuj się z administratorem, aby uzyskać odblokowanie.")
                return
            
            self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()
            await message.channel.send(MOJA_REKLAMA)
            await message.channel.send("🤝 **KROKI:**\n1. Wstaw reklamę powyżej u siebie.\n2. Wklej tutaj **TWOJĄ REKLAMĘ**.\n3. Napisz **GOTOWE**.")
            
            await asyncio.sleep(900)
            if message.author.id in self.aktywne_sesje:
                if asyncio.get_event_loop().time() - self.aktywne_sesje[message.author.id] >= 900:
                    await message.channel.send("⌛ Przykro mi, ale musisz zacząć od nowa ponieważ trzeba było za długo czekać (15 minut).")
                    del self.aktywne_sesje[message.author.id]
            return

        if "GOTOWE" in content_upper:
            if message.author.id not in self.aktywne_sesje:
                await message.channel.send("❌ Sesja wygasła lub nie została rozpoczęta. Napisz `Partnerstwo` ponownie.")
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

                if invite.guild.id == MOJE_ID_SERWERA:
                    await message.channel.send("❌ To mój serwer!")
                    return

                if guild_id_str in self.uzyte_serwery:
                    await message.channel.send("❌ Ten serwer już brał udział w partnerstwie!")
                    return

                if part_ch and log_ch:
                    await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nOd: {message.author.mention}\n\n{target_reklama}")
                    new_log = await log_ch.send(f"📂 **NOWE DANE**\nID_SERWERA: {guild_id_str}\nID_USER: {message.author.id}\n🏠 Serwer: {invite.guild.name}\n🔗 Link: {invite_url}\n📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                    
                    self.uzyte_serwery[guild_id_str] = new_log.id
                    self.ostatni_serwer = invite.guild.name
                    del self.aktywne_sesje[message.author.id]
                    await message.channel.send(f"✅ **Sukces!** Partnerstwo zostało zaakceptowane i wrzucone na kanał.")
            except:
                await message.channel.send("❌ Błąd: Zaproszenie jest nieprawidłowe lub wygasło.")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ BRAK TOKENA W VARIABLES!")
    else:
        client = UltimateKore()
        client.run(TOKEN)

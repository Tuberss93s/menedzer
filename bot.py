import discord
import re
import os
import asyncio

# --- KONFIGURACJA ---
TOKEN = os.getenv('DISCORD_TOKEN') 
KANAL_PARTNERSTWA_ID = 1476971697507795177
KANAL_KORE_LOGS_ID = 1480639848862716185 
MOJE_ID_SERWERA = 1476957231034663153
ADMIN_ID = 1347691963008286781  # Twoje ID właściciela

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
    * ⚡ **𝟷,𝟶𝟶 Western ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs + ʙᴏᴏsᴛ** — **20 ᴢᴌ**
    * ᴄʜᴇᴀᴛʏ, sᴄʀɪᴘᴛʏ ᴏʀᴀᴢ ᴅᴇsɪɢɴ/ɢʀᴀꜰɪᴋᴀ!

---

### 💳 **ᴘᴌᴀᴛɴᴏśᴄɪ ɪ ʀᴇᴀʟɪᴢᴀᴄᴊᴀ:**
* 〢🎫 **ᴘᴀʏsᴀғᴇᴄᴀʀᴅ (ᴘsᴄ)** — Jedyna akceptowana metoda płatności.
* 〢⚡ **ᴛɪᴄᴋᴇᴛ 1:1:** Wszystko ustalamy indywidualnie na tickecie.
* 〢🛡️ **ʟᴇɢɪᴛ:** Sprawdź nasze opinie na kanale <#1476961244463239180>.

---

🔗 **ᴅᴏᴌᴀ̨ᴄᴢ ᴅᴏ ɴᴀs:** https://discord.gg/9jUSJcT2PF
"""

class InstantKore(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ostatni_serwer = "Wczytywanie..."
        self.uzyte_serwery = {} # ID_GUILD: ID_MESSAGE_LOGS
        self.aktywne_sesje = {} # USER_ID: LAST_ACTIVITY_TIMESTAMP

    async def load_db_from_discord(self):
        """Pobiera bazę danych oraz nazwę ostatniego serwera z historii logów"""
        await self.wait_until_ready()
        baza_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        if baza_ch:
            print("⏳ Wczytywanie bazy partnerstw i ostatniego serwera...")
            messages = []
            async for msg in baza_ch.history(limit=500):
                messages.append(msg)
                match = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if match:
                    self.uzyte_serwery[match.group(1)] = msg.id
            
            # Pobieranie nazwy ostatniego serwera z najnowszej wiadomości w logach
            if messages:
                for m in messages: # Pierwsza od góry (najnowsza)
                    name_match = re.search(r'🏠 Serwer: (.+)', m.content)
                    if name_match:
                        self.ostatni_serwer = name_match.group(1)
                        break
            else:
                self.ostatni_serwer = "Brak"
            print(f"✅ Załadowano {len(self.uzyte_serwery)} partnerstw. Ostatni: {self.ostatni_serwer}")

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
                await asyncio.sleep(4)

    async def on_ready(self):
        print("-" * 30)
        print(f'✅ KORE MANAGER ONLINE | Admin ID: {ADMIN_ID}')
        print("-" * 30)
        self.loop.create_task(self.status_rotator())
        self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return

        # --- KOMENDA: USUŃ PARTNERSTWO ---
        if message.content.startswith("!usun") and message.author.id == ADMIN_ID:
            try:
                guild_id = message.content.split()[1]
                if guild_id in self.uzyte_serwery:
                    log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
                    
                    # Pobieranie logu, aby wyciągnąć ID użytkownika przed usunięciem
                    msg_log = await log_ch.fetch_message(self.uzyte_serwery[guild_id])
                    user_match = re.search(r'ID_USER: (\d+)', msg_log.content)
                    
                    if user_match:
                        try:
                            user = await self.fetch_user(int(user_match.group(1)))
                            await user.send("⚠️ **ɪɴғᴏʀᴍᴀᴄᴊᴀ sʏsᴛᴇᴍᴏᴡᴀ — ᴋᴏʀᴇ sʜ0ᴘ**\nTwoja współpraca została zakończona lub zamknięta przez właściciela.")
                        except: pass # DM zablokowane
                    
                    await msg_log.delete()
                    del self.uzyte_serwery[guild_id]
                    await message.channel.send(f"✅ Partnerstwo {guild_id} zostało usunięte z bazy danych i logów.")
                else:
                    await message.channel.send("❌ Nie znaleziono serwera o takim ID w bazie.")
            except:
                await message.channel.send("❌ Poprawne użycie: `!usun [ID_SERWERA]`")
            return

        if not isinstance(message.channel, discord.DMChannel): return

        content_upper = message.content.upper()

        if "PARTNERSTWO" in content_upper:
            self.aktywne_sesje[message.author.id] = asyncio.get_event_loop().time()
            await message.channel.send(MOJA_REKLAMA)
            await message.channel.send("🤝 **KROKI:**\n1. Wstaw reklamę powyżej u siebie.\n2. Wklej tutaj **TWOJĄ REKLAMĘ**.\n3. Napisz **GOTOWE**.")
            
            # Obsługa timeoutu 15 minut
            await asyncio.sleep(900)
            if message.author.id in self.aktywne_sesje:
                if asyncio.get_event_loop().time() - self.aktywne_sesje[message.author.id] >= 900:
                    await message.channel.send("⌛ Przykro mi, ale musisz zacząć od nowa ponieważ trzeba było za długo czekać (15 minut).")
                    del self.aktywne_sesje[message.author.id]
            return

        if "GOTOWE" in content_upper:
            if message.author.id not in self.aktywne_sesje:
                await message.channel.send("❌ Twoja sesja wygasła. Napisz `Partnerstwo` aby zacząć od nowa.")
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

                part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)
                log_ch = self.get_channel(KANAL_KORE_LOGS_ID)

                if part_ch and log_ch:
                    await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nOd: {message.author.mention}\n\n{target_reklama}")
                    
                    # Wysyłka logów z ID_USER dla systemu usuwania
                    new_log = await log_ch.send(f"📂 **NOWE DANE**\nID_SERWERA: {guild_id_str}\nID_USER: {message.author.id}\n🏠 Serwer: {invite.guild.name}\n🔗 Link: {invite_url}")
                    
                    self.uzyte_serwery[guild_id_str] = new_log.id
                    self.ostatni_serwer = invite.guild.name
                    if message.author.id in self.aktywne_sesje: del self.aktywne_sesje[message.author.id]
                    await message.channel.send(f"✅ **Sukces!** Partnerstwo zaakceptowane.")
            except:
                await message.channel.send("❌ Błąd linku zaproszenia.")

client = InstantKore()
client.run(TOKEN)

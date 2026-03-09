import discord
import re
import os
import asyncio

# --- KONFIGURACJA (POBIERANA Z RAILWAY) ---
TOKEN = os.getenv('DISCORD_TOKEN') 
KANAL_PARTNERSTWA_ID = 1476971697507795177
KANAL_KORE_LOGS_ID = 1480639848862716185 
MOJE_ID_SERWERA = 1476957231034663153

# --- TWOJA PEŁNA REKLAMA (TYLKO PSC) ---
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
        self.ostatni_serwer = "Brak"
        self.uzyte_serwery = set()

    async def load_db_from_discord(self):
        """Wczytuje bazę partnerstw z historii kanału logów"""
        await self.wait_until_ready()
        baza_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        if baza_ch:
            print("⏳ Wczytywanie bazy partnerstw z historii...")
            async for msg in baza_ch.history(limit=1000):
                match = re.search(r'ID_SERWERA: (\d+)', msg.content)
                if match:
                    self.uzyte_serwery.add(match.group(1))
            print(f"✅ Załadowano {len(self.uzyte_serwery)} partnerstw.")

    async def status_rotator(self):
        """Dynamiczna pętla statusów (zmiana co 4 sekundy)"""
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
                await asyncio.sleep(4) # Przyspieszone do 4 sekund

    async def on_ready(self):
        print("-" * 30)
        print(f'✅ KORE MANAGER ONLINE')
        print(f'👤 Developer: kitsune_2520zapas')
        print("-" * 30)
        self.loop.create_task(self.status_rotator())
        self.loop.create_task(self.load_db_from_discord())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        if not isinstance(message.channel, discord.DMChannel): return

        content_upper = message.content.upper()
        log_ch = self.get_channel(KANAL_KORE_LOGS_ID)
        part_ch = self.get_channel(KANAL_PARTNERSTWA_ID)

        # KOMENDA: PARTNERSTWO
        if "PARTNERSTWO" in content_upper:
            await message.channel.send(MOJA_REKLAMA)
            await message.channel.send("🤝 **KROKI:**\n1. Wstaw reklamę powyżej u siebie.\n2. Wklej tutaj **TWOJĄ REKLAMĘ**.\n3. Napisz **GOTOWE**.")
            return

        # KOMENDA: GOTOWE
        if "GOTOWE" in content_upper:
            target_reklama = None
            invite_url = None
            async for msg in message.channel.history(limit=15):
                inv_match = re.search(r'(discord\.(gg|io|me|li)\/.+|discord\.com\/invite\/.+)', msg.content)
                if inv_match and "9jUSJcT2PF" not in inv_match.group(0):
                    target_reklama = msg.content
                    invite_url = inv_match.group(0)
                    break

            if not target_reklama:
                await message.channel.send("❌ Nie znalazłem Twojej reklamy w DM. Wklej ją najpierw!")
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

                if part_ch:
                    # Wysyłka reklamy partnera
                    await part_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nOd: {message.author.mention}\n\n{target_reklama}")
                    
                    # Logowanie do bazy i pamięci
                    self.uzyte_serwery.add(guild_id_str)
                    self.ostatni_serwer = invite.guild.name
                    await message.channel.send(f"✅ **Sukces!** Partnerstwo zaakceptowane.")
                    
                    if log_ch:
                        await log_ch.send(f"📂 **NOWE DANE**\nID_SERWERA: {guild_id_str}\n👤 Od: {message.author}\n🏠 Serwer: {invite.guild.name}\n🔗 Link: {invite_url}")
                else:
                    await message.channel.send("❌ Błąd: Brak dostępu do kanału partnerstw.")
            except Exception:
                await message.channel.send("❌ Błąd: Link wygasł lub jest niepoprawny.")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ BŁĄD: Brak zmiennej DISCORD_TOKEN na Railway!")
    else:
        client = InstantKore()
        client.run(TOKEN)

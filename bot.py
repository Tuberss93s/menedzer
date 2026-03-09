import discord
import json
import re
import os
import asyncio

# --- KONFIGURACJA ZMIENNYCH ---
# Pobiera token bezpiecznie z ustawień Railway (zmienna DISCORD_TOKEN)
TOKEN = os.getenv('DISCORD_TOKEN') 
KANAL_PARTNERSTWA_ID = 1476971697507795177
KANAL_BAZA_DANYCH_ID = 1480552897279164528
MOJE_ID_SERWERA = 1476957231034663153

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
    * ⚡ **𝟷,𝟶𝟶 Western ᴏꜰꜰʟɪɴᴇ ᴍᴇᴍʙᴇʀs + ʙᴏᴏsᴛ** — **20 ᴢᴌ**
    * ᴄʜᴇᴀᴛʏ, sᴄʀɪᴘᴛʏ ᴏʀᴀᴢ ᴅᴇsɪɢɴ/ɢʀᴀꜰɪᴋᴀ!

---

### 💳 **ᴘᴌᴀᴛɴᴏśᴄɪ ɪ ʀᴇᴀʟɪᴢᴀᴄᴊᴀ:**
* 〢🎫 **ᴘᴀʏsᴀғᴇᴄᴀʀᴅ (ᴘsᴄ)** — Szybko i anonimowo.
* 〢⚡ **ᴛɪᴄᴋᴇᴛ 1:1:** Wszystko ustalamy indywidualnie na tickecie.
* 〢🛡️ **ʟᴇɢɪᴛ:** Sprawdź nasze opinie na kanale <#1476961244463239180>.

---

🔗 **ᴅᴏᴌᴀ̨ᴄᴢ ᴅᴏ ɴᴀs:** https://discord.gg/9jUSJcT2PF
"""

DB_FILE = 'active_partnerships.json'
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f: json.dump({}, f)

class InstantKore(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ostatni_serwer = "Brak"

    async def status_rotator(self):
        await self.wait_until_ready()
        while not self.is_closed():
            messages = [
                "⚙️ Developer @kitsune_2520zapas",
                "✅ Czekanie na partnerstwa",
                "🛠️ MADE IN KORE SH0P",
                "💎 discord.gg/9jUSJcT2PF",
                f"🤝 OSTATNIE: {self.ostatni_serwer}"
            ]
            for msg in messages:
                await self.change_presence(activity=discord.CustomActivity(name=msg))
                await asyncio.sleep(7)

    async def on_ready(self):
        print("-" * 30)
        print(f'✅ KORE MANAGER ONLINE')
        print(f'👤 Developer: kitsune_2520zapas')
        print("-" * 30)
        self.loop.create_task(self.status_rotator())

    async def on_message(self, message):
        if message.author.id == self.user.id: return
        if not isinstance(message.channel, discord.DMChannel): return

        content_upper = message.content.upper()
        baza_ch = self.get_channel(KANAL_BAZA_DANYCH_ID)

        if "PARTNERSTWO" in content_upper:
            await message.channel.send(MOJA_REKLAMA)
            await message.channel.send("🤝 **KROKI:**\n1. Wstaw reklamę powyżej u siebie.\n2. Wklej tutaj **TWOJĄ REKLAMĘ**.\n3. Napisz **GOTOWE**.")
            return

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
                await message.channel.send("❌ Nie znalazłem Twojej reklamy w DM. Wklej ją najpierw, potem napisz GOTOWE.")
                return

            try:
                invite = await self.fetch_invite(invite_url)
                if invite.guild.id == MOJE_ID_SERWERA:
                    await message.channel.send("❌ To jest link do mojego serwera!")
                    return

                # Wczytywanie bazy
                if not os.path.exists(DB_FILE):
                    with open(DB_FILE, 'w') as f: json.dump({}, f)
                
                with open(DB_FILE, 'r') as f: db = json.load(f)
                
                if str(invite.guild.id) in db:
                    await message.channel.send("❌ Ten serwer już brał udział w partnerstwie!")
                    return

                log_ch = self.get_channel(KANAL_PARTNERSTWA_ID)
                if log_ch:
                    await log_ch.send(f"🤝 **ɴᴏᴡᴇ ᴘᴀʀᴛɴᴇʀsᴛᴡᴏ**\nOd: {message.author.mention}\n\n{target_reklama}")
                    
                    db[str(invite.guild.id)] = message.author.id
                    with open(DB_FILE, 'w') as f: json.dump(db, f)
                    
                    self.ostatni_serwer = invite.guild.name
                    await message.channel.send(f"✅ **Sukces!** Partnerstwo zaakceptowane.")
                    
                    if baza_ch:
                        await baza_ch.send(f"📂 **NOWE DANE DO SPRAWDZENIA**\n👤 Od: {message.author}\n🏠 Serwer: {invite.guild.name}\n🔗 Link: {invite_url}")
                else:
                    await message.channel.send("❌ Błąd: Nie widzę kanału partnerstw.")

            except Exception as e:
                await message.channel.send("❌ Zły link.")
                if baza_ch: await baza_ch.send(f"⚠️ Błąd u {message.author}: {e}")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ BŁĄD: Brak zmiennej DISCORD_TOKEN w ustawieniach Railway!")
    else:
        client = InstantKore()
        client.run(TOKEN)

# emojis.py
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
import discord
from discord.ext import commands

logger = logging.getLogger("emojis")

ASSETS_DIR = Path(__file__).parent / "emoji" / "assets"
CACHE_FILE = Path(__file__).parent / "emoji" / "synced_emojis.json"


class DynamicEmoji(str):
    """
    A dynamic string-like emoji object that updates in-place when synced
    with Discord Developer Portal (Application Emojis).
    """
    def __new__(cls, name: str, default: str):
        obj = super().__new__(cls, default)
        obj.name = name
        obj._val = default
        obj.emoji_id = None
        return obj

    def set_value(self, val: str, emoji_id: Optional[int] = None):
        self._val = str(val)
        if emoji_id:
            self.emoji_id = emoji_id

    def __str__(self):
        return self._val

    def __repr__(self):
        return self._val

    def __format__(self, format_spec):
        return format(self._val, format_spec)

    def strip(self, chars=None):
        return self._val.strip(chars)

    def __add__(self, other):
        return self._val + str(other)

    def __radd__(self, other):
        return str(other) + self._val

    def __eq__(self, other):
        return self._val == str(other)

    def __hash__(self):
        return hash(self._val)


# --- Main Emojis (Defaults until synced with Developer Portal) ---
CHECK = DynamicEmoji("check", "<:Check:1491719303215710288>")
VERIFIED_CHECK = DynamicEmoji("check", "<:Check:1491719303215710288>")
CROSS = DynamicEmoji("cross", "<:zcross:1491493999909802155>")
CROSS_MARK = DynamicEmoji("cross", "<:zcross:1491493999909802155>")
TICK = DynamicEmoji("check", "<:Check:1491719303215710288>")
ZTICK = DynamicEmoji("check", "<:Check:1491719303215710288>")
ERROR_X = DynamicEmoji("cross", "<:zcross:1491493999909802155>")
LOCK = DynamicEmoji("lock", "<:lock:1409553573427150972>")
UNLOCK = DynamicEmoji("unlock", "<:unlock:1409553569903935538>")
GHOST = DynamicEmoji("ghost", "<:ghost:1409553544578732125>")
UNGHOST = DynamicEmoji("unghost", "<:unghost:1409553565160181902>")
BOOST = DynamicEmoji("boost", "<:boost:1458329837050527807>")
INFO = DynamicEmoji("warning", "<:Warning:1408118547086835904>")
CART = DynamicEmoji("cart", "<:Cart:1458329940801097885>")
SUPPORT = DynamicEmoji("support", "<:support:1409379435827826821>")
DELETE = DynamicEmoji("delete", "<:delete:1409553551994261504>")
LOADING = DynamicEmoji("loading", "<:icons_loading:1425323212564332648>")

# --- Stats Emojis ---
STATS = DynamicEmoji("stats", "<:stats:1428002716894101655>")
UPTIME = DynamicEmoji("uptime", "<:total:1425322898813485067>")
DATABASE = DynamicEmoji("database", "<:database:1415899333714247713>")
VERIFIED_DEV = DynamicEmoji("verified_dev", "<:VerifiedDeveloper:1409854824010350612>")
OS_SYSTEM = DynamicEmoji("system", "<:System:1428005160361398422>")
CPU = DynamicEmoji("cpu", "<:cpu:1428004267825827981>")
RAM = DynamicEmoji("ram", "<:ram:1428004267704193025>")
STORAGE = DynamicEmoji("storage", "<:Storage:1428004311207510076>")
CROWN = DynamicEmoji("crown", "<:crown:1409553548068524103>")
GEARS = DynamicEmoji("gears", "<:gears:1418984679318618154>")
LINK = DynamicEmoji("link", "<:links:1491494933452820660>")
CREDITS = DynamicEmoji("credits", "<:CreditCard:1428002644940816497>")

# --- Utility Emojis ---
TIMER = DynamicEmoji("timer", "<:icons_uptime:1409377448994406523>")
REPLY = DynamicEmoji("reply", "<:reply:1408031308143132753>")
REPLY_2 = DynamicEmoji("reply", "<:reply:1408031308143132753>")
BELL = DynamicEmoji("bell", "<:BELL:1458697802258583606>")

# --- Role / Status Emojis ---
VIP = DynamicEmoji("vip", "<:vip:1410092948884033589>")
FRIEND = DynamicEmoji("friend", "<:Friend:1410093575621967872>")
VERIFIED = DynamicEmoji("verified", "<:verified:1410092911391146126>")
ENABLED = DynamicEmoji("enabled", "<:enabled:1410218898724360263>")
DISABLED = DynamicEmoji("disabled", "<:disabled:1410218888368619551>")
DISABLED_OFF = DynamicEmoji("disabled_off", "<:disabled:1491719828858474496>")

# Mapping from constant variable name to asset filename in emoji/assets/
ASSET_NAME_MAP = {
    "CHECK": "check",
    "VERIFIED_CHECK": "check",
    "CROSS": "cross",
    "CROSS_MARK": "cross",
    "TICK": "check",
    "ZTICK": "check",
    "ERROR_X": "cross",
    "LOCK": "lock",
    "UNLOCK": "unlock",
    "GHOST": "ghost",
    "UNGHOST": "unghost",
    "BOOST": "boost",
    "INFO": "warning",
    "CART": "cart",
    "SUPPORT": "support",
    "DELETE": "delete",
    "LOADING": "loading",
    "STATS": "stats",
    "UPTIME": "uptime",
    "DATABASE": "database",
    "VERIFIED_DEV": "verified_dev",
    "OS_SYSTEM": "system",
    "CPU": "cpu",
    "RAM": "ram",
    "STORAGE": "storage",
    "CROWN": "crown",
    "GEARS": "gears",
    "LINK": "link",
    "CREDITS": "credits",
    "TIMER": "timer",
    "REPLY": "reply",
    "REPLY_2": "reply",
    "BELL": "bell",
    "VIP": "vip",
    "FRIEND": "friend",
    "VERIFIED": "verified",
    "ENABLED": "enabled",
    "DISABLED": "disabled",
    "DISABLED_OFF": "disabled_off",
}

# --- Compatibility Mappings ---
EMOJIES = {
    "lock": LOCK,
    "unlock": UNLOCK,
    "ghost": GHOST,
    "unghost": UNGHOST,
    "boost": BOOST,
    "info": INFO,
    "cross": CROSS,
    "cart": CART,
    "check": CHECK,
}

ROLE_EMOJIS = {
    "Developer": VERIFIED_DEV,
    "Vip": VIP,
    "Friend": FRIEND,
    "Owner": CROWN,
    "Verified": VERIFIED,
}

# All application emojis loaded from Developer Portal
APPLICATION_EMOJIS: Dict[str, discord.Emoji] = {}


def get_emoji(name: str, fallback: str = "") -> str:
    """Retrieve an application emoji by asset name or fallback to default."""
    name_lower = name.lower()
    if name_lower in APPLICATION_EMOJIS:
        return str(APPLICATION_EMOJIS[name_lower])
    # Check if a constant matches
    for var_name, asset in ASSET_NAME_MAP.items():
        if asset == name_lower and var_name in globals():
            return str(globals()[var_name])
    return fallback


def _apply_cached_emojis():
    """Load cached emoji mappings on startup if available."""
    if not CACHE_FILE.exists():
        return
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cached = json.load(f)
        for var_name, asset in ASSET_NAME_MAP.items():
            if asset in cached and var_name in globals():
                emoji_obj = globals()[var_name]
                if isinstance(emoji_obj, DynamicEmoji):
                    emoji_obj.set_value(cached[asset])
    except Exception as e:
        logger.warning(f"Could not load cached emojis: {e}")


# Preload cache immediately on module import
_apply_cached_emojis()


async def sync_application_emojis(bot: commands.Bot, force_reupload: bool = False) -> Tuple[int, int]:
    """
    Sync all emojis from emoji/assets/ directly to Discord Developer Portal (Application Emojis).
    - If the emoji is not yet uploaded to Developer Portal, uploads it automatically.
    - If it already exists on Developer Portal, binds to the existing emoji.
    - Updates all DynamicEmoji constants in emojis.py in real-time so the entire bot uses them.
    - Saves the synced state to emoji/synced_emojis.json.
    """
    if not ASSETS_DIR.exists():
        print(f"⚠️ [Emoji Sync] Assets directory not found at {ASSETS_DIR}")
        return 0, 0

    print("🔄 [Emoji Sync] Fetching existing Application Emojis from Discord Developer Portal...")
    try:
        existing_emojis = await bot.fetch_application_emojis()
    except Exception as e:
        print(f"❌ [Emoji Sync] Failed to fetch application emojis: {e}")
        return 0, 0

    # Build lookup map by lowercase name
    existing_map: Dict[str, discord.Emoji] = {e.name.lower(): e for e in existing_emojis}
    print(f"ℹ️ [Emoji Sync] Found {len(existing_emojis)} existing emojis in Developer Portal.")

    # Scan emoji/assets directory
    asset_files = [
        f for f in ASSETS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in {".png", ".gif", ".jpg", ".jpeg", ".webp"}
    ]

    synced_map: Dict[str, str] = {}
    uploaded_count = 0
    synced_count = 0

    for file_path in asset_files:
        name = file_path.stem.lower()

        # Check if already present on Developer Portal
        if name in existing_map and not force_reupload:
            emoji = existing_map[name]
            APPLICATION_EMOJIS[name] = emoji
            synced_map[name] = str(emoji)
            synced_count += 1
            continue

        # Upload missing emoji to Developer Portal
        try:
            with open(file_path, "rb") as img_file:
                img_bytes = img_file.read()

            print(f"📤 [Emoji Sync] Uploading '{name}' ({len(img_bytes)} bytes) to Developer Portal...")
            new_emoji = await bot.create_application_emoji(name=name, image=img_bytes)
            APPLICATION_EMOJIS[name] = new_emoji
            synced_map[name] = str(new_emoji)
            uploaded_count += 1
            synced_count += 1
            print(f"✨ [Emoji Sync] Successfully uploaded '{name}' -> {new_emoji}")
        except discord.HTTPException as http_err:
            print(f"❌ [Emoji Sync] HTTP Error uploading '{name}': {http_err}")
            # Fall back to existing if available
            if name in existing_map:
                emoji = existing_map[name]
                APPLICATION_EMOJIS[name] = emoji
                synced_map[name] = str(emoji)
                synced_count += 1
        except Exception as err:
            print(f"❌ [Emoji Sync] Error uploading '{name}': {err}")

    # Update all DynamicEmoji constants in this module
    for var_name, asset in ASSET_NAME_MAP.items():
        if asset in synced_map and var_name in globals():
            emoji_obj = globals()[var_name]
            if isinstance(emoji_obj, DynamicEmoji):
                emoji_obj.set_value(synced_map[asset])

    # Save to cache file
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(synced_map, f, indent=2)
    except Exception as e:
        logger.warning(f"Failed to save emoji cache: {e}")

    print(f"🎉 [Emoji Sync Completed] Total: {synced_count}/{len(asset_files)} synced (Uploaded new: {uploaded_count}).")
    return synced_count, len(asset_files)

import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta, timezone
import math
import os
import random
import re


BOT_TOKEN = ""
PREFIX    = "!"

intents = discord.Intents.default()
intents.message_content = True
intents.members         = True
mother_insults = [
    "я твою мать ебал",
    "я ебал твою мать",
    "сын шлюхи",
    "пошел нахуй",
    "пошел нахуй!",
    "сын бляди",
    "ебу твой рот",
    "твоя мать шлюха",
    "ебать твою мать",
    "твоя мать блядина",
    "твою мать во все щели",
    "твоя мать на хуе вертелась",
    "я твою мать в рот ебал",
    "твоя мать конченая проститутка",
    "твою мать собаки драли",
    "твоя мать на трассе отрабатывает",
    "твоя мать за копейки даёт",
    "твоя мать бомжей обслуживает",
    "твою мать всем двором ебали",
    "твоя мать — общественная дырка",
    "твоя мать на вокзале дежурит",
    "твою мать в жопу долбили",
    "твоя мать грязная шалава",
    "сын хуйни",
    "сын пидора",
    "твоя мать чмошница подзаборная",
    "твою мать ебали во все дыхательные и не очень пути",
    "твоя мать дешёвая подстилка",
    "твоя мать на свинарнике отсосала",
    "твою мать в клоунаду не взяли — сказали, слишком блядская",
    "твоя мать — живой черновик для хуёв",
    "твою мать даже бомжи за свои не считают",
    "твоя мать и конь — лучшие друзья",
    "твою мать кончиной залили",
    "твоя мать — синоним слова 'проёбанная'",
    "твою мать в цирке вместо батута использовали",
    "твоя мать хуями питается",
    "твою мать ебали, пока ты под столом в игрушки играл",
    "твоя мать на весь район банкомат — вставляешь и получаешь",
    "твою мать через форточку дрючили",
    "твоя мать грязнее унитаза на заправке",
    "твою мать даже стыдно называть женщиной",
    "твоя мать на дне рождении гостям раздаёт, а не подарки",
    "нищий"
]
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
packet_data = 3000
receive_data  = 000
DB_PATH = "bot_data.db"

RANK_NAMES = {
    0: "Пользователь",
    1: "Младший модератор",
    2: "Старший модератор",
    3: "Младший администратор",
    4: "Старший администратор",
    5: "Создатель",
}

RANK_EMOJIS = {
    0: "👤",
    1: "🛡️",
    2: "⚔️",
    3: "🔰",
    4: "👑",
    5: "⭐",
}

RP_ACTIONS = {
    "обнять": {
        "emoji": "🤗", "color": 0xFFB6C1,
        "templates": [
            "**{a}** крепко обнял **{t}**",
            "**{a}** обнял **{t}** ",
            "**{a}**  обнял **{t}** ",
            "**{a}** обнял **{t}**",
        ]
    },
    "поцеловать": {
        "emoji": "💋", "color": 0xFF69B4,
        "templates": [
            "**{a}** поцеловал **{t}**! 💋",
            "**{a}** нежно поцеловал **{t}** в щёчку~ 😘",
            "**{a}** поцелуйчик бурмалдатик с  **{t}**!",
            "**{a}** и **{t}** поцеловались",
        ]
    },
    "убить": {
        "emoji": "⚔️", "color": 0xCC0000,
        "templates": [
            "**{a}** убил **{t}**! ☠️",
            "**{a}** ударил ножом в спину **{t}**! 🗡️",
            "**{a}** кильнул **{t}** и кинул диз.",
            "**{a}** одним взглядом убил нахуй **{t}** 👁️",
        ]
    },
    "укусить": {
        "emoji": "😬", "color": 0xFF4500,
        "templates": [
            "**{a}** укусил **{t}**",
            "**{a}** тихонько укусил **{t}**",
            "**{a}** оставил укус на **{t}**! ",
            "**{a}** кусьнул **{t}**",
        ]
    },
    "ударить": {
        "emoji": "👊", "color": 0xFF6347,
        "templates": [
            "**{a}** ударил **{t}** ",
            "**{a}** отвесил **{t}** сладеньку пощечину",
            "**{a}** пнул ногой  **{t}** ",
            "**{a}** чуть не убил  **{t}**",
        ]
    },
    "уебать": {
        "emoji": "💢", "color": 0xFF0000,
        "templates": [
            "**{a}** уебал **{t}** т",
            "**{a}** уебенил **{t}** ",
            "**{a}** так уебал **{t}**, что тот чуть не откис нахуй",
            "**{a}** прописал **{t}** знатных люлей!(типа люля)",
        ]
    },
    "трахнуть": {
        "emoji": "🍆", "color": 0x800080,
        "templates": [
            "**{a}** трахнул **{t}**! надеемся, что**{t}** понравилось",
            "**{a}** и **{t}** уединились. к сожалению подробностей не будет",
            "**{a}** трахнул **{t}** ",
            "**{a}** нежно занялся интимом с  **{t}** ",
        ]
    },
    "выебать": {
        "emoji": "🔥", "color": 0xFF4500,
        "templates": [
            "**{a}** выебал **{t}** ",
            "**{a}** и **{t}** поебались!!!!!",
            "**{a}** жестко трахнул  **{t}** ",
            "**{a}** выебал до посинения **{t}** ",
        ]
    },
}


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c    = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS marriages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id   INTEGER NOT NULL,
            user1_id   INTEGER NOT NULL,
            user2_id   INTEGER NOT NULL,
            start_date TEXT    NOT NULL,
            extra_days INTEGER DEFAULT 0,
            in_rating  INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS divorce_history (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id     INTEGER NOT NULL,
            user1_id     INTEGER NOT NULL,
            user2_id     INTEGER NOT NULL,
            start_date   TEXT    NOT NULL,
            extra_days   INTEGER DEFAULT 0,
            divorce_date TEXT    NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id      INTEGER NOT NULL,
            from_user     INTEGER NOT NULL,
            to_user       INTEGER NOT NULL,
            created_at    TEXT    NOT NULL,
            proposal_type TEXT    DEFAULT 'new'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS mod_ranks (
            guild_id INTEGER NOT NULL,
            user_id  INTEGER NOT NULL,
            rank     INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (guild_id, user_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id    INTEGER NOT NULL,
            reporter_id INTEGER NOT NULL,
            target_id   INTEGER NOT NULL,
            reason      TEXT    NOT NULL,
            created_at  TEXT    NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS message_stats (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id   INTEGER NOT NULL,
            user_id    INTEGER NOT NULL,
            sent_at    TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


def get_mod_rank(guild: discord.Guild, user_id: int) -> int:
    if guild.owner_id == user_id:
        return 5
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT rank FROM mod_ranks WHERE guild_id=? AND user_id=?", (guild.id, user_id))
    row = c.fetchone()
    conn.close()
    return row["rank"] if row else 0


def set_mod_rank(guild_id: int, user_id: int, rank: int):
    conn = get_conn()
    if rank == 0:
        conn.execute("DELETE FROM mod_ranks WHERE guild_id=? AND user_id=?", (guild_id, user_id))
    else:
        conn.execute(
            "INSERT INTO mod_ranks (guild_id, user_id, rank) VALUES (?,?,?) "
            "ON CONFLICT(guild_id, user_id) DO UPDATE SET rank=excluded.rank",
            (guild_id, user_id, rank)
        )
    conn.commit()
    conn.close()


def get_marriage(guild_id: int, user_id: int) -> sqlite3.Row | None:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT * FROM marriages WHERE guild_id=? AND (user1_id=? OR user2_id=?)",
        (guild_id, user_id, user_id)
    )
    row = c.fetchone()
    conn.close()
    return row


def get_partner_id(marriage: sqlite3.Row, user_id: int) -> int:
    return marriage["user2_id"] if marriage["user1_id"] == user_id else marriage["user1_id"]


def marriage_duration(marriage: sqlite3.Row) -> timedelta:
    start = datetime.fromisoformat(marriage["start_date"])
    return (datetime.now() - start) + timedelta(days=marriage["extra_days"])


def fmt_duration(td: timedelta) -> str:
    total   = max(0, int(td.total_seconds()))
    years   = total // (365 * 24 * 3600); total %= (365 * 24 * 3600)
    months  = total // (30  * 24 * 3600); total %= (30  * 24 * 3600)
    days    = total // (24  * 3600);      total %= (24  * 3600)
    hours   = total // 3600;              total %= 3600
    minutes = total // 60
    parts   = []
    if years:   parts.append(f"{years} л.")
    if months:  parts.append(f"{months} мес.")
    if days:    parts.append(f"{days} дн.")
    if hours:   parts.append(f"{hours} ч.")
    if minutes or not parts: parts.append(f"{minutes} мин.")
    return " ".join(parts)


def fmt_relative(dt: datetime) -> str:
    if dt.tzinfo is not None:
        delta = datetime.now(timezone.utc) - dt
    else:
        delta = datetime.now() - dt
    total  = max(0, int(delta.total_seconds()))
    years  = total // (365 * 24 * 3600); total %= (365 * 24 * 3600)
    months = total // (30  * 24 * 3600); total %= (30  * 24 * 3600)
    days   = total // (24  * 3600)
    parts  = []
    if years:  parts.append(f"{years} л.")
    if months: parts.append(f"{months} мес.")
    if days or not parts: parts.append(f"{days} дн.")
    return " ".join(parts)


async def do_divorce(guild_id: int, marriage: sqlite3.Row):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "INSERT INTO divorce_history (guild_id,user1_id,user2_id,start_date,extra_days,divorce_date) VALUES (?,?,?,?,?,?)",
        (guild_id, marriage["user1_id"], marriage["user2_id"],
         marriage["start_date"], marriage["extra_days"], datetime.now().isoformat())
    )
    c.execute("DELETE FROM marriages WHERE id=?", (marriage["id"],))
    conn.commit()
    conn.close()


async def resolve_member(guild: discord.Guild, arg: str, mentions: list) -> discord.Member | None:
    if mentions:
        return mentions[0]
    match = re.search(r'discord\.com/users/(\d+)', arg)
    uid   = int(match.group(1)) if match else (int(arg.strip()) if arg.strip().isdigit() else None)
    if uid:
        try:
            return guild.get_member(uid) or await guild.fetch_member(uid)
        except Exception:
            return None
    return None


def parse_duration(raw: str):
    UNITS  = {"с": 1, "сек": 1, "м": 60, "мин": 60, "ч": 3600, "час": 3600,
               "д": 86400, "дн": 86400, "день": 86400, "н": 604800, "нед": 604800}
    LABELS = {"с": "сек.", "сек": "сек.", "м": "мин.", "мин": "мин.", "ч": "ч.", "час": "ч.",
               "д": "дн.", "дн": "дн.", "день": "дн.", "н": "нед.", "нед": "нед."}
    raw = raw.lower().strip()
    for i, ch in enumerate(raw):
        if not ch.isdigit():
            num, suf = raw[:i], raw[i:].strip()
            if num and suf in UNITS:
                return int(num) * UNITS[suf], f"{num} {LABELS[suf]}"
            return None, None
    return None, None


def embed_error(text: str) -> discord.Embed:
    return discord.Embed(description=f"❌ {text}", color=0xFF4444)


def embed_ok(text: str) -> discord.Embed:
    return discord.Embed(description=f"✅ {text}", color=0x44BB66)


async def get_reply_member(message: discord.Message) -> discord.Member | None:
    ref = message.reference
    if not ref:
        return None
    try:
        replied_msg = ref.resolved or await message.channel.fetch_message(ref.message_id)
        if isinstance(replied_msg, discord.Message) and replied_msg.author and not replied_msg.author.bot:
            return message.guild.get_member(replied_msg.author.id) or await message.guild.fetch_member(replied_msg.author.id)
    except Exception:
        pass
    return None


def record_message(guild_id: int, user_id: int):
    conn = get_conn()
    conn.execute(
        "INSERT INTO message_stats (guild_id, user_id, sent_at) VALUES (?,?,?)",
        (guild_id, user_id, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_stats(guild_id: int, since: datetime | None) -> list[sqlite3.Row]:
    conn = get_conn()
    c    = conn.cursor()
    if since:
        c.execute(
            "SELECT user_id, COUNT(*) as cnt FROM message_stats WHERE guild_id=? AND sent_at>=? GROUP BY user_id ORDER BY cnt DESC LIMIT 10",
            (guild_id, since.isoformat())
        )
    else:
        c.execute(
            "SELECT user_id, COUNT(*) as cnt FROM message_stats WHERE guild_id=? GROUP BY user_id ORDER BY cnt DESC LIMIT 10",
            (guild_id,)
        )
    rows = c.fetchall()
    conn.close()
    return rows


def get_total_messages(guild_id: int, since: datetime | None) -> int:
    conn = get_conn()
    c    = conn.cursor()
    if since:
        c.execute("SELECT COUNT(*) as cnt FROM message_stats WHERE guild_id=? AND sent_at>=?", (guild_id, since.isoformat()))
    else:
        c.execute("SELECT COUNT(*) as cnt FROM message_stats WHERE guild_id=?", (guild_id,))
    row = c.fetchone()
    conn.close()
    return row["cnt"] if row else 0


def get_hourly_stats(guild_id: int) -> list[int]:
    since = datetime.now() - timedelta(hours=24)
    conn  = get_conn()
    c     = conn.cursor()
    c.execute(
        "SELECT strftime('%H', sent_at) as hour, COUNT(*) as cnt FROM message_stats "
        "WHERE guild_id=? AND sent_at>=? GROUP BY hour",
        (guild_id, since.isoformat())
    )
    rows   = c.fetchall()
    conn.close()
    counts = [0] * 24
    for row in rows:
        counts[int(row["hour"])] = row["cnt"]
    return counts


PLACE_MEDALS = {1: "💎", 2: "🏠", 3: "💎🏠", 4: "4.", 5: "5.", 6: "6.", 7: "7.", 8: "8.", 9: "9.", 10: "10."}


async def send_stats(channel: discord.TextChannel, guild: discord.Guild, period: str):
    now = datetime.now()
    if period == "day":
        since = now - timedelta(hours=24)
        label = "ЗА СУТКИ (24 ЧАСА)"
    elif period == "week":
        since = now - timedelta(weeks=1)
        label = "ЗА НЕДЕЛЮ"
    elif period == "month":
        since = now - timedelta(days=30)
        label = "ЗА МЕСЯЦ"
    else:
        since = None
        label = "ЗА ВСЁ ВРЕМЯ"

    rows  = get_stats(guild.id, since)
    total = get_total_messages(guild.id, since)

    if not rows:
        return await channel.send(embed=discord.Embed(
            description="📭 Нет данных о сообщениях за этот период.", color=0x888888
        ))

    lines = []
    for i, row in enumerate(rows, start=1):
        member = guild.get_member(row["user_id"])
        name   = member.display_name if member else f"ID:{row['user_id']}"
        medal  = PLACE_MEDALS.get(i, f"{i}.")
        cnt    = f"{row['cnt']:,}".replace(",", " ")
        lines.append(f"{medal} {name} — {cnt}")

    desc = "\n".join(lines) + f"\n\nВсего сообщений: {total:,}".replace(",", " ")
    e = discord.Embed(
        title=f"📊 СТАТИСТИКА ПО ОБЩИТЕЛЬНЫМ ПОЛЬЗОВАТЕЛЯМ\n{label}",
        description=desc,
        color=0x5865F2
    )
    await channel.send(embed=e)


async def send_hourly_stats(channel: discord.TextChannel, guild: discord.Guild):
    counts = get_hourly_stats(guild.id)
    total  = sum(counts)
    if total == 0:
        return await channel.send(embed=discord.Embed(
            description="📭 Нет данных о сообщениях за последние 24 часа.", color=0x888888
        ))

    now_h   = datetime.now().hour
    max_val = max(counts) if max(counts) > 0 else 1
    BAR_LEN = 12

    lines = []
    for h in range(24):
        cnt      = counts[h]
        filled   = round(BAR_LEN * cnt / max_val) if cnt > 0 else 0
        bar      = "█" * filled + "░" * (BAR_LEN - filled)
        marker   = " ◄" if h == now_h else ""
        cnt_str  = f"{cnt:,}".replace(",", " ")
        lines.append(f"`{h:02d}ч` {bar} {cnt_str}{marker}")

    desc = "\n".join(lines) + f"\n\nВсего сообщений: {total:,}".replace(",", " ")
    e = discord.Embed(
        title="📊 АКТИВНОСТЬ ПО ЧАСАМ (24 ЧАСА)",
        description=desc,
        color=0x5865F2
    )
    await channel.send(embed=e)


async def build_profile_embed(member: discord.Member) -> discord.Embed:
    rank       = get_mod_rank(member.guild, member.id)
    rank_name  = RANK_NAMES[rank]
    rank_emoji = RANK_EMOJIS[rank]
    roles    = [r for r in reversed(member.roles) if r.name != "@everyone"]
    top_role = roles[0] if roles else None
    created_str = member.created_at.strftime("%d.%m.%Y") + f" ({fmt_relative(member.created_at)})"
    joined_str  = (member.joined_at.strftime("%d.%m.%Y") + f" ({fmt_relative(member.joined_at)})") if member.joined_at else "—"
    sorted_members = sorted(
        [m for m in member.guild.members if not m.bot],
        key=lambda m: m.joined_at or datetime.now(timezone.utc)
    )
    join_pos = next((i + 1 for i, m in enumerate(sorted_members) if m.id == member.id), "—")
    marriage = get_marriage(member.guild.id, member.id)
    if marriage:
        pid          = get_partner_id(marriage, member.id)
        partner      = member.guild.get_member(pid)
        marriage_str = f"{partner.mention if partner else f'<@{pid}>'} ({fmt_duration(marriage_duration(marriage))})"
    else:
        marriage_str = "Не в браке"
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT COUNT(*) as cnt FROM reports WHERE guild_id=? AND target_id=?", (member.guild.id, member.id))
    report_count = c.fetchone()["cnt"]
    conn.close()
    color = top_role.color if top_role and top_role.color.value else 0x5865F2
    role_lines = "\n".join(f"・{r.mention}" for r in roles[:6]) or "・Нет ролей"
    if len(roles) > 6:
        role_lines += f"\n・*...и ещё {len(roles) - 6}*"
    flags      = member.public_flags
    USER_FLAGS = {
        "staff": "👨‍💼 Сотрудник Discord",
        "partner": "🤝 Партнёр Discord",
        "hypesquad_bravery": "🟠 HypeSquad Bravery",
        "hypesquad_brilliance": "🟣 HypeSquad Brilliance",
        "hypesquad_balance": "🟢 HypeSquad Balance",
        "early_supporter": "💜 Early Supporter",
        "verified_bot_developer": "🤖 Verified Bot Dev",
        "active_developer": "👾 Active Developer",
        "bug_hunter_level_2": "🏅 Bug Hunter Lv.2",
    }
    badge_list = [label for attr, label in USER_FLAGS.items() if getattr(flags, attr, False)]
    e = discord.Embed(color=color)
    e.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    e.set_thumbnail(url=member.display_avatar.url)
    e.description = (
        f"👤 **Это пользователь** — {top_role.mention if top_role else '—'}\n"
        f"{role_lines}"
    )
    e.add_field(
        name="🪪 Основное",
        value=(
            f"**Тег:** {member}\n"
            f"**ID:** `{member.id}`"
        ),
        inline=True
    )
    e.add_field(
        name=f"{rank_emoji} Ранг на сервере",
        value=(
            f"**[{rank}] {rank_name}**\n"
            f"**Позиция захода:** #{join_pos}"
        ),
        inline=True
    )
    e.add_field(name="\u200b", value="\u200b", inline=False)
    e.add_field(name="📅 Регистрация в Discord", value=created_str, inline=True)
    e.add_field(name="📅 На сервере с",          value=joined_str,  inline=True)
    e.add_field(name="\u200b", value="\u200b", inline=False)
    e.add_field(name="💍 Брак",    value=marriage_str,          inline=True)
    e.add_field(name="📢 Репорты", value=f"{report_count} шт.", inline=True)
    if badge_list:
        e.add_field(name="🏅 Значки Discord", value="\n".join(badge_list), inline=False)
    e.set_footer(text=f"Запрошено {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    return e


async def send_help(channel: discord.TextChannel):
    e1 = discord.Embed(title="📖 Все команды бота", color=0x5865F2)
    e1.add_field(
        name="⭐ Система рангов модераторов",
        value=(
            "Ранги назначаются внутри бота и не зависят от ролей Discord.\n"
            "Владелец сервера всегда имеет **ранг 5 (Создатель)**.\n\n"
            "**Ранги:**\n"
            "`[1]` 🛡️ Младший модератор\n"
            "`[2]` ⚔️ Старший модератор\n"
            "`[3]` 🔰 Младший администратор\n"
            "`[4]` 👑 Старший администратор\n"
            "`[5]` ⭐ Создатель\n\n"
            "**Назначение ранга** (нужен ранг выше цели):\n"
            "`+Модер @user` / `+админ @user` / `Повысить @user` → ранг 1\n"
            "`+Модер 2 @user` / `+админ 2 @user` / `Повысить 2 @user` → ранг 2\n"
            "`+Модер 3 @user` / `Повысить 3 @user` → ранг 3\n"
            "`+Модер 4 @user` / `Повысить 4 @user` → ранг 4\n"
            "`+Модер 5 @user` / `Повысить 5 @user` → ранг 5 (только владелец)\n\n"
            "**Через восклицательные знаки:**\n"
            "`!модер @user` → ранг 1\n"
            "`!!модер @user` → ранг 2\n"
            "`!!!модер @user` → ранг 3\n"
            "`!!!!модер @user` → ранг 4\n\n"
            "**Повышение/понижение:**\n"
            "`Повысить @user` — +1 ранг\n"
            "`Понизить @user` — -1 ранг\n\n"
            "**Снятие:**\n"
            "`Снять @user` / `Разжаловать @user` — убрать все права"
        ),
        inline=False
    )
    await channel.send(embed=e1)
    e2 = discord.Embed(title="🔨 Модерация", color=0xFF4444)
    e2.add_field(
        name="Требуемые ранги",
        value=(
            "**`!бан @user [причина]`** — *(ранг 2+)*\n"
            "┗ Банит участника сервера. Также работает **ответом** на сообщение без @упоминания.\n\n"
            "**`!мут @user <время> [причина]`** — *(ранг 1+)*\n"
            "┗ Таймаут. Форматы: `30с` `10м` `2ч` `1д` `1н`. Макс: 28 дней.\n"
            "┗ Также работает **ответом**: `!мут 10м причина`\n\n"
            "**`!размут @user [причина]`** — *(ранг 1+)*\n"
            "┗ Снимает таймаут. Также работает ответом.\n\n"
            "**`!банлист [стр.]`** — *(ранг 2+)*\n"
            "┗ Список всех забаненных участников.\n\n"
            "**`!мутлист [стр.]`** — *(ранг 1+)*\n"
            "┗ Список всех замученных участников."
        ),
        inline=False
    )
    await channel.send(embed=e2)
    e3 = discord.Embed(title="📢 Репорты", color=0xFF9900)
    e3.add_field(
        name="Команды репортов",
        value=(
            "**`!репорт @user причина`** — *(все)*\n"
            "┗ Отправить жалобу на пользователя.\n\n"
            "**`!репортлист [@user] [стр.]`** — *(ранг 1+)*\n"
            "┗ Просмотр репортов сервера. С @user — только на него.\n\n"
            "**`!очиститьрепорты [@user]`** — *(ранг 3+)*\n"
            "┗ Удалить репорты. Без @user — удалить все."
        ),
        inline=False
    )
    await channel.send(embed=e3)
    e4 = discord.Embed(title="👤 Профиль", color=0x5865F2)
    e4.add_field(
        name="Просмотр профиля",
        value=(
            "**`!кто я`** — *(все)*\n"
            "┗ Показывает **ваш собственный** профиль.\n\n"
            "**`кто ты @user`** / **`профиль @user`** — *(все)*\n"
            "┗ Показывает профиль другого пользователя.\n"
            "┗ Принимает @упоминание, числовой ID или ссылку `discord.com/users/ID`.\n"
            "┗ **Ответом** на сообщение: `кто ты` без аргументов — покажет профиль автора.\n\n"
            "**`кто админ`** — *(все)*\n"
            "┗ Список всех модераторов и администраторов сервера (ранг 1+)."
        ),
        inline=False
    )
    await channel.send(embed=e4)
    e5 = discord.Embed(title="🎮 Развлечения", color=0xFF69B4)
    e5.add_field(
        name="Шипперинг",
        value=(
            "**`!шипперим`** — *(все)*\n"
            "┗ Шипперит вас с рандомным участником. Генерирует шип-имя и процент совместимости."
        ),
        inline=False
    )
    e5.add_field(
        name="💫 РП-действия — *(все)*",
        value=(
            "`обнять @user` · `поцеловать @user` · `укусить @user`\n"
            "`ударить @user` · `убить @user` · `уебать @user`\n"
            "`трахнуть @user` · `выебать @user`\n\n"
            "┗ Без префикса `!`. Причина — со второй строки:\n"
            "```\nтрахнуть @user\nпотому что хочу\n```"
            "┗ **Ответом** на сообщение: просто напишите действие без @упоминания."
        ),
        inline=False
    )
    await channel.send(embed=e5)
    e6 = discord.Embed(title="💍 Браки", color=0xFF69B4)
    e6.add_field(
        name="Создание и расторжение — *(все)*",
        value=(
            "**`Брак @user`** — предложение. При разводе < 3 дней назад — предложит восстановить.\n"
            "**`Брак да`** / **`Брак нет`** — ответ на предложение.\n"
            "**`!Развод`** — расторгнуть свой брак (восстановление доступно 3 дня)."
        ),
        inline=False
    )
    e6.add_field(
        name="Информация — *(все)*",
        value=(
            "**`Мой брак`** — ваш брак.\n"
            "**`Твой брак @user`** — брак указанного пользователя.\n"
            "**`Браки [стр.]`** — список всех браков сервера."
        ),
        inline=False
    )
    e6.add_field(
        name="Рейтинг — *(все)*",
        value=(
            "**`Топ браков [стр.]`** — топ по сроку брака.\n"
            "**`+Брак рейтинг`** / **`-Брак рейтинг`** — войти/выйти из топа."
        ),
        inline=False
    )
    e6.add_field(
        name="Управление — *(ранг 3+)*",
        value=(
            "**`Поженить пару @u1 @u2`** — зарегистрировать брак принудительно.\n"
            "**`Развести пару @u1 @u2`** — расторгнуть брак принудительно.\n"
            "**`!Сброс браков`** — удалить все браки на сервере.\n"
            "**`Развести вышедших`** — развести пары с покинувшими участниками.\n"
            "**`Брак режим развода выключить | один | оба`** — авторазвод при выходе.\n"
            "**`Брак продлить <дни>`** / **`Продлить брак <дни>`** — продлить свой брак."
        ),
        inline=False
    )
    await channel.send(embed=e6)
    e7 = discord.Embed(title="📊 Статистика сообщений", color=0x5865F2)
    e7.add_field(
        name="Команды статистики — *(все)*",
        value=(
            "**`Чат стата по часам`** — почасовая активность за 24 часа (график).\n\n"
            "**`Стата сутки`** / `Стата` / `Топ` / `Топ сутки` — топ за сутки.\n\n"
            "**`Стата неделя`** / `Топ неделя` — топ за 7 дней.\n\n"
            "**`Стата месяц`** / `Топ месяц` — топ за 30 дней.\n\n"
            "**`Стата вся`** / `Топ вся` — топ за всё время."
        ),
        inline=False
    )
    await channel.send(embed=e7)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="шоб не творили хуйни"
    ))
    print(f"Бот запущен: {bot.user} (ID: {bot.user.id}) | Серверов: {len(bot.guilds)}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


@bot.event
async def on_member_remove(member: discord.Member):
    marriage = get_marriage(member.guild.id, member.id)
    if not marriage:
        return
    await do_divorce(member.guild.id, marriage)


@bot.command(name="бан")
async def cmd_ban(ctx, member: discord.Member = None, *, reason: str = "Причина не указана"):
    if get_mod_rank(ctx.guild, ctx.author.id) < 2:
        return await ctx.send(embed=embed_error("Требуется ранг **[2] Старший модератор** или выше."))
    if not member:
        member = await get_reply_member(ctx.message)
    if not member:
        return await ctx.send(embed=discord.Embed(
            title="🔨 Бан — использование",
            description=(
                "`!бан @пользователь [причина]`\n"
                "Или **ответом** на сообщение: `!бан [причина]`"
            ),
            color=0x7289DA
        ))
    if member == ctx.author:
        return await ctx.send(embed=embed_error("Нельзя забанить самого себя."))
    if member == ctx.guild.owner:
        return await ctx.send(embed=embed_error("Нельзя забанить владельца сервера."))
    if get_mod_rank(ctx.guild, member.id) >= get_mod_rank(ctx.guild, ctx.author.id):
        return await ctx.send(embed=embed_error("Нельзя забанить пользователя с равным или более высоким рангом."))
    try:
        await member.ban(reason=f"{ctx.author} | {reason}", delete_message_days=0)
    except discord.Forbidden:
        return await ctx.send(embed=embed_error("Недостаточно прав бота для бана."))
    e = discord.Embed(title="🔨 Пользователь забанен", color=0xFF4444)
    e.add_field(name="Пользователь", value=f"{member} ({member.id})", inline=False)
    e.add_field(name="Модератор",    value=ctx.author.mention,        inline=True)
    e.add_field(name="Причина",      value=reason,                    inline=True)
    e.set_thumbnail(url=member.display_avatar.url)
    e.timestamp = datetime.now()
    await ctx.send(embed=e)


@bot.command(name="мут")
async def cmd_mute(ctx, member_or_duration: str = None, duration_or_reason: str = None, *, reason: str = "Причина не указана"):
    if get_mod_rank(ctx.guild, ctx.author.id) < 1:
        return await ctx.send(embed=embed_error("Требуется ранг **[1] Младший модератор** или выше."))
    member   = None
    duration = None
    reply_member = await get_reply_member(ctx.message)
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
        duration = member_or_duration if member_or_duration and not member_or_duration.startswith("<@") else duration_or_reason
        raw_args = ctx.message.content.split()
        mention_str = f"<@{member.id}>"
        alt_mention = f"<@!{member.id}>"
        filtered = [a for a in raw_args[1:] if a not in (mention_str, alt_mention)]
        duration = filtered[0] if filtered else None
        if filtered and len(filtered) > 1:
            reason = " ".join(filtered[1:])
    elif reply_member:
        member   = reply_member
        duration = member_or_duration
        if duration_or_reason:
            reason = duration_or_reason + (" " + reason if reason != "Причина не указана" else "")
    if not member or not duration:
        return await ctx.send(embed=discord.Embed(
            title="🔇 Мут — использование",
            description=(
                "`!мут @пользователь <время> [причина]`\n"
                "Или **ответом**: `!мут <время> [причина]`\n"
                "**Форматы:** `30с` · `10м` · `2ч` · `1д` · `1н`"
            ),
            color=0x7289DA
        ))
    seconds, label = parse_duration(duration)
    if seconds is None:
        return await ctx.send(embed=embed_error("Неверный формат времени. Примеры: `30с`, `10м`, `2ч`, `1д`, `1н`"))
    if seconds > 28 * 24 * 3600:
        return await ctx.send(embed=embed_error("Максимальная длительность — 28 дней."))
    if member == ctx.author:
        return await ctx.send(embed=embed_error("Нельзя замутить самого себя."))
    if member == ctx.guild.owner:
        return await ctx.send(embed=embed_error("Нельзя замутить владельца сервера."))
    if get_mod_rank(ctx.guild, member.id) >= get_mod_rank(ctx.guild, ctx.author.id):
        return await ctx.send(embed=embed_error("Нельзя замутить пользователя с равным или более высоким рангом."))
    try:
        await member.timeout(discord.utils.utcnow() + timedelta(seconds=seconds), reason=f"{ctx.author} | {reason}")
    except discord.Forbidden:
        return await ctx.send(embed=embed_error("Недостаточно прав бота для мута."))
    e = discord.Embed(title="🔇 Пользователь замучен", color=0xFF9900)
    e.add_field(name="Пользователь", value=f"{member} ({member.id})", inline=False)
    e.add_field(name="Длительность", value=label,             inline=True)
    e.add_field(name="Модератор",    value=ctx.author.mention, inline=True)
    e.add_field(name="Причина",      value=reason,             inline=False)
    e.set_thumbnail(url=member.display_avatar.url)
    e.timestamp = datetime.now()
    await ctx.send(embed=e)


@bot.command(name="размут", aliases=["unmute"])
async def cmd_unmute(ctx, member: discord.Member = None, *, reason: str = "Причина не указана"):
    if get_mod_rank(ctx.guild, ctx.author.id) < 1:
        return await ctx.send(embed=embed_error("Требуется ранг **[1] Младший модератор** или выше."))
    if not member:
        member = await get_reply_member(ctx.message)
    if not member:
        return await ctx.send(embed=embed_error(
            "Укажите пользователя: `!размут @пользователь`\n"
            "Или ответьте на его сообщение: `!размут`"
        ))
    try:
        await member.timeout(None, reason=f"{ctx.author} | {reason}")
    except discord.Forbidden:
        return await ctx.send(embed=embed_error("Недостаточно прав бота."))
    e = discord.Embed(title="🔊 Мут снят", color=0x44BB66)
    e.add_field(name="Пользователь", value=member.mention,    inline=True)
    e.add_field(name="Модератор",    value=ctx.author.mention, inline=True)
    await ctx.send(embed=e)


@bot.command(name="банлист")
async def cmd_banlist(ctx, page: int = 1):
    if get_mod_rank(ctx.guild, ctx.author.id) < 2:
        return await ctx.send(embed=embed_error("Требуется ранг **[2] Старший модератор** или выше."))
    bans = [entry async for entry in ctx.guild.bans()]
    if not bans:
        return await ctx.send(embed=discord.Embed(description="✅ Забаненных участников нет.", color=0x888888))
    per_page    = 10
    total_pages = max(1, math.ceil(len(bans) / per_page))
    page        = max(1, min(page, total_pages))
    lines = [
        f"🔨 **{e.user}** (`{e.user.id}`) — {e.reason or 'Причина не указана'}"
        for e in bans[(page - 1) * per_page : page * per_page]
    ]
    e = discord.Embed(title=f"🔨 Список банов — стр. {page}/{total_pages}", description="\n".join(lines), color=0xFF4444)
    e.set_footer(text=f"Всего забанено: {len(bans)}")
    await ctx.send(embed=e)


@bot.command(name="мутлист")
async def cmd_mutelist(ctx, page: int = 1):
    if get_mod_rank(ctx.guild, ctx.author.id) < 1:
        return await ctx.send(embed=embed_error("Требуется ранг **[1] Младший модератор** или выше."))
    muted = [m for m in ctx.guild.members if m.timed_out_until and m.timed_out_until > discord.utils.utcnow()]
    if not muted:
        return await ctx.send(embed=discord.Embed(description="🔊 Замученных участников нет.", color=0x888888))
    per_page    = 10
    total_pages = max(1, math.ceil(len(muted) / per_page))
    page        = max(1, min(page, total_pages))
    lines = []
    for m in muted[(page - 1) * per_page : page * per_page]:
        remaining = m.timed_out_until.replace(tzinfo=None) - datetime.utcnow()
        lines.append(f"🔇 **{m.display_name}** — осталось {fmt_duration(remaining)}")
    e = discord.Embed(title=f"🔇 Замученные — стр. {page}/{total_pages}", description="\n".join(lines), color=0xFF9900)
    e.set_footer(text=f"Всего: {len(muted)}")
    await ctx.send(embed=e)


@bot.command(name="репорт")
async def cmd_report(ctx, member: discord.Member = None, *, reason: str = None):
    if not member or not reason:
        return await ctx.send(embed=discord.Embed(
            title="📢 Репорт — использование",
            description="`!репорт @пользователь причина`",
            color=0x7289DA
        ))
    if member == ctx.author:
        return await ctx.send(embed=embed_error("Нельзя репортить самого себя."))
    if member.bot:
        return await ctx.send(embed=embed_error("Нельзя репортить бота."))
    conn = get_conn()
    conn.execute(
        "INSERT INTO reports (guild_id, reporter_id, target_id, reason, created_at) VALUES (?,?,?,?,?)",
        (ctx.guild.id, ctx.author.id, member.id, reason, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    e = discord.Embed(title="📢 Репорт отправлен", color=0xFF9900)
    e.add_field(name="На кого", value=f"{member} ({member.id})", inline=False)
    e.add_field(name="Причина", value=reason,                    inline=False)
    e.add_field(name="От кого", value=ctx.author.mention,        inline=True)
    e.set_thumbnail(url=member.display_avatar.url)
    e.timestamp = datetime.now()
    await ctx.send(embed=e)


@bot.command(name="репортлист")
async def cmd_reportlist(ctx, member: discord.Member = None, page: int = 1):
    if get_mod_rank(ctx.guild, ctx.author.id) < 1:
        return await ctx.send(embed=embed_error("Требуется ранг **[1] Младший модератор** или выше."))
    conn = get_conn()
    c    = conn.cursor()
    if member:
        c.execute("SELECT * FROM reports WHERE guild_id=? AND target_id=? ORDER BY created_at DESC", (ctx.guild.id, member.id))
    else:
        c.execute("SELECT * FROM reports WHERE guild_id=? ORDER BY created_at DESC", (ctx.guild.id,))
    all_r = c.fetchall()
    conn.close()
    if not all_r:
        return await ctx.send(embed=discord.Embed(description="📭 Репортов нет.", color=0x888888))
    per_page    = 8
    total_pages = max(1, math.ceil(len(all_r) / per_page))
    page        = max(1, min(page, total_pages))
    lines = []
    for r in all_r[(page - 1) * per_page : page * per_page]:
        reporter = ctx.guild.get_member(r["reporter_id"])
        target   = ctx.guild.get_member(r["target_id"])
        date_str = datetime.fromisoformat(r["created_at"]).strftime("%d.%m %H:%M")
        lines.append(
            f"`[{date_str}]` **{target.display_name if target else r['target_id']}** "
            f"← {reporter.display_name if reporter else r['reporter_id']}: {r['reason']}"
        )
    title = f"📋 Репорты" + (f" на {member.display_name}" if member else "") + f" — стр. {page}/{total_pages}"
    e = discord.Embed(title=title, description="\n".join(lines), color=0xFF9900)
    e.set_footer(text=f"Всего: {len(all_r)}")
    await ctx.send(embed=e)


@bot.command(name="очиститьрепорты")
async def cmd_clear_reports(ctx, member: discord.Member = None):
    if get_mod_rank(ctx.guild, ctx.author.id) < 3:
        return await ctx.send(embed=embed_error("Требуется ранг **[3] Младший администратор** или выше."))
    conn = get_conn()
    if member:
        conn.execute("DELETE FROM reports WHERE guild_id=? AND target_id=?", (ctx.guild.id, member.id))
        msg = f"Репорты на {member.mention} удалены."
    else:
        conn.execute("DELETE FROM reports WHERE guild_id=?", (ctx.guild.id,))
        msg = "Все репорты на сервере удалены."
    conn.commit()
    conn.close()
    await ctx.send(embed=embed_ok(msg))


@bot.command(name="шипперим")
async def cmd_ship(ctx):
    members = [m for m in ctx.guild.members if not m.bot and m != ctx.author]
    if not members:
        return await ctx.send(embed=embed_error("На сервере недостаточно участников."))
    u1, u2    = ctx.author, random.choice(members)
    n1, n2    = u1.display_name, u2.display_name
    ship_name = n1[:max(1, len(n1) // 2)] + n2[max(0, len(n2) // 2):]
    compat    = random.randint(50, 100)
    hearts    = "❤️" * (compat // 10) + "🖤" * (10 - compat // 10)
    TEMPLATES = [
        f"💘 **{u1.mention}** и **{u2.mention}** созданы друг для друга! Шип: **{ship_name}**",
        f"💞 Вселенная решила: **{u1.mention}** + **{u2.mention}** = ❤️ **{ship_name}**",
        f"🔥 **{u1.mention}** и **{u2.mention}** — огонь! Имя шипа: **{ship_name}** 💕",
        f"💌 Любовный радар: **{u1.mention}** влюблён(а) в **{u2.mention}**! Шип: **{ship_name}**",
    ]
    e = discord.Embed(title="💘 Шипперим!", description=random.choice(TEMPLATES), color=0xFF69B4)
    e.add_field(name="Совместимость", value=f"{hearts} {compat}%", inline=False)
    await ctx.send(embed=e)


@bot.command(name="кто")
async def cmd_who(ctx, *, arg: str = None):
    if arg is None or arg.strip().lower() == "я":
        member = ctx.author
    else:
        member = await resolve_member(ctx.guild, arg, ctx.message.mentions)
    if not member:
        return await ctx.send(embed=embed_error("Пользователь не найден. Укажите @упоминание, ID или `я`."))
    await ctx.send(embed=await build_profile_embed(member))


@bot.command(name="профиль")
async def cmd_profile(ctx, *, arg: str = None):
    if arg is None or arg.strip().lower() == "я":
        member = ctx.author
    else:
        member = await resolve_member(ctx.guild, arg, ctx.message.mentions)
    if not member:
        return await ctx.send(embed=embed_error("Пользователь не найден."))
    await ctx.send(embed=await build_profile_embed(member))


@bot.command(name="команды", aliases=["помощь", "help"])
async def cmd_help(ctx):
    await send_help(ctx.channel)
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return

    if not message.content.startswith("!"):
        record_message(message.guild.id, message.author.id)

    await bot.process_commands(message)
    lines     = message.content.strip().split("\n")
    raw       = lines[0].strip()
    reason_rp = lines[1].strip() if len(lines) > 1 else None
    lower     = raw.lower()
    guild_id  = message.guild.id
    author    = message.author
    ch        = message.channel
    my_rank   = get_mod_rank(message.guild, author.id)

    if lower in ("!команды", "!помощь", "!help"):
        await send_help(ch)
        return

    STATS_TRIGGERS = {
        "чат стата по часам": "hourly",
        "стата сутки": "day",
        "стата": "day",
        "топ": "day",
        "топ сутки": "day",
        "стата неделя": "week",
        "топ неделя": "week",
        "стата месяц": "month",
        "топ месяц": "month",
        "стата вся": "all",
        "топ вся": "all",
    }
    
    # ===== ОСКОРБЛЕНИЯ МАТЕРИ (МУТ И СООБЩЕНИЕ) =====
    if lower in mother_insults:
        target = message.author  # мутим автора сообщения
        try:
            await ch.send("Я ВЫРЕЖУ ТВОЮ СЕМЬЮ НА КУСКИ И СКОРМЛЮ ИХ ТЕБЕ ЖЕ В ЖОПУ ЧЕРЕЗ ВОРОНКУ, А ПОТОМ ВЫЕБУ ТО ЧТО ОСТАНЕТСЯ, ТЫ КОНЧЕННЫЙ КУСОК КАЛА, ТВОЯ МАТЬ СДОХЛА ОТ РАКА ПИЗДЫ ПОКА ТЫ ДРОЧИЛ НА ЕЁ ФОТО, УЁБИЩЕ")
            await target.timeout(discord.utils.utcnow() + timedelta(seconds=120))
        except discord.Forbidden:
            await ch.send("пока что поживи ебучий выблядок")
        return

    # Получение участника из упоминания для статистики
    member_for_stats = None
    if message.mentions:
        member_for_stats = message.mentions[0]
    
    if lower in STATS_TRIGGERS:
        period = STATS_TRIGGERS[lower]
        if period == "hourly":
            await send_hourly_stats(ch, message.guild)
        else:
            await send_stats(ch, message.guild, period)
        return

    if lower == "кто ты" or lower.startswith("кто ты ") or lower == "профиль" or lower.startswith("профиль "):
        if lower in ("кто ты", "профиль"):
            reply_m = await get_reply_member(message)
            member  = reply_m if reply_m else author
        else:
            arg    = raw[7:].strip() if lower.startswith("кто ты ") else raw[8:].strip()
            member = await resolve_member(message.guild, arg, message.mentions)
            if not member:
                reply_m = await get_reply_member(message)
                member  = reply_m if reply_m else None
        if not member:
            return await ch.send(embed=embed_error("Пользователь не найден. Укажите @упоминание, ID или ссылку."))
        await ch.send(embed=await build_profile_embed(member))
        return

    if lower == "кто админ":
        conn = get_conn()
        c    = conn.cursor()
        c.execute(
            "SELECT user_id, rank FROM mod_ranks WHERE guild_id=? AND rank >= 1 ORDER BY rank DESC",
            (guild_id,)
        )
        rows = c.fetchall()
        conn.close()
        lines_admin = []
        owner = message.guild.owner
        owner_in_list = any(r["user_id"] == message.guild.owner_id for r in rows)
        if owner and not owner_in_list:
            lines_admin.append(
                f"{RANK_EMOJIS[5]} **[5] {RANK_NAMES[5]}** — {owner.mention} (`{owner.display_name}`)"
            )
        for row in rows:
            m    = message.guild.get_member(row["user_id"])
            rank = row["rank"]
            name = m.display_name if m else f"ID:{row['user_id']}"
            mention = m.mention if m else f"<@{row['user_id']}>"
            lines_admin.append(
                f"{RANK_EMOJIS[rank]} **[{rank}] {RANK_NAMES[rank]}** — {mention} (`{name}`)"
            )
        if not lines_admin:
            return await ch.send(embed=discord.Embed(
                description="😶 На сервере нет назначенных модераторов.",
                color=0x888888
            ))
        e = discord.Embed(
            title="👮 Администрация сервера",
            description="\n".join(lines_admin),
            color=0x5865F2
        )
        e.set_footer(text=f"Всего: {len(lines_admin)} чел.")
        await ch.send(embed=e)
        return

    for prefix_pattern in [
        ("+модер",       "assign"),
        ("+админ",       "assign"),
        ("повысить",     "promote_or_assign"),
        ("понизить",     "demote"),
        ("снять",        "remove"),
        ("разжаловать",  "remove"),
    ]:
        pfx, action = prefix_pattern
        if lower.startswith(pfx):
            rest   = lower[len(pfx):].strip()
            target = None
            rank_num = None
            if action in ("assign", "promote_or_assign"):
                num_match = re.match(r'^(\d+)\s*', rest)
                if num_match:
                    rank_num = int(num_match.group(1))
                    rest     = rest[num_match.end():].strip()
                else:
                    rank_num = 1 if action == "assign" else None
                target = await resolve_member(message.guild, rest, message.mentions)
                if not target:
                    continue
                if action == "promote_or_assign" and rank_num is None:
                    cur      = get_mod_rank(message.guild, target.id)
                    rank_num = min(cur + 1, 5)
            elif action == "demote":
                target = await resolve_member(message.guild, rest, message.mentions)
                if not target:
                    continue
                cur      = get_mod_rank(message.guild, target.id)
                rank_num = max(cur - 1, 0)
                action   = "assign"
            elif action == "remove":
                target   = await resolve_member(message.guild, rest, message.mentions)
                rank_num = 0
                action   = "assign"
            if target:
                if rank_num is None:
                    rank_num = 1
                if rank_num > 5 or rank_num < 0:
                    await ch.send(embed=embed_error("Ранг должен быть от 0 до 5."))
                    return
                target_rank = get_mod_rank(message.guild, target.id)
                if target == author:
                    await ch.send(embed=embed_error("Нельзя изменить собственный ранг."))
                    return
                if rank_num >= 5 and message.guild.owner_id != author.id:
                    await ch.send(embed=embed_error("Ранг **[5] Создатель** может назначить только владелец сервера."))
                    return
                if my_rank <= target_rank and rank_num > 0:
                    await ch.send(embed=embed_error("Нельзя изменить ранг пользователя с равным или более высоким рангом."))
                    return
                if my_rank <= rank_num and rank_num > 0:
                    await ch.send(embed=embed_error("Нельзя назначить ранг равный или выше вашего."))
                    return
                if rank_num == 0:
                    if my_rank <= target_rank:
                        await ch.send(embed=embed_error("Нельзя снять пользователя с равным или более высоким рангом."))
                        return
                    set_mod_rank(guild_id, target.id, 0)
                    await ch.send(embed=embed_ok(f"С {target.mention} снят ранг модератора."))
                else:
                    set_mod_rank(guild_id, target.id, rank_num)
                    emoji = RANK_EMOJIS[rank_num]
                    name  = RANK_NAMES[rank_num]
                    await ch.send(embed=embed_ok(
                        f"{target.mention} назначен ранг {emoji} **[{rank_num}] {name}**."
                    ))
                return

    excl_match = re.match(r'^(!{1,4})модер\s+', lower)
    if excl_match:
        excl_count = len(excl_match.group(1))
        rank_num   = min(excl_count, 4)
        rest       = raw[excl_match.end():].strip()
        target     = await resolve_member(message.guild, rest, message.mentions)
        if target:
            target_rank = get_mod_rank(message.guild, target.id)
            if target == author:
                return await ch.send(embed=embed_error("Нельзя изменить собственный ранг."))
            if my_rank <= target_rank:
                return await ch.send(embed=embed_error("Нельзя изменить ранг пользователя с равным или более высоким рангом."))
            if my_rank <= rank_num:
                return await ch.send(embed=embed_error("Нельзя назначить ранг равный или выше вашего."))
            set_mod_rank(guild_id, target.id, rank_num)
            await ch.send(embed=embed_ok(
                f"{target.mention} назначен ранг {RANK_EMOJIS[rank_num]} **[{rank_num}] {RANK_NAMES[rank_num]}**."
            ))
            return

    for action_key, action_data in RP_ACTIONS.items():
        if lower.startswith(action_key + " ") and message.mentions:
            target = message.mentions[0]
            if target == author:
                await ch.send(embed=embed_error("Нельзя это делать с самим собой!"))
                return
            text = random.choice(action_data["templates"]).format(a=author.mention, t=target.mention)
            if reason_rp:
                text += f"\n\n📝 **Причина:** {reason_rp}"
            await ch.send(embed=discord.Embed(
                description=f"{action_data['emoji']} {text}", color=action_data["color"]
            ))
            return
        if lower == action_key:
            reply_m = await get_reply_member(message)
            if reply_m:
                target = reply_m
                if target == author:
                    await ch.send(embed=embed_error("Нельзя это делать с самим собой!"))
                    return
                text = random.choice(action_data["templates"]).format(a=author.mention, t=target.mention)
                if reason_rp:
                    text += f"\n\n📝 **Причина:** {reason_rp}"
                await ch.send(embed=discord.Embed(
                    description=f"{action_data['emoji']} {text}", color=action_data["color"]
                ))
                return

    if (lower.startswith("брак ") and message.mentions
            and not any(lower.startswith(x) for x in (
                "брак да", "брак нет", "брак цена", "брак продлить", "брак режим", "брак рейтинг"))):
        target = message.mentions[0]
        if target == author:
            return await ch.send(embed=embed_error("Нельзя сделать предложение самому себе."))
        if get_marriage(guild_id, author.id):
            return await ch.send(embed=embed_error("Вы уже в браке. Используйте `!Развод`."))
        if get_marriage(guild_id, target.id):
            return await ch.send(embed=embed_error(f"{target.mention} уже состоит в браке."))
        conn = get_conn()
        c    = conn.cursor()
        c.execute(
            """SELECT * FROM divorce_history WHERE guild_id=?
               AND ((user1_id=? AND user2_id=?) OR (user1_id=? AND user2_id=?))
               ORDER BY divorce_date DESC LIMIT 1""",
            (guild_id, author.id, target.id, target.id, author.id)
        )
        history = c.fetchone()
        c.execute("DELETE FROM proposals WHERE guild_id=? AND from_user=? AND to_user=?",
                  (guild_id, author.id, target.id))
        proposal_type = "restore" if (
            history and datetime.now() - datetime.fromisoformat(history["divorce_date"]) <= timedelta(days=3)
        ) else "new"
        c.execute(
            "INSERT INTO proposals (guild_id, from_user, to_user, created_at, proposal_type) VALUES (?,?,?,?,?)",
            (guild_id, author.id, target.id, datetime.now().isoformat(), proposal_type)
        )
        conn.commit()
        conn.close()
        if proposal_type == "restore":
            e = discord.Embed(
                title="💞 Предложение о восстановлении брака",
                description=f"{author.mention} предлагает {target.mention} восстановить прежний брак!\n\n**Брак да** — принять, **Брак нет** — отказать.",
                color=0xFF69B4
            )
        else:
            e = discord.Embed(
                title="💍 Предложение руки и сердца",
                description=f"{author.mention} делает предложение {target.mention}! 💕\n\n**Брак да** — принять, **Брак нет** — отказать.",
                color=0xFF69B4
            )
        await ch.send(embed=e)
        return

    if lower == "брак да":
        conn = get_conn()
        c    = conn.cursor()
        c.execute("SELECT * FROM proposals WHERE guild_id=? AND to_user=? ORDER BY created_at DESC LIMIT 1",
                  (guild_id, author.id))
        proposal = c.fetchone()
        conn.close()
        if not proposal:
            return await ch.send(embed=embed_error("У вас нет входящих предложений."))
        from_id   = proposal["from_user"]
        prop_type = proposal["proposal_type"]
        if get_marriage(guild_id, author.id) or get_marriage(guild_id, from_id):
            conn = get_conn()
            conn.execute("DELETE FROM proposals WHERE id=?", (proposal["id"],))
            conn.commit(); conn.close()
            return await ch.send(embed=embed_error("Один из участников уже состоит в браке."))
        from_user = message.guild.get_member(from_id)
        mention1  = from_user.mention if from_user else f"<@{from_id}>"
        conn = get_conn()
        c    = conn.cursor()
        if prop_type == "restore":
            c.execute(
                """SELECT * FROM divorce_history WHERE guild_id=?
                   AND ((user1_id=? AND user2_id=?) OR (user1_id=? AND user2_id=?))
                   ORDER BY divorce_date DESC LIMIT 1""",
                (guild_id, from_id, author.id, author.id, from_id)
            )
            history = c.fetchone()
            if history:
                c.execute(
                    "INSERT INTO marriages (guild_id,user1_id,user2_id,start_date,extra_days,in_rating) VALUES (?,?,?,?,?,?)",
                    (guild_id, history["user1_id"], history["user2_id"], history["start_date"], history["extra_days"], 0)
                )
                c.execute("DELETE FROM divorce_history WHERE id=?", (history["id"],))
                title, desc = "💞 Брак восстановлен!", f"🎊 {mention1} и {author.mention} восстановили свой союз!"
            else:
                c.execute(
                    "INSERT INTO marriages (guild_id,user1_id,user2_id,start_date,extra_days,in_rating) VALUES (?,?,?,?,?,?)",
                    (guild_id, from_id, author.id, datetime.now().isoformat(), 0, 0)
                )
                title, desc = "💒 Брак заключён!", f"🎊 {mention1} и {author.mention} теперь женаты!"
        else:
            c.execute(
                "INSERT INTO marriages (guild_id,user1_id,user2_id,start_date,extra_days,in_rating) VALUES (?,?,?,?,?,?)",
                (guild_id, from_id, author.id, datetime.now().isoformat(), 0, 0)
            )
            title, desc = "💒 Поздравляем с браком!", f"🎊 {mention1} и {author.mention} теперь женаты!"
        c.execute("DELETE FROM proposals WHERE id=?", (proposal["id"],))
        conn.commit()
        conn.close()
        await ch.send(embed=discord.Embed(title=title, description=desc, color=0xFF69B4))
        return

    if lower == "брак нет":
        conn = get_conn()
        c    = conn.cursor()
        c.execute("SELECT * FROM proposals WHERE guild_id=? AND to_user=? ORDER BY created_at DESC LIMIT 1",
                  (guild_id, author.id))
        proposal = c.fetchone()
        if not proposal:
            conn.close()
            return await ch.send(embed=embed_error("У вас нет входящих предложений."))
        from_user = message.guild.get_member(proposal["from_user"])
        c.execute("DELETE FROM proposals WHERE id=?", (proposal["id"],))
        conn.commit()
        conn.close()
        await ch.send(embed=discord.Embed(
            description=f"💔 {author.mention} отклонил(а) предложение {from_user.mention if from_user else 'пользователя'}.",
            color=0xAAAAAA
        ))
        return

    if lower == "!развод":
        marriage = get_marriage(guild_id, author.id)
        if not marriage:
            return await ch.send(embed=embed_error("Вы не состоите в браке."))
        partner_id = get_partner_id(marriage, author.id)
        partner    = message.guild.get_member(partner_id)
        await do_divorce(guild_id, marriage)
        await ch.send(embed=discord.Embed(
            title="💔 Развод",
            description=(
                f"{author.mention} и {partner.mention if partner else f'<@{partner_id}>'} расторгли брак.\n"
                "Восстановить союз можно в течение **3 дней**."
            ),
            color=0x888888
        ))
        return

    if lower == "мой брак":
        marriage = get_marriage(guild_id, author.id)
        if not marriage:
            return await ch.send(embed=discord.Embed(description="💔 Вы не состоите в браке.", color=0x888888))
        partner_id = get_partner_id(marriage, author.id)
        partner    = message.guild.get_member(partner_id)
        td         = marriage_duration(marriage)
        e = discord.Embed(title="💑 Ваш брак", color=0xFF69B4)
        e.add_field(name="Партнёр",         value=partner.mention if partner else f"<@{partner_id}>", inline=True)
        e.add_field(name="Срок брака",      value=fmt_duration(td), inline=True)
        e.add_field(name="Дата заключения", value=datetime.fromisoformat(marriage["start_date"]).strftime("%d.%m.%Y %H:%M"), inline=True)
        e.add_field(name="В рейтинге",      value="✅ Да" if marriage["in_rating"] else "❌ Нет", inline=True)
        if partner:
            e.set_thumbnail(url=partner.display_avatar.url)
        await ch.send(embed=e)
        return

    if lower.startswith("твой брак") and message.mentions:
        target   = message.mentions[0]
        marriage = get_marriage(guild_id, target.id)
        if not marriage:
            return await ch.send(embed=discord.Embed(description=f"💔 {target.mention} не состоит в браке.", color=0x888888))
        partner_id = get_partner_id(marriage, target.id)
        partner    = message.guild.get_member(partner_id)
        td         = marriage_duration(marriage)
        e = discord.Embed(title=f"💑 Брак {target.display_name}", color=0xFF69B4)
        e.add_field(name="Партнёр",         value=partner.mention if partner else f"<@{partner_id}>", inline=True)
        e.add_field(name="Срок брака",      value=fmt_duration(td), inline=True)
        e.add_field(name="Дата заключения", value=datetime.fromisoformat(marriage["start_date"]).strftime("%d.%m.%Y %H:%M"), inline=True)
        e.add_field(name="В рейтинге",      value="✅ Да" if marriage["in_rating"] else "❌ Нет", inline=True)
        e.set_thumbnail(url=target.display_avatar.url)
        await ch.send(embed=e)
        return

    if lower == "браки" or (lower.startswith("браки ") and lower[6:].strip().isdigit()):
        page = int(lower[6:].strip()) if lower.startswith("браки ") and lower[6:].strip().isdigit() else 1
        conn = get_conn()
        c    = conn.cursor()
        c.execute("SELECT * FROM marriages WHERE guild_id=? ORDER BY start_date ASC", (guild_id,))
        all_m = c.fetchall()
        conn.close()
        if not all_m:
            return await ch.send(embed=discord.Embed(description="💔 Браков нет.", color=0x888888))
        per_page    = 10
        total_pages = max(1, math.ceil(len(all_m) / per_page))
        page        = max(1, min(page, total_pages))
        lines_m = []
        for i, m in enumerate(all_m[(page - 1) * per_page : page * per_page], start=(page - 1) * per_page + 1):
            u1 = message.guild.get_member(m["user1_id"])
            u2 = message.guild.get_member(m["user2_id"])
            n1 = u1.display_name if u1 else f"ID:{m['user1_id']}"
            n2 = u2.display_name if u2 else f"ID:{m['user2_id']}"
            lines_m.append(f"`{i:>2}.` {n1} 💍 {n2} — {fmt_duration(marriage_duration(m))}")
        e = discord.Embed(title=f"💑 Браки сервера — стр. {page}/{total_pages}", description="\n".join(lines_m), color=0xFF69B4)
        e.set_footer(text=f"Всего браков: {len(all_m)}")
        await ch.send(embed=e)
        return

    if lower.startswith("поженить пару") and len(message.mentions) >= 2:
        if my_rank < 3:
            return await ch.send(embed=embed_error("Требуется ранг **[3] Младший администратор** или выше."))
        u1, u2 = message.mentions[0], message.mentions[1]
        if u1 == u2:
            return await ch.send(embed=embed_error("Нельзя поженить пользователя с самим собой."))
        if get_marriage(guild_id, u1.id):
            return await ch.send(embed=embed_error(f"{u1.mention} уже состоит в браке."))
        if get_marriage(guild_id, u2.id):
            return await ch.send(embed=embed_error(f"{u2.mention} уже состоит в браке."))
        conn = get_conn()
        conn.execute("INSERT INTO marriages (guild_id,user1_id,user2_id,start_date,extra_days,in_rating) VALUES (?,?,?,?,?,?)",
                     (guild_id, u1.id, u2.id, datetime.now().isoformat(), 0, 0))
        conn.commit(); conn.close()
        await ch.send(embed=discord.Embed(
            title="💒 Брак зарегистрирован!",
            description=f"🎊 {u1.mention} и {u2.mention} теперь состоят в браке!",
            color=0xFF69B4
        ))
        return

    if lower.startswith("развести пару") and len(message.mentions) >= 2:
        if my_rank < 3:
            return await ch.send(embed=embed_error("Требуется ранг **[3] Младший администратор** или выше."))
        u1, u2 = message.mentions[0], message.mentions[1]
        conn   = get_conn()
        c      = conn.cursor()
        c.execute(
            "SELECT * FROM marriages WHERE guild_id=? AND ((user1_id=? AND user2_id=?) OR (user1_id=? AND user2_id=?))",
            (guild_id, u1.id, u2.id, u2.id, u1.id)
        )
        marriage = c.fetchone()
        conn.close()
        if not marriage:
            return await ch.send(embed=embed_error(f"{u1.mention} и {u2.mention} не состоят в браке друг с другом."))
        await do_divorce(guild_id, marriage)
        await ch.send(embed=discord.Embed(
            title="💔 Брак расторгнут",
            description=f"{u1.mention} и {u2.mention} были принудительно разведены.",
            color=0x888888
        ))
        return

    if lower == "!сброс браков":
        if my_rank < 4:
            return await ch.send(embed=embed_error("Требуется ранг **[4] Старший администратор** или выше."))
        conn = get_conn()
        c    = conn.cursor()
        c.execute("DELETE FROM marriages       WHERE guild_id=?", (guild_id,))
        c.execute("DELETE FROM divorce_history WHERE guild_id=?", (guild_id,))
        c.execute("DELETE FROM proposals       WHERE guild_id=?", (guild_id,))
        conn.commit(); conn.close()
        await ch.send(embed=discord.Embed(
            title="🔄 Все браки сброшены",
            description="Список браков и история разводов обнулены.",
            color=0xFF4444
        ))
        return

    if lower == "развести вышедших":
        if my_rank < 3:
            return await ch.send(embed=embed_error("Требуется ранг **[3] Младший администратор** или выше."))
        conn = get_conn()
        c    = conn.cursor()
        c.execute("SELECT * FROM marriages WHERE guild_id=?", (guild_id,))
        all_m    = c.fetchall()
        conn.close()
        divorced = 0
        for m in all_m:
            u1 = message.guild.get_member(m["user1_id"])
            u2 = message.guild.get_member(m["user2_id"])
            if not u1 or not u2:
                await do_divorce(guild_id, m)
                divorced += 1
        await ch.send(embed=discord.Embed(
            title="💔 Готово",
            description=f"Расторгнуто браков с вышедшими участниками: **{divorced}**",
            color=0x888888
        ))
        return

    extend_days = None
    if lower.startswith("брак продлить "):
        parts = lower.split()
        if len(parts) >= 3 and parts[2].isdigit():
            extend_days = int(parts[2])
    elif lower.startswith("продлить брак "):
        parts = lower.split()
        if len(parts) >= 3 and parts[2].isdigit():
            extend_days = int(parts[2])
    if extend_days is not None:
        marriage = get_marriage(guild_id, author.id)
        if not marriage:
            return await ch.send(embed=embed_error("Вы не состоите в браке."))
        if extend_days <= 0:
            return await ch.send(embed=embed_error("Укажите положительное количество дней."))
        conn = get_conn()
        conn.execute("UPDATE marriages SET extra_days=extra_days+? WHERE id=?", (extend_days, marriage["id"]))
        conn.commit(); conn.close()
        await ch.send(embed=embed_ok(f"Брак продлён на **{extend_days} дн.** 🎉"))
        return

    if lower == "топ браков" or (lower.startswith("топ браков ") and lower[11:].strip().isdigit()):
        page = int(lower[11:].strip()) if lower.startswith("топ браков ") and lower[11:].strip().isdigit() else 1
        conn = get_conn()
        c    = conn.cursor()
        c.execute("SELECT * FROM marriages WHERE guild_id=? AND in_rating=1", (guild_id,))
        rated = c.fetchall()
        conn.close()
        if not rated:
            return await ch.send(embed=discord.Embed(description="🏆 В рейтинге нет пар.", color=0x888888))
        sorted_m    = sorted(rated, key=marriage_duration, reverse=True)
        per_page    = 10
        total_pages = max(1, math.ceil(len(sorted_m) / per_page))
        page        = max(1, min(page, total_pages))
        MEDALS      = {1: "🥇", 2: "🥈", 3: "🥉"}
        lines_t = []
        for i, m in enumerate(sorted_m[(page - 1) * per_page : page * per_page], start=(page - 1) * per_page + 1):
            u1    = message.guild.get_member(m["user1_id"])
            u2    = message.guild.get_member(m["user2_id"])
            n1    = u1.display_name if u1 else f"ID:{m['user1_id']}"
            n2    = u2.display_name if u2 else f"ID:{m['user2_id']}"
            medal = MEDALS.get(i, f"`{i:>2}.`")
            lines_t.append(f"{medal} **{n1}** 💍 **{n2}** — {fmt_duration(marriage_duration(m))}")
        e = discord.Embed(title=f"🏆 Топ браков — стр. {page}/{total_pages}", description="\n".join(lines_t), color=0xFFD700)
        await ch.send(embed=e)
        return

    if lower == "+брак рейтинг":
        marriage = get_marriage(guild_id, author.id)
        if not marriage:
            return await ch.send(embed=embed_error("Вы не состоите в браке."))
        if marriage["in_rating"]:
            return await ch.send(embed=embed_error("Ваша пара уже в рейтинге."))
        conn = get_conn()
        conn.execute("UPDATE marriages SET in_rating=1 WHERE id=?", (marriage["id"],))
        conn.commit(); conn.close()
        await ch.send(embed=embed_ok("Ваша пара добавлена в топ браков! 🏆"))
        return

    if lower == "-брак рейтинг":
        marriage = get_marriage(guild_id, author.id)
        if not marriage:
            return await ch.send(embed=embed_error("Вы не состоите в браке."))
        if not marriage["in_rating"]:
            return await ch.send(embed=embed_error("Ваша пара не в рейтинге."))
        conn = get_conn()
        conn.execute("UPDATE marriages SET in_rating=0 WHERE id=?", (marriage["id"],))
        conn.commit(); conn.close()
        await ch.send(embed=embed_ok("Ваша пара исключена из топа браков."))
        return


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN") or BOT_TOKEN
    bot.run(token)
    print('huy')
    if packet_data and receive_data:
        print('connected to huy')
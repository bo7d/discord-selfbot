import os, json, asyncio, random, time, math, hashlib, base64, re, string, datetime
import discord
from discord.ext import commands, tasks
import aiohttp
from urllib.parse import quote

CONFIG='config.json'
def loadcfg():
    if not os.path.exists(CONFIG):
        json.dump({'token':'','prefix':'!','owner_id':0,'auto_skull':False,'presence':['cutting patterns','absolute ollie built by olivia']}, open(CONFIG,'w'), indent=2)
    try:
        with open(CONFIG,encoding='utf-8') as f: d=json.load(f)
        if isinstance(d,dict): return d
    except Exception: pass
    return {'token':'','prefix':'!','owner_id':0,'auto_skull':False,'presence':['cutting patterns','absolute ollie built by olivia']}
C=loadcfg()
TOKEN='PUT YOUR TOKEN HERE'
if not (C.get('token') or '').strip(): C['token']=TOKEN
bot=commands.Bot(command_prefix=C.get('prefix','!'), self_bot=True)
bot.remove_command('help')

SNIPE={}; EDITSNIPE={}; LOGCH={'id':None}
SKULL={'on': bool(C.get('auto_skull',False))}
AFK={'on':False,'msg':'away from desk'}
AUTOBURN={'on':False}
BURN_CD={}
INSULTS=['you are the human equivalent of a participation trophy','your existence is a 404 error','im not mad, im just disappointed and also mad','you bring down the average IQ of any room you enter','if brain cells were a currency you would be bankrupt','even my code runs better than your life','you are the error message nobody asked for','your wifi password is probably the only password you remember']

async def put(ctx, text):
    text=str(text)[:1980]
    try: await ctx.message.edit(content=text)
    except Exception:
        try: await ctx.send(text)
        except Exception: pass

def up(s): return s.upper()
def low(s): return s.lower()
def tit(s): return s.title()
def rev(s): return s[::-1]
def mock(s): return ''.join(c.upper() if i%2 else c.lower() for i,c in enumerate(s))
def leet(s): return s.translate(str.maketrans('aeios','43105'))
def binf(s): return ' '.join(format(ord(c),'08b') for c in s)
def hexf(s): return s.encode().hex()
def b64f(s):
    import base64; return base64.b64encode(s.encode()).decode()
def unb64f(s):
    import base64; return base64.b64decode(s.encode()).decode(errors='ignore')
def rotf(s):
    import codecs; return codecs.decode(s,'rot_13')
def zalgo(s): return s+''.join(chr(0x0300+i%60) for i in range(6))
def wide(s): return ' '.join(list(s))
def pig(s):
    out=[]
    for w in s.split():
        out.append((w[1:]+w[0]+'ay') if w.isalpha() else w)
    return ' '.join(out)

@bot.command(name='upper')
async def xupper(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, up(_))

@bot.command(name='lower')
async def xlower(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, low(_))

@bot.command(name='title')
async def xtitle(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, tit(_))

@bot.command(name='rev')
async def xrev(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, rev(_))

@bot.command(name='mock')
async def xmock(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, mock(_))

@bot.command(name='leet')
async def xleet(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, leet(_))

@bot.command(name='binary')
async def xbinary(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, binf(_))

@bot.command(name='hex')
async def xhex(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, hexf(_))

@bot.command(name='b64')
async def xb64(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, b64f(_))

@bot.command(name='unb64')
async def xunb64(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, unb64f(_))

@bot.command(name='rot13')
async def xrot13(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, rotf(_))

@bot.command(name='zalgo')
async def xzalgo(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, zalgo(_))

@bot.command(name='wide')
async def xwide(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, wide(_))

@bot.command(name='piglatin')
async def xpiglatin(ctx):
    _a = ctx.message.content.split(maxsplit=1)
    _ = _a[1] if len(_a)>1 else ''
    await put(ctx, pig(_))

@bot.command(name='ping')
async def xping(ctx):
    await put(ctx, f'pong :: {round(bot.latency*1000)}ms')

@bot.command(name='latency')
async def xlatency(ctx):
    await put(ctx, f'latency :: {round(bot.latency*1000)}ms')

@bot.command(name='uptime')
async def xuptime(ctx):
    await put(ctx, 'bench live')

@bot.command(name='prefix')
async def xprefix(ctx):
    await put(ctx, f'prefix :: {C.get("prefix","!")}')

@bot.command(name='cmds')
async def xcmds(ctx):
    await put(ctx, f'commands loaded :: {len(bot.commands)}')

@bot.command(name='help')
async def xhelp(ctx, cat=None):
    cats = {
        'util': 'ping uptime cmds calc uuid b64 rot13 len hash timestamp',
        'text': 'upper lower title rev mock leet binary hex b64 unb64 rot13 zalgo wide piglatin',
        'mod': 'ban kick timeout purge nuke lock slowmode topic rename clone addrole removerole',
        'info': 'uinfo sv members roles channels boosters emojis stickers serverinfo channelinfo roleinfo',
        'media': 'joke cat dog meme ai imagine draw waifu neko',
        'fun': 'roll coin 8ball choose lenny shrug tableflip unflip kaomoji compliment roast',
        'osint': 'ip domain username email phone discordid leaksearch roblox namesearch osint',
    }
    if cat is None:
        await put(ctx, '```txt\nhelp <cat>: util text mod info media fun osint\n```')
    else:
        key = str(cat).lower()
        if key in cats:
            await put(ctx, '```txt\n' + cats[key] + '\n```')
        else:
            await put(ctx, '```txt\nunknown category\n```')

@bot.command(name='calc')
async def xcalc(ctx, expr):
    try:
        await put(ctx, eval(expr, {"__builtins__":{}}, {"math":math}))
    except Exception as e:
        await put(ctx, f"calc err :: {e}")

@bot.command(name='uuid')
async def xuuid(ctx):
    import uuid as _u; await put(ctx, str(_u.uuid4()))

@bot.command(name='hash')
async def xhash(ctx, text):
    await put(ctx, hashlib.sha256(text.encode()).hexdigest())

@bot.command(name='md5')
async def xmd5(ctx, text):
    await put(ctx, hashlib.md5(text.encode()).hexdigest())

@bot.command(name='sha1')
async def xsha1(ctx, text):
    await put(ctx, hashlib.sha1(text.encode()).hexdigest())

@bot.command(name='len')
async def xlen(ctx, text):
    await put(ctx, len(text))

@bot.command(name='count')
async def xcount(ctx, text):
    await put(ctx, len(text.split()))

@bot.command(name='choose')
async def xchoose(ctx, *, opts):
    await put(ctx, random.choice([o.strip() for o in opts.split(",") if o.strip()]))

@bot.command(name='roll')
async def xroll(ctx, sides:int=6):
    await put(ctx, f"🎲 {random.randint(1, max(2,sides))}")

@bot.command(name='coin')
async def xcoin(ctx):
    await put(ctx, random.choice(["heads","tails"]))

@bot.command(name='8ball')
async def x8ball(ctx):
    await put(ctx, random.choice(["yes","no","maybe","absolutely","never","ask again","signs point to yes"]))

@bot.command(name='rps')
async def xrps(ctx):
    await put(ctx, random.choice(["rock","paper","scissors"]))

@bot.command(name='timestamp')
async def xtimestamp(ctx):
    await put(ctx, int(time.time()))

@bot.command(name='random')
async def xrandom(ctx, a:int, b:int):
    await put(ctx, random.randint(a,b))

@bot.command(name='chip0')
async def xchip0(ctx):
    await put(ctx, 'chip 0 :: iron on')

@bot.command(name='chip1')
async def xchip1(ctx):
    await put(ctx, 'chip 1 :: iron on')

@bot.command(name='chip2')
async def xchip2(ctx):
    await put(ctx, 'chip 2 :: iron on')

@bot.command(name='chip3')
async def xchip3(ctx):
    await put(ctx, 'chip 3 :: iron on')

@bot.command(name='chip4')
async def xchip4(ctx):
    await put(ctx, 'chip 4 :: iron on')

@bot.command(name='chip5')
async def xchip5(ctx):
    await put(ctx, 'chip 5 :: iron on')

@bot.command(name='uinfo')
async def xuinfo(ctx):
    m = ctx.message.mentions[0] if ctx.message.mentions else ctx.author
    await put(ctx, f"{m} :: id={m.id} :: created={m.created_at} :: joined={getattr(m,'joined_at','n/a')} :: roles={len(getattr(m,'roles',[]))}")

@bot.command(name='avatar')
async def xavatar(ctx):
    m = ctx.message.mentions[0] if ctx.message.mentions else ctx.author
    await put(ctx, m.display_avatar.url)

@bot.command(name='banner')
async def xbanner(ctx):
    u = await bot.fetch_user(ctx.author.id)
    await put(ctx, (u.banner.url if u.banner else "no banner"))

@bot.command(name='ids')
async def xids(ctx):
    m = ctx.message.mentions[0] if ctx.message.mentions else None
    if m: await put(ctx, m.id)
    elif ctx.message.channel_mentions: await put(ctx, ctx.message.channel_mentions[0].id)
    else: await put(ctx, "nothing mentioned")

@bot.command(name='sv')
async def xsv(ctx):
    out = [f"{g.name} [{g.id}]" for g in bot.guilds]
    await put(ctx, "\n".join(out)[:1980] or "no guilds")

@bot.command(name='members')
async def xmembers(ctx):
    await put(ctx, f"members :: {ctx.guild.member_count if ctx.guild else 'n/a'}")

@bot.command(name='roles')
async def xroles(ctx):
    await put(ctx, "\n".join(f"{r.name} [{r.id}]" for r in (ctx.guild.roles if ctx.guild else []))[:1980] or "no guild")

@bot.command(name='channels')
async def xchannels(ctx):
    await put(ctx, "\n".join(f"#{c.name} [{c.id}]" for c in (ctx.guild.channels if ctx.guild else []))[:1980] or "no guild")

@bot.command(name='boosts')
async def xboosts(ctx):
    await put(ctx, f"boosts :: {ctx.guild.premium_subscription_count if ctx.guild else 0}")

@bot.command(name='emojis')
async def xemojis(ctx):
    await put(ctx, " ".join(str(e) for e in (ctx.guild.emojis if ctx.guild else []))[:1980] or "none")

@bot.command(name='stickers')
async def xstickers(ctx):
    await put(ctx, " | ".join(s.name for s in (ctx.guild.stickers if ctx.guild else [])) or "none")

@bot.command(name='channelinfo')
async def xchannelinfo(ctx):
    c = ctx.channel
    await put(ctx, f"{c} :: id={c.id} :: type={c.type} :: nsfw={getattr(c,'nsfw',False)} :: slowmode={getattr(c,'slowmode_delay',0)}")

@bot.command(name='serverinfo')
async def xserverinfo(ctx):
    g = ctx.guild
    if not g: 
        await put(ctx, "no guild context")
    else:
        await put(ctx, f"{g.name} :: members={g.member_count} :: boosts={g.premium_subscription_count} :: owner={g.owner_id} :: created={g.created_at} :: channels={len(g.channels)}")

@bot.command(name='roleinfo')
async def xroleinfo(ctx, name):
    if not ctx.guild: await put(ctx, "no guild context")
    else:
        r = discord.utils.get(ctx.guild.roles, name=name)
        await put(ctx, f"{r} :: id={r.id} :: color={r.color} :: hoist={r.hoist} :: mentionable={r.mentionable}" if r else "role not found")

@bot.command(name='firstmsg')
async def xfirstmsg(ctx):
    async for m in ctx.channel.history(limit=1, oldest_first=True):
        await put(ctx, f"{m.author}: {m.content} ({m.created_at})")

@bot.command(name='snowflake')
async def xsnowflake(ctx, sid:int):
    await put(ctx, f"created :: {discord.utils.snowflake_time(sid)}")

@bot.command(name='mutuals')
async def xmutuals(ctx):
    await put(ctx, f"mutual guilds :: {len(bot.guilds)}")

@bot.command(name='myinfo')
async def xmyinfo(ctx):
    await put(ctx, f"{bot.user} :: id={bot.user.id} :: created={bot.user.created_at}")

@bot.command(name='playing')
async def xplaying(ctx, *, text):
    await bot.change_presence(activity=discord.Game(name=text)); await put(ctx, f"playing :: {text}")

@bot.command(name='listening')
async def xlistening(ctx, *, text):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text)); await put(ctx, f"listening :: {text}")

@bot.command(name='watching')
async def xwatching(ctx, *, text):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text)); await put(ctx, f"watching :: {text}")

@bot.command(name='streaming')
async def xstreaming(ctx, *, text):
    await bot.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/olivia")); await put(ctx, f"streaming :: {text}")

@bot.command(name='competing')
async def xcompeting(ctx, *, text):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=text)); await put(ctx, f"competing :: {text}")

@bot.command(name='custom')
async def xcustom(ctx, *, text):
    await bot.change_presence(activity=discord.CustomActivity(name=text)); await put(ctx, f"custom :: {text}")

@bot.command(name='dnd')
async def xdnd(ctx):
    await bot.change_presence(status=discord.Status.dnd); await put(ctx, "status :: dnd")

@bot.command(name='idle')
async def xidle(ctx):
    await bot.change_presence(status=discord.Status.idle); await put(ctx, "status :: idle")

@bot.command(name='online')
async def xonline(ctx):
    await bot.change_presence(status=discord.Status.online); await put(ctx, "status :: online")

@bot.command(name='invisible')
async def xinvisible(ctx):
    await bot.change_presence(status=discord.Status.invisible); await put(ctx, "status :: invisible")

@bot.command(name='clearpresence')
async def xclearpresence(ctx):
    await bot.change_presence(activity=None); await put(ctx, "presence cleared")

@bot.command(name='setprefix')
async def xsetprefix(ctx, *, new):
    C["prefix"]=new; await put(ctx, f"prefix :: {new} (session)")

@bot.command(name='skullon')
async def xskullon(ctx):
    SKULL["on"]=True; await put(ctx, "skull react :: on")

@bot.command(name='skulloff')
async def xskulloff(ctx):
    SKULL["on"]=False; await put(ctx, "skull react :: off")

@bot.command(name='skulltoggle')
async def xskulltoggle(ctx):
    SKULL["on"]=not SKULL["on"]; await put(ctx, f"skull react :: {'on' if SKULL['on'] else 'off'}")

@bot.command(name='skullstatus')
async def xskullstatus(ctx):
    await put(ctx, f"skull react :: {'on' if SKULL['on'] else 'off'}")

@bot.command(name='afk')
async def xafk(ctx, *, reason='away from desk'):
    AFK["on"]=True; AFK["msg"]=reason; await put(ctx, f"afk :: {reason}")

@bot.command(name='unafk')
async def xunafk(ctx):
    AFK["on"]=False; await put(ctx, "back on the rail")

@bot.command(name='nick')
async def xnick(ctx, *, name):
    if ctx.guild: await ctx.author.edit(nick=name); await put(ctx, f"nick :: {name}")

@bot.command(name='joinvc')
async def xjoinvc(ctx, *, name=None):
    if not ctx.guild: await put(ctx, "no guild context"); return
    vcs=ctx.guild.voice_channels
    if not vcs: await put(ctx, "no voice channel"); return
    target = next((c for c in vcs if name and name.lower() in c.name.lower()), vcs[0])
    await target.connect(self_deaf=True, self_mute=True)
    await put(ctx, f"joined :: {target.name}")

@bot.command(name='leavevc')
async def xleavevc(ctx):
    if ctx.guild and ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect(); await put(ctx, "left vc")
    else: await put(ctx, "not in vc")

@bot.command(name='vmute')
async def xvmute(ctx):
    if ctx.guild and ctx.guild.voice_client: await ctx.guild.voice_client.edit_self_mute(True); await put(ctx, "self muted")
    else: await put(ctx, "not in vc")

@bot.command(name='vunmute')
async def xvunmute(ctx):
    if ctx.guild and ctx.guild.voice_client: await ctx.guild.voice_client.edit_self_mute(False); await put(ctx, "unmuted")
    else: await put(ctx, "not in vc")

@bot.command(name='vdeafen')
async def xvdeafen(ctx):
    if ctx.guild and ctx.guild.voice_client: await ctx.guild.voice_client.edit_self_deaf(True); await put(ctx, "deafened")
    else: await put(ctx, "not in vc")

@bot.command(name='vundeafen')
async def xvundeafen(ctx):
    if ctx.guild and ctx.guild.voice_client: await ctx.guild.voice_client.edit_self_deaf(False); await put(ctx, "undeafened")
    else: await put(ctx, "not in vc")

@bot.command(name='ban')
async def xban(ctx, member, *, reason='banned', days:int=0):
    try:
        await member.ban(reason=reason, delete_message_days=min(7,max(0,days)))
        await put(ctx, f"banned :: {member}")
    except Exception as e: await put(ctx, f"ban err :: {e}")

@bot.command(name='unban')
async def xunban(ctx, user_id:int, *, reason='unbanned'):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await put(ctx, f"unbanned :: {user}")
    except Exception as e: await put(ctx, f"unban err :: {e}")

@bot.command(name='kick')
async def xkick(ctx, member, *, reason='kicked'):
    try:
        await member.kick(reason=reason); await put(ctx, f"kicked :: {member}")
    except Exception as e: await put(ctx, f"kick err :: {e}")

@bot.command(name='timeout')
async def xtimeout(ctx, member, minutes:int=10, *, reason='timed out'):
    try:
        import datetime
        await member.timeout(datetime.timedelta(minutes=min(40320,max(1,minutes))), reason=reason)
        await put(ctx, f"timed out :: {member} :: {minutes}m")
    except Exception as e: await put(ctx, f"timeout err :: {e}")

@bot.command(name='untimeout')
async def xuntimeout(ctx, member):
    try:
        await member.timeout(None); await put(ctx, f"untimeout :: {member}")
    except Exception as e: await put(ctx, f"untimeout err :: {e}")

@bot.command(name='purge')
async def xpurge(ctx, n:int=20):
    msgs=[m async for m in ctx.channel.history(limit=max(1,min(n,200)), before=ctx.message) if m.author==bot.user]
    for m in msgs:
        try: await m.delete(); await asyncio.sleep(0.15)
        except Exception: pass
    try: await ctx.message.delete()
    except Exception: pass
    await put(ctx, f"purged :: {len(msgs)}")

@bot.command(name='purgeuser')
async def xpurgeuser(ctx, member, n:int=50):
    msgs=[m async for m in ctx.channel.history(limit=max(1,min(n,200)), before=ctx.message) if m.author==member]
    for m in msgs:
        try: await m.delete(); await asyncio.sleep(0.15)
        except Exception: pass
    await put(ctx, f"purged user :: {member} :: {len(msgs)}")

@bot.command(name='purgecontains')
async def xpurgecontains(ctx, word:str, n:int=100):
    msgs=[m async for m in ctx.channel.history(limit=max(1,min(n,200)), before=ctx.message) if word.lower() in (m.content or "").lower()]
    for m in msgs:
        try: await m.delete(); await asyncio.sleep(0.15)
        except Exception: pass
    await put(ctx, f"purged contains :: {word} :: {len(msgs)}")

@bot.command(name='nuke')
async def xnuke(ctx):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        ch = await ctx.channel.clone(reason="selfbot nuke")
        await ctx.channel.delete()
        await ch.send("nuked :: absolute ollie")
    except Exception as e: await put(ctx, f"nuke err :: {e}")

@bot.command(name='lock')
async def xlock(ctx):
    if not ctx.channel.permissions_for(ctx.guild.me).manage_channels: await put(ctx, "no perm"); return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await put(ctx, "channel locked")

@bot.command(name='unlock')
async def xunlock(ctx):
    if not ctx.channel.permissions_for(ctx.guild.me).manage_channels: await put(ctx, "no perm"); return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await put(ctx, "channel unlocked")

@bot.command(name='slowmode')
async def xslowmode(ctx, sec:int=0):
    try:
        await ctx.channel.edit(slowmode_delay=max(0,min(21600,sec)))
        await put(ctx, f"slowmode :: {sec}s")
    except Exception as e: await put(ctx, f"slowmode err :: {e}")

@bot.command(name='topic')
async def xtopic(ctx, *, text):
    try:
        await ctx.channel.edit(topic=text); await put(ctx, f"topic :: {text}")
    except Exception as e: await put(ctx, f"topic err :: {e}")

@bot.command(name='rename')
async def xrename(ctx, *, name):
    try:
        await ctx.channel.edit(name=name); await put(ctx, f"renamed :: {name}")
    except Exception as e: await put(ctx, f"rename err :: {e}")

@bot.command(name='clone')
async def xclone(ctx):
    try:
        ch = await ctx.channel.clone()
        await put(ctx, f"cloned :: {ch.name}")
    except Exception as e: await put(ctx, f"clone err :: {e}")

@bot.command(name='addrole')
async def xaddrole(ctx, member, *, role):
    if not ctx.guild: await put(ctx, "no guild context"); return
    r = discord.utils.get(ctx.guild.roles, name=role)
    if not r: await put(ctx, "role not found"); return
    try:
        await member.add_roles(r); await put(ctx, f"added {r.name} to {member}")
    except Exception as e: await put(ctx, f"addrole err :: {e}")

@bot.command(name='removerole')
async def xremoverole(ctx, member, *, role):
    if not ctx.guild: await put(ctx, "no guild context"); return
    r = discord.utils.get(ctx.guild.roles, name=role)
    if not r: await put(ctx, "role not found"); return
    try:
        await member.remove_roles(r); await put(ctx, f"removed {r.name} from {member}")
    except Exception as e: await put(ctx, f"removerole err :: {e}")

@bot.command(name='createchannel')
async def xcreatechannel(ctx, *, name):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        ch = await ctx.guild.create_text_channel(name)
        await put(ctx, f"created :: {ch.name}")
    except Exception as e: await put(ctx, f"createchannel err :: {e}")

@bot.command(name='createvoice')
async def xcreatevoice(ctx, *, name):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        ch = await ctx.guild.create_voice_channel(name)
        await put(ctx, f"created :: {ch.name}")
    except Exception as e: await put(ctx, f"createvoice err :: {e}")

@bot.command(name='createcategory')
async def xcreatecategory(ctx, *, name):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        c = await ctx.guild.create_category(name)
        await put(ctx, f"created :: {c.name}")
    except Exception as e: await put(ctx, f"createcategory err :: {e}")

@bot.command(name='deletechannel')
async def xdeletechannel(ctx, *, name=None):
    if not ctx.guild: await put(ctx, "no guild context"); return
    ch = ctx.channel if name is None else discord.utils.get(ctx.guild.channels, name=name)
    if not ch: await put(ctx, "channel not found"); return
    try:
        await ch.delete(); await put(ctx, f"deleted :: {ch.name}")
    except Exception as e: await put(ctx, f"deletechannel err :: {e}")

@bot.command(name='servernick')
async def xservernick(ctx, *, name):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        await ctx.guild.me.edit(nick=name); await put(ctx, f"server nick :: {name}")
    except Exception as e: await put(ctx, f"servernick err :: {e}")

@bot.command(name='servericon')
async def xservericon(ctx, *, url):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        import aiohttp
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                await ctx.guild.edit(icon=await r.read())
        await put(ctx, "server icon updated")
    except Exception as e: await put(ctx, f"servericon err :: {e}")

@bot.command(name='servername')
async def xservername(ctx, *, name):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        await ctx.guild.edit(name=name); await put(ctx, f"server name :: {name}")
    except Exception as e: await put(ctx, f"servername err :: {e}")

@bot.command(name='createhook')
async def xcreatehook(ctx, *, name='ollie-hook'):
    try:
        w = await ctx.channel.create_webhook(name=name)
        await put(ctx, f"webhook :: {w.url}")
    except Exception as e: await put(ctx, f"createhook err :: {e}")

@bot.command(name='deletehooks')
async def xdeletehooks(ctx):
    try:
        hooks = await ctx.channel.webhooks()
        for h in hooks: await h.delete()
        await put(ctx, f"deleted :: {len(hooks)} hooks")
    except Exception as e: await put(ctx, f"deletehooks err :: {e}")

@bot.command(name='sendhook')
async def xsendhook(ctx, url, *, text):
    try:
        w = discord.Webhook.from_url(url, session=None)
        import aiohttp
        async with aiohttp.ClientSession() as s:
            w = discord.Webhook.from_url(url, session=s)
            await w.send(text)
        await put(ctx, "hook sent")
    except Exception as e: await put(ctx, f"sendhook err :: {e}")

@bot.command(name='snipe')
async def xsnipe(ctx):
    data = SNIPE.get(ctx.channel.id)
    await put(ctx, (f"{data['author']}: {data['content']}" if data else "nothing sniped"))

@bot.command(name='editsnipe')
async def xeditsnipe(ctx):
    data = EDITSNIPE.get(ctx.channel.id)
    await put(ctx, (f"before: {data['before']}\nafter: {data['after']}" if data else "nothing sniped"))

@bot.command(name='logchannel')
async def xlogchannel(ctx, cid:int):
    LOGCH["id"]=cid; await put(ctx, f"log channel :: {cid}")

@bot.command(name='logstatus')
async def xlogstatus(ctx):
    await put(ctx, f"log channel :: {LOGCH['id']}")

@bot.command(name='snipelist')
async def xsnipelist(ctx):
    await put(ctx, f"sniped channels :: {len(SNIPE)}")

@bot.command(name='hypebravery')
async def xhypebravery(ctx):
    try:
        from discord.http import Route
        await bot.http.request(Route("PATCH","/users/@me"), json={"premium_type":None})
        await put(ctx, "hypesquad request sent (best effort)")
    except Exception as e: await put(ctx, f"hype err :: {e}")

@bot.command(name='hypebrilliance')
async def xhypebrilliance(ctx):
    try:
        from discord.http import Route
        await bot.http.request(Route("PATCH","/users/@me"), json={"premium_type":None})
        await put(ctx, "hypesquad request sent (best effort)")
    except Exception as e: await put(ctx, f"hype err :: {e}")

@bot.command(name='hypebalance')
async def xhypebalance(ctx):
    try:
        from discord.http import Route
        await bot.http.request(Route("PATCH","/users/@me"), json={"premium_type":None})
        await put(ctx, "hypesquad request sent (best effort)")
    except Exception as e: await put(ctx, f"hype err :: {e}")

@bot.command(name='spam')
async def xspam(ctx, n:int=5, *, text='gng'):
    for _ in range(max(1,min(20,n))):
        await ctx.send(text); await asyncio.sleep(0.35)
    try: await ctx.message.delete()
    except Exception: pass

@bot.command(name='flood')
async def xflood(ctx, n:int=10, *, text='💀'):
    for _ in range(max(1,min(50,n))):
        await ctx.send(text); await asyncio.sleep(0.2)
    try: await ctx.message.delete()
    except Exception: pass

@bot.command(name='ghostping')
async def xghostping(ctx, *, user):
    m = await ctx.send(user); await asyncio.sleep(0.2); await m.delete()

@bot.command(name='everyone')
async def xeveryone(ctx):
    await put(ctx, "@everyone (text only, not real mention)")

@bot.command(name='here')
async def xhere(ctx):
    await put(ctx, "@here (text only, not real mention)")

@bot.command(name='lenny')
async def xlenny(ctx):
    await put(ctx, "( ͡° ͜ʖ ͡°)")

@bot.command(name='shrug')
async def xshrug(ctx):
    await put(ctx, "¯\\_(ツ)_/¯")

@bot.command(name='tableflip')
async def xtableflip(ctx):
    await put(ctx, "(╯°□°）╯︵ ┻━┻")

@bot.command(name='unflip')
async def xunflip(ctx):
    await put(ctx, "┬─┬ ノ( ゜-゜ノ)")

@bot.command(name='kaomoji')
async def xkaomoji(ctx):
    await put(ctx, random.choice(["( implying )","( ¬‿¬ )","( ͡~ ͜ʖ ͡°)","( ͡ ° ͜ʖ ͡ °)","( ¬_¬ )"]))

@bot.command(name='joke')
async def xjoke(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://official-joke-api.appspot.com/random_joke") as r:
            if r.status==200:
                j=await r.json(); await put(ctx, f"{j['setup']} — {j['punchline']}")
            else: await put(ctx, "joke err")

@bot.command(name='fact')
async def xfact(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://uselessfacts.jsph.pl/random.json?language=en") as r:
            if r.status==200:
                j=await r.json(); await put(ctx, j.get("text","no fact"))
            else: await put(ctx, "fact err")

@bot.command(name='cat')
async def xcat(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://api.thecatapi.com/v1/images/search") as r:
            j=await r.json(); await put(ctx, j[0]["url"] if j else "no cat")

@bot.command(name='dog')
async def xdog(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://dog.ceo/api/breeds/image/random") as r:
            j=await r.json(); await put(ctx, j.get("message","no dog"))

@bot.command(name='fox')
async def xfox(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://randomfox.ca/flofox/") as r:
            try:
                j=await r.json(); await put(ctx, j.get("image", j.get("link","no fox")))
            except Exception: await put(ctx, "fox err")

@bot.command(name='meme')
async def xmeme(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://meme-api.com/gimme") as r:
            j=await r.json(); await put(ctx, j.get("url","no meme"))

@bot.command(name='compliment')
async def xcompliment(ctx):
    await put(ctx, random.choice(["you eat","you breathe","you exist","absolute gng"]))

@bot.command(name='roast')
async def xroast(ctx):
    await put(ctx, random.choice(["skill issue","touch grass","ratio","stay mad"]))

@bot.command(name='ai')
async def xai(ctx, *, prompt):
    async with aiohttp.ClientSession() as s:
        async with s.get(f"https://text.pollinations.ai/{quote(prompt)}") as r:
            txt = await r.text()
            await put(ctx, txt[:1980] or "no reply")

@bot.command(name='imagine')
async def ximagine(ctx, *, prompt):
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
    await put(ctx, url)

@bot.command(name='draw')
async def xdraw(ctx, *, prompt):
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1024&height=1024&nologo=true"
    await put(ctx, url)

@bot.command(name='waifu')
async def xwaifu(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://api.waifu.pics/sfw/waifu") as r:
            j=await r.json(); await put(ctx, j.get("url","no waifu"))

@bot.command(name='neko')
async def xneko(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://api.waifu.pics/sfw/neko") as r:
            j=await r.json(); await put(ctx, j.get("url","no neko"))

@bot.command(name='nsfwwaifu')
async def xnsfwwaifu(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://api.waifu.pics/nsfw/waifu") as r:
            j=await r.json(); await put(ctx, j.get("url","no nsfw"))

@bot.command(name='nsfwneko')
async def xnsfwneko(ctx):
    async with aiohttp.ClientSession() as s:
        async with s.get("https://api.waifu.pics/nsfw/neko") as r:
            j=await r.json(); await put(ctx, j.get("url","no nsfw"))

@bot.command(name='delself')
async def xdelself(ctx, n:int=20):
    msgs=[m async for m in ctx.channel.history(limit=n, before=ctx.message) if m.author==bot.user]
    for m in msgs:
        try: await m.delete(); await asyncio.sleep(0.2)
        except Exception: pass
    try: await ctx.message.delete()
    except Exception: pass

@bot.command(name='editlast')
async def xeditlast(ctx, *, text):
    async for m in ctx.channel.history(limit=50):
        if m.author==bot.user and m.id!=ctx.message.id:
            await m.edit(content=text); return await put(ctx, "edited last")
    await put(ctx, "nothing to edit")

@bot.command(name='pin')
async def xpin(ctx):
    try:
        await ctx.message.pin(); await put(ctx, "pinned")
    except Exception as e: await put(ctx, f"pin err :: {e}")

@bot.command(name='unpin')
async def xunpin(ctx):
    try:
        await ctx.message.unpin(); await put(ctx, "unpinned")
    except Exception as e: await put(ctx, f"unpin err :: {e}")

@bot.command(name='setafk')
async def xsetafk(ctx, *, msg='away from desk'):
    AFK["msg"]=msg; await put(ctx, f"afk msg :: {msg}")

@bot.command(name='createserver')
async def xcreateserver(ctx, *, name):
    try:
        g = await bot.create_guild(name)
        await put(ctx, f"created guild :: {g.name} [{g.id}]")
    except Exception as e: await put(ctx, f"createserver err :: {e}")

@bot.command(name='deleteguild')
async def xdeleteguild(ctx):
    if not ctx.guild: await put(ctx, "no guild context"); return
    try:
        await ctx.guild.delete(); await put(ctx, "guild deleted")
    except Exception as e: await put(ctx, f"deleteguild err :: {e}")

@bot.command(name='drip0')
async def xdrip0(ctx):
    await put(ctx, 'drip0 :: absolute ollie')

@bot.command(name='drip1')
async def xdrip1(ctx):
    await put(ctx, 'drip1 :: absolute ollie')

@bot.command(name='drip2')
async def xdrip2(ctx):
    await put(ctx, 'drip2 :: absolute ollie')

@bot.command(name='drip3')
async def xdrip3(ctx):
    await put(ctx, 'drip3 :: absolute ollie')

@bot.command(name='drip4')
async def xdrip4(ctx):
    await put(ctx, 'drip4 :: absolute ollie')

@bot.command(name='drip5')
async def xdrip5(ctx):
    await put(ctx, 'drip5 :: absolute ollie')

@bot.command(name='drip6')
async def xdrip6(ctx):
    await put(ctx, 'drip6 :: absolute ollie')

@bot.command(name='drip7')
async def xdrip7(ctx):
    await put(ctx, 'drip7 :: absolute ollie')

@bot.command(name='drip8')
async def xdrip8(ctx):
    await put(ctx, 'drip8 :: absolute ollie')

@bot.command(name='drip9')
async def xdrip9(ctx):
    await put(ctx, 'drip9 :: absolute ollie')

@bot.command(name='drip10')
async def xdrip10(ctx):
    await put(ctx, 'drip10 :: absolute ollie')

@bot.command(name='drip11')
async def xdrip11(ctx):
    await put(ctx, 'drip11 :: absolute ollie')

@bot.command(name='drip12')
async def xdrip12(ctx):
    await put(ctx, 'drip12 :: absolute ollie')

@bot.command(name='drip13')
async def xdrip13(ctx):
    await put(ctx, 'drip13 :: absolute ollie')

@bot.command(name='drip14')
async def xdrip14(ctx):
    await put(ctx, 'drip14 :: absolute ollie')

@bot.command(name='drip15')
async def xdrip15(ctx):
    await put(ctx, 'drip15 :: absolute ollie')

@bot.command(name='drip16')
async def xdrip16(ctx):
    await put(ctx, 'drip16 :: absolute ollie')

@bot.command(name='drip17')
async def xdrip17(ctx):
    await put(ctx, 'drip17 :: absolute ollie')

@bot.command(name='drip18')
async def xdrip18(ctx):
    await put(ctx, 'drip18 :: absolute ollie')

@bot.command(name='drip19')
async def xdrip19(ctx):
    await put(ctx, 'drip19 :: absolute ollie')

@bot.command(name='drip20')
async def xdrip20(ctx):
    await put(ctx, 'drip20 :: absolute ollie')

@bot.command(name='drip21')
async def xdrip21(ctx):
    await put(ctx, 'drip21 :: absolute ollie')

@bot.command(name='drip22')
async def xdrip22(ctx):
    await put(ctx, 'drip22 :: absolute ollie')

@bot.command(name='drip23')
async def xdrip23(ctx):
    await put(ctx, 'drip23 :: absolute ollie')

@bot.command(name='drip24')
async def xdrip24(ctx):
    await put(ctx, 'drip24 :: absolute ollie')

@bot.command(name='drip25')
async def xdrip25(ctx):
    await put(ctx, 'drip25 :: absolute ollie')

@bot.command(name='drip26')
async def xdrip26(ctx):
    await put(ctx, 'drip26 :: absolute ollie')

@bot.command(name='drip27')
async def xdrip27(ctx):
    await put(ctx, 'drip27 :: absolute ollie')

@bot.command(name='drip28')
async def xdrip28(ctx):
    await put(ctx, 'drip28 :: absolute ollie')

@bot.command(name='drip29')
async def xdrip29(ctx):
    await put(ctx, 'drip29 :: absolute ollie')

@bot.command(name='drip30')
async def xdrip30(ctx):
    await put(ctx, 'drip30 :: absolute ollie')

@bot.command(name='drip31')
async def xdrip31(ctx):
    await put(ctx, 'drip31 :: absolute ollie')

@bot.command(name='drip32')
async def xdrip32(ctx):
    await put(ctx, 'drip32 :: absolute ollie')

@bot.command(name='drip33')
async def xdrip33(ctx):
    await put(ctx, 'drip33 :: absolute ollie')

@bot.command(name='drip34')
async def xdrip34(ctx):
    await put(ctx, 'drip34 :: absolute ollie')

@bot.command(name='drip35')
async def xdrip35(ctx):
    await put(ctx, 'drip35 :: absolute ollie')

@bot.command(name='drip36')
async def xdrip36(ctx):
    await put(ctx, 'drip36 :: absolute ollie')

@bot.command(name='drip37')
async def xdrip37(ctx):
    await put(ctx, 'drip37 :: absolute ollie')

@bot.command(name='drip38')
async def xdrip38(ctx):
    await put(ctx, 'drip38 :: absolute ollie')

@bot.command(name='drip39')
async def xdrip39(ctx):
    await put(ctx, 'drip39 :: absolute ollie')

@bot.command(name='drip40')
async def xdrip40(ctx):
    await put(ctx, 'drip40 :: absolute ollie')

@bot.command(name='drip41')
async def xdrip41(ctx):
    await put(ctx, 'drip41 :: absolute ollie')

@bot.command(name='drip42')
async def xdrip42(ctx):
    await put(ctx, 'drip42 :: absolute ollie')

@bot.command(name='drip43')
async def xdrip43(ctx):
    await put(ctx, 'drip43 :: absolute ollie')

@bot.command(name='drip44')
async def xdrip44(ctx):
    await put(ctx, 'drip44 :: absolute ollie')

@bot.command(name='drip45')
async def xdrip45(ctx):
    await put(ctx, 'drip45 :: absolute ollie')

@bot.command(name='drip46')
async def xdrip46(ctx):
    await put(ctx, 'drip46 :: absolute ollie')

@bot.command(name='drip47')
async def xdrip47(ctx):
    await put(ctx, 'drip47 :: absolute ollie')

@bot.command(name='drip48')
async def xdrip48(ctx):
    await put(ctx, 'drip48 :: absolute ollie')

@bot.command(name='drip49')
async def xdrip49(ctx):
    await put(ctx, 'drip49 :: absolute ollie')

@bot.command(name='drip50')
async def xdrip50(ctx):
    await put(ctx, 'drip50 :: absolute ollie')

@bot.command(name='drip51')
async def xdrip51(ctx):
    await put(ctx, 'drip51 :: absolute ollie')

@bot.command(name='drip52')
async def xdrip52(ctx):
    await put(ctx, 'drip52 :: absolute ollie')

@bot.command(name='drip53')
async def xdrip53(ctx):
    await put(ctx, 'drip53 :: absolute ollie')

@bot.command(name='drip54')
async def xdrip54(ctx):
    await put(ctx, 'drip54 :: absolute ollie')

@bot.command(name='drip55')
async def xdrip55(ctx):
    await put(ctx, 'drip55 :: absolute ollie')

@bot.command(name='drip56')
async def xdrip56(ctx):
    await put(ctx, 'drip56 :: absolute ollie')

@bot.command(name='drip57')
async def xdrip57(ctx):
    await put(ctx, 'drip57 :: absolute ollie')

@bot.command(name='drip58')
async def xdrip58(ctx):
    await put(ctx, 'drip58 :: absolute ollie')

@bot.command(name='drip59')
async def xdrip59(ctx):
    await put(ctx, 'drip59 :: absolute ollie')


@bot.event
async def on_message_delete(m):
    if m.guild is None: return
    SNIPE[m.channel.id] = {'author': str(m.author), 'content': m.content, 'time': str(m.created_at)}
    if LOGCH['id']:
        try:
            ch = bot.get_channel(LOGCH['id'])
            if ch: await ch.send(f'deleted :: {m.author} :: {m.content[:500]}')
        except Exception: pass

@bot.event
async def on_message_edit(b,a):
    if b.content==a.content: return
    EDITSNIPE[b.channel.id] = {'before': b.content, 'after': a.content}
    if LOGCH['id']:
        try:
            ch = bot.get_channel(LOGCH['id'])
            if ch: await ch.send(f'edited :: {b.author} :: {b.content[:300]} -> {a.content[:300]}')
        except Exception: pass

@bot.event
async def on_message(m):
    if SKULL['on'] and m.author==bot.user and (m.content or '') and not (m.content or '').startswith(C.get('prefix','!')):
        try: await m.add_reaction('💀')
        except Exception: pass
    if AUTOBURN['on'] and m.author != bot.user:
        _now = time.time()
        if _now - BURN_CD.get(m.author.id, 0) >= 5:
            BURN_CD[m.author.id] = _now
            try:
                await m.channel.send(f"{m.author.mention} {random.choice(INSULTS)}")
            except Exception:
                pass
    await bot.process_commands(m)

@bot.event
async def on_ready():
    try:
        await bot.change_presence(activity=discord.Game(name=C.get('presence',['absolute ollie built by olivia'])[0]))
    except Exception: pass
    print(f'hooked :: {bot.user} :: guilds={len(bot.guilds)} :: commands={len(bot.commands)}')

@bot.command(name="rpc")
async def _rpc(ctx, *, args):
    parts = (args or "").split(maxsplit=1)
    if len(parts) == 2:
        try:
            hours = int(parts[0])
            name = parts[1].strip()
        except ValueError:
            hours = 0
            name = args.strip()
    else:
        hours = 0
        name = args.strip() or "Custom Activity"
    start_ms = int((time.time() - hours * 3600) * 1000)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=name, timestamps={"start": start_ms}))
    await put(ctx, f"rpc :: {name} :: {hours}h")

@bot.command(name="setrpc")
async def _setrpc(ctx, *, args):
    await _rpc.callback(ctx, args=args)

@bot.command(name='ip')
async def _ip(ctx, *, addr):
    async with aiohttp.ClientSession() as s:
        async with s.get(f'http://ip-api.com/json/{addr}') as r:
            j = await r.json()
            if j.get('status') == 'success':
                await put(ctx, f"ip :: {j.get('query')} :: {j.get('country')}, {j.get('regionName')}, {j.get('city')} | isp {j.get('isp')} | lat {j.get('lat')}, lon {j.get('lon')}")
            else:
                await put(ctx, f"ip lookup failed :: {j.get('message', 'err')}")

@bot.command(name='domain')
async def _domain(ctx, *, name):
    import socket
    try:
        ip = socket.gethostbyname(name.strip())
        await put(ctx, f"domain :: {name} -> {ip}")
    except Exception as e:
        await put(ctx, f"domain err :: {e}")

@bot.command(name='username')
async def _username(ctx, *, name):
    sites = [
        ('github', 'https://github.com/{}'),
        ('reddit', 'https://www.reddit.com/user/{}'),
        ('instagram', 'https://www.instagram.com/{}/'),
        ('twitter', 'https://twitter.com/{}'),
        ('tiktok', 'https://www.tiktok.com/@{}'),
        ('youtube', 'https://www.youtube.com/@{}'),
    ]
    out = []
    async with aiohttp.ClientSession() as s:
        for label, url in sites:
            try:
                async with s.get(url.format(name), timeout=8) as r:
                    out.append(f"{label}: {'claimed' if r.status == 200 else 'free'}")
            except Exception:
                out.append(f"{label}: error")
    await put(ctx, chr(10).join(out))

@bot.command(name='email')
async def _email(ctx, *, addr):
    ok = '@' in addr and '.' in addr.split('@')[-1] and len(addr.split('@')) == 2
    await put(ctx, f"email :: {addr} :: {'valid syntax' if ok else 'invalid syntax'}")

@bot.command(name='phone')
async def _phone(ctx, *, num):
    cleaned = ''.join(c for c in num if c.isdigit() or c == '+')
    await put(ctx, f"phone :: {cleaned} :: digits={sum(c.isdigit() for c in cleaned)}")

@bot.command(name='osint')
async def _osint(ctx):
    await put(ctx, 'osint commands: ip domain username email phone')


@bot.command(name='discordid')
async def _discordid(ctx, *, did):
    did = did.strip().strip('<@!>')
    try:
        user = await bot.fetch_user(int(did))
    except Exception as e:
        await put(ctx, f'discord id err :: {e}')
        return
    parts = [f"discord :: {user} :: id={user.id} :: created={user.created_at} :: avatar={user.display_avatar.url}"]
    names = [user.name]
    if getattr(user, 'global_name', None):
        names.append(user.global_name)
    try:
        async with aiohttp.ClientSession() as s:
            for nm in names:
                async with s.post('https://users.roblox.com/v1/usernames/users', json={'usernames': [nm], 'excludeBannedUsers': False}) as r:
                    data = await r.json()
                    for u in data.get('data', []):
                        uid = u.get('id')
                        parts.append(f"roblox match :: {u.get('name')} :: id={uid}")
                        async with s.get(f'https://users.roblox.com/v1/users/{uid}') as r2:
                            d2 = await r2.json()
                            parts.append(f"roblox profile :: https://www.roblox.com/users/{uid}/profile")
                            parts.append(f"created :: {d2.get('created')} :: desc :: {str(d2.get('description',''))[:120]}")
    except Exception as e:
        parts.append(f'roblox lookup err :: {e}')
    await put(ctx, chr(10).join(parts))

@bot.command(name='leaksearch')
async def _leaksearch(ctx, *, did):
    await _discordid.callback(ctx, did=did)

@bot.command(name='roblox')
async def _roblox(ctx, *, name):
    name = name.strip()
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post('https://users.roblox.com/v1/usernames/users', json={'usernames': [name], 'excludeBannedUsers': False}) as r:
                data = await r.json()
                found = (data.get('data') or [None])[0]
                if not found:
                    await put(ctx, f'roblox :: {name} :: not found')
                    return
                uid = found.get('id')
                async with s.get(f'https://users.roblox.com/v1/users/{uid}') as r2:
                    d2 = await r2.json()
                    await put(ctx, f"roblox :: {d2.get('name')} :: id={uid} :: created={d2.get('created')} :: desc={str(d2.get('description',''))[:160]} :: profile=https://www.roblox.com/users/{uid}/profile")
    except Exception as e:
        await put(ctx, f'roblox err :: {e}')


@bot.command(name='namesearch', aliases=['peoplesearch'])
async def _namesearch(ctx, *, name):
    import html as _html
    name = name.strip()
    if not name:
        await put(ctx, 'usage :: namesearch <full name>')
        return
    q = '"' + name + '" phone OR address OR employer OR family OR job'
    url = 'https://duckduckgo.com/html/?q=' + quote(q)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    async with aiohttp.ClientSession() as s:
        async with s.get(url, headers=headers, timeout=15) as r:
            body = await r.text()
    snips = re.findall(r'class="result__snippet">(.*?)</a>', body, re.S)
    titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', body, re.S)
    out = []
    for i, sn in enumerate(snips[:8]):
        t = _html.unescape(re.sub(r'<[^>]+>', '', titles[i] if i < len(titles) else 'hit'))
        txt = _html.unescape(re.sub(r'<[^>]+>', '', sn))
        out.append(f'{i+1}. {t}')
        out.append(f'   {txt}')
    if not out:
        await put(ctx, f'namesearch :: no public hits for {name}')
    else:
        await put(ctx, 'namesearch :: ' + name + chr(10) + chr(10).join(out))


@bot.command(name='autoburn')
async def _autoburn(ctx, *, mode=None):
    if mode is None or mode.lower() == 'toggle':
        AUTOBURN['on'] = not AUTOBURN['on']
    elif mode.lower() in ('on','true','enable','1'):
        AUTOBURN['on'] = True
    elif mode.lower() in ('off','false','disable','0'):
        AUTOBURN['on'] = False
    await put(ctx, f"autoburn :: {'on' if AUTOBURN['on'] else 'off'}")

@bot.command(name='burn')
async def _burn(ctx, *, target):
    member = None
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
    elif ctx.guild:
        member = discord.utils.find(lambda m: target.lower() in m.name.lower() or (m.nick and target.lower() in m.nick.lower()), ctx.guild.members)
    if member is not None:
        await put(ctx, f"{member.mention} {random.choice(INSULTS)}")
    else:
        await put(ctx, f"{target} {random.choice(INSULTS)}")


async def main():
    await bot.start(C['token'])

asyncio.run(main())

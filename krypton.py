import discord
import requests
from discord.ext import commands
from discord.ext import tasks
from tinydb import TinyDB, Query
from getGEXP import storeGEXP, getPlayerGEXPMessage, getWeeklyGEXPTopMessage, getDailyGEXPTopMessage
from infoCommand import getGuildInfoMessage

token = 'BOT_TOKEN'
apiKey = 'API_KEY'
cmdPrefix = '$'
bot = commands.Bot(command_prefix=cmdPrefix)
bot.remove_command('help')
dataDB = TinyDB('dataDB.json')
noName = discord.Embed(title='No Name Provided', description='Please provide a username after the command, or link your Discord user ID with your Minecraft name with the command **link**.', color=11141120
                       ).set_footer(text='Krypton Bot made by Yuushi#5964')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="your GEXP | $help"))
    getEXP.start()
    setRoles.start()
    remindLink.start()
    print('Krypton Bot is ready.')


@tasks.loop(minutes=15)
async def getEXP():
    clearDB()
    storeGEXP()
    guild = bot.get_guild(714335785469345793)
    unlinkRole = discord.utils.get(guild.roles, name='Unlinked')
    linkRole = discord.utils.get(guild.roles, name='Linked')
    botRole = discord.utils.get(guild.roles, name='Bots')
    for member in guild.members:
        if botRole in member.roles:
            pass
        elif not dataDB.get(Query()['userID'] == member.id):
            await member.add_roles(unlinkRole)
            await member.remove_roles(linkRole)
        else:
            await member.add_roles(linkRole)
            await member.remove_roles(unlinkRole)


@tasks.loop(hours=1)
async def remindLink():
    guild = bot.get_guild(714335785469345793)
    unlinkRole = discord.utils.get(guild.roles, name='Unlinked')
    unlink_channel = bot.get_channel(728366357455962153)
    await unlink_channel.send(content='<@&' + str(unlinkRole.id) + '>')
    await unlink_channel.send(embed=discord.Embed(title='Link your Account', description='Please make sure to link your Minecraft username with your Discord account so that your guild role can be updated automatically. You can do so by going into the <#714643693738655804> channel and typing `$link <ign>`.',
                                                  color=11141120).set_footer(text='Krypton Bot made by Yuushi#5964'))


@tasks.loop(minutes=15)
async def setRoles():
    guild = bot.get_guild(714335785469345793)
    bot_channel = bot.get_channel(728296239518580846)
    for member in guild.members:
        if dataDB.get(Query()['userID'] == member.id):
            search = dataDB.get(Query()['userID'] == member.id)
            weeklyEXP = search.get('weeklyEXP')
            if 0 <= weeklyEXP < 100000:
                rank = 'Initiate'
            elif 100000 <= weeklyEXP < 200000:
                rank = 'Experienced'
            else:
                rank = 'Krypt Gods'
            role = discord.utils.get(guild.roles, name=rank)
            if role not in member.roles:
                await delete_role(member, rank, guild)
                await member.add_roles(role)
                await bot_channel.send('<@' + str(member.id) + '>', embed=discord.Embed(title=':diamond_shape_with_a_dot_inside: You\'re shining!', description='Your rank has been changed to **' + rank + '** because of the total of Guild Experience you earned this week. \n **Total Weekly GEXP**: ' + format(weeklyEXP,
                                                                                                                                                                                                                 ',d') + ' exp',
                                                           color=43520).set_footer(text='Krypton Bot made by Yuushi#5964'))


async def delete_role(member, rank, guild):
    if rank == 'Krypt Gods':
        await member.remove_roles(discord.utils.get(guild.roles, name='Initiate'), discord.utils.get(guild.roles, name='Experienced'))
    elif rank == 'Experienced':
        await member.remove_roles(discord.utils.get(guild.roles, name='Initiate'), discord.utils.get(guild.roles, name='Krypt Gods'))
    elif rank == 'Initiate':
        await member.remove_roles(discord.utils.get(guild.roles, name='Experienced'), discord.utils.get(guild.roles, name='Krypt Gods'))


def getName(ctx):
    userID = ctx.message.author.id
    if dataDB.get(Query()['userID'] == userID):
        search = dataDB.get(Query()['userID'] == userID)
        uuid = search.get('uuid')
        return uuid
    else:
        return None

def clearDB():
    guildData = requests.get('https://api.hypixel.net/guild?key=' + apiKey + '&id=5ef336138ea8c950b6cb73f2').json()
    apiUUID = []
    for i in range(len(guildData["guild"]["members"])):
        apiUUID.append(guildData["guild"]["members"][i]["uuid"])
    for i in range(len(dataDB)):
        dbUUID = dataDB.all()[i]['uuid']
        if dbUUID not in apiUUID:
            dataDB.remove(Query()['uuid'] == dbUUID)


@bot.command()
async def help(ctx):
    helpMessage = discord.Embed(title='Help Menu', description='`' + cmdPrefix + 'help` + bring up this help menu \n `' + cmdPrefix + 'link <ign>` + link your Discord ID to your Minecraft name (not case sensitive) \n '
                                                               '`' + cmdPrefix + 'exp <ign>` + get a member\'s GEXP \n `' + cmdPrefix + 'daily` + get the daily GEXP leaderboard \n '
                                                               '`' + cmdPrefix + 'weekly` + get the weekly GEXP leaderboard')
    helpMessage.set_footer(text='Krypton Bot made by Yuushi#5964')
    await ctx.send(embed=helpMessage)


@bot.command()
async def link(ctx, name=None):
    if name is None:
        await ctx.send(embed=discord.Embed(title='No Username Provided', description='Please provide your Minecraft username to be linked with your Discord user ID.', color=11141120
                                           ).set_footer(text='Krypton Bot made by Yuushi#5964'))
    else:
        userID = ctx.message.author.id
        uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + name).json()["id"]
        guildData = requests.get('https://api.hypixel.net/guild?key=' + apiKey + '&id=5ef336138ea8c950b6cb73f2').json()
        uuidList = []
        for i in range(len(guildData["guild"]["members"])):
            uuidList.append(guildData["guild"]["members"][i]["uuid"])
        if uuid in uuidList:
            guild = bot.get_guild(714335785469345793)
            unlinkRole = discord.utils.get(guild.roles, name='Unlinked')
            linkRole = discord.utils.get(guild.roles, name='Linked')
            memberRole = discord.utils.get(guild.roles, name='Member')
            guestRole = discord.utils.get(guild.roles, name='Guest')
            initiateRole = discord.utils.get(guild.roles, name='Initiate')
            guildMemberRole = discord.utils.get(guild.roles, name='----Guild Member----')
            dataDB.update({'userID': userID}, Query().uuid == uuid)
            await ctx.send(embed=discord.Embed(title='Username Linked',
                                               description='Your Discord user ID has been linked with your Minecraft username, hence your role will automatically be updated depending on your weekly Guild Experience.',
                                               color=43520
                                               ).set_footer(text='Krypton Bot made by Yuushi#5964'))
            member = guild.get_member(userID)
            await member.remove_roles(unlinkRole)
            await member.remove_roles(guestRole)
            await member.add_roles(memberRole)
            await member.add_roles(guildMemberRole)
            await member.add_roles(initiateRole)
            await member.add_roles(linkRole)
        else:
            await ctx.send(embed=discord.Embed(title='Impersonator!',
                                               description='You are not a member of the Krypton\'s guild so you can\'t link your Minecraft name to the guild\'s bot. Don\'t try to impersonate us!',
                                               color=11141120
                                               ).set_footer(text='Krypton Bot made by Yuushi#5964'))


@bot.command()
async def exp(ctx, name=None):
    if name is None:
        uuid = getName(ctx)
        name = requests.get('https://api.hypixel.net/player?key=' + apiKey + '&uuid=' + uuid).json()["player"]["displayname"]
        if name is None:
            await ctx.send(embed=noName)
    if name is not None:
        uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/' + name).json()["id"]
        await ctx.send(embed=getPlayerGEXPMessage(uuid))


@bot.command()
async def daily(ctx):
    await ctx.send(embed=getDailyGEXPTopMessage())


@bot.command()
async def weekly(ctx):
    await ctx.send(embed=getWeeklyGEXPTopMessage())
    
    
@bot.command()
async def info(ctx):
    await ctx.send(embed=getGuildInfoMessage())


@bot.command()
async def list(ctx):
    guild = bot.get_guild(714335785469345793)
    unlinkRole = discord.utils.get(guild.roles, name='Unlinked')
    content = ''
    if (ctx.message.author.id == 272553041826414593) or (ctx.message.author.id == 193425484799803395):
        for member in guild.members:
            if unlinkRole in member.roles:
                content = content + '`-` <@' + str(member.id) + '> \n'
        await ctx.message.author.send(embed=discord.Embed(title='Unlinked Members').add_field(name='List of Unlinked members', value=content))
    else:
        await ctx.send(embed=discord.Embed(title='An error has occured', description='This command is reserved to the guild owner <@' + str(272553041826414593) + '> and to the developer of the bot <@' + str(193425484799803395) + '>.', color=11141120).set_footer(text='Krypton Bot made by Yuushi#5964'))

bot.run(token)

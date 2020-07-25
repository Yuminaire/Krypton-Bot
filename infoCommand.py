import discord
import requests
from tinydb import TinyDB, Query
apiKey = 'API_KEY'
dataDB = TinyDB('dataDB.json')


def getGuildLevel(exp):
    expToLevelDict = {100000: 0, 250000: 1, 500000: 2, 1000000: 3, 1750000: 4, 2750000: 5, 4000000: 6, 5500000: 7, 7500000: 8}
    if exp >= 7500000:
        if exp < 15000000:
            return round((exp - 7500000) / 2500000) + 9
        else:
            return round((exp - 15000000) / 3000000) + 12
    else:
        for i in range(len(expToLevelDict)):
            if exp < list(expToLevelDict.keys())[i]:
                return expToLevelDict[list(expToLevelDict.keys())[i]]


def getGuildInfo():
    totalWeeklyEXP = []
    totalDailyEXP = []
    guildData = requests.get('https://api.hypixel.net/guild?key=' + apiKey + '&id=5ef336138ea8c950b6cb73f2').json()
    guildName = guildData["guild"]["name"]
    guildTag = guildData["guild"]["tag"]
    nbMembers = len(guildData["guild"]["members"])
    totalEXP = guildData["guild"]["exp"]
    guildLevel = getGuildLevel(totalEXP)
    for i in range(len(dataDB)):
        dailyEXP = dataDB.all()[i]['dailyEXP']
        totalDailyEXP.append(dailyEXP)
    totalDailyEXP = sum(totalDailyEXP)
    for i in range(len(dataDB)):
        weeklyEXP = dataDB.all()[i]['weeklyEXP']
        totalWeeklyEXP.append(weeklyEXP)
    totalWeeklyEXP = sum(totalWeeklyEXP)
    return guildName, guildTag, guildLevel, nbMembers, totalDailyEXP, totalWeeklyEXP


def getGuildInfoMessage():
    guildInfo = getGuildInfo()
    guildInfoMessage = discord.Embed(title='[' + guildInfo[1] + '] ' + guildInfo[0], url='https://plancke.io/hypixel/guild/name/krypton', description=str(guildInfo[3]) + '/125 members',
                                     color=16755200)
    guildInfoMessage.set_author(name='Guild Info')
    guildInfoMessage.add_field(name='Level', value=str(guildInfo[2]), inline=True)
    guildInfoMessage.add_field(name='Owner', value='KingFaleiro', inline=True)
    guildInfoMessage.add_field(name='Created on', value='24/06/2020', inline=True)
    guildInfoMessage.add_field(name='Daily Guild Experience', value='Total: ' + format(guildInfo[4], ',d') + ' exp', inline=False)
    guildInfoMessage.add_field(name='Weekly Guild Experience', value= 'Total: ' + format(guildInfo[5], ',d') + ' exp', inline=False)
    guildInfoMessage.set_footer(text='Krypton Bot made by Yuushi#5964')
    return guildInfoMessage





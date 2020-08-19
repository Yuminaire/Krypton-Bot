import requests
import discord
import datetime
from datetime import date
from tinydb import TinyDB, Query

apiKey = 'API_KEY'
dataDB = TinyDB('dataDB.json')


def storeGEXP():
    print('Retrieving GEXP data from Hypixel API', datetime.datetime.now())
    guildData = requests.get('https://api.hypixel.net/guild?key=' + apiKey + '&id=5ef336138ea8c950b6cb73f2').json()
    for i in range(len(guildData["guild"]["members"])):
        if len(list(guildData["guild"]["members"][i]["expHistory"].values())) == 7:
          uuid = guildData["guild"]["members"][i]["uuid"]
          weeklyEXP = sum(list(guildData["guild"]["members"][i]["expHistory"].values()))
          dailyEXP = list(guildData["guild"]["members"][i]["expHistory"].values())[0]
          if dataDB.get(Query()['uuid'] == uuid):
              dataDB.update({'weeklyEXP': weeklyEXP}, Query().uuid == uuid)
              dataDB.update({'dailyEXP': dailyEXP}, Query().uuid == uuid)
          else:
              dataDB.insert({'uuid': uuid, 'weeklyEXP': weeklyEXP, 'dailyEXP': dailyEXP, 'userID': ''})


def getPlayerGEXP(uuid):
    guildData = requests.get('https://api.hypixel.net/guild?key=' + apiKey + '&id=5ef336138ea8c950b6cb73f2').json()
    for i in range(len(guildData["guild"]["members"])):
        if guildData["guild"]["members"][i]["uuid"] == uuid:
            weeklyEXP = sum(list(guildData["guild"]["members"][i]["expHistory"].values()))
            dailyEXP = list(guildData["guild"]["members"][i]["expHistory"].values())
            dateDailyEXP = list(guildData["guild"]["members"][i]["expHistory"].keys())
            guildRank = guildData["guild"]["members"][i]["rank"]
            guildTag = guildData["guild"]["tag"]
            return weeklyEXP, dailyEXP, dateDailyEXP, guildRank, guildTag


def getPlayerGEXPMessage(uuid):
    name = requests.get('https://api.hypixel.net/player?key=' + apiKey + '&uuid=' + uuid).json()["player"]["displayname"]
    playerGEXP = getPlayerGEXP(uuid)
    playerGEXPMessage = discord.Embed(title='[' + playerGEXP[4] + '] ' + name, url='https://plancke.io/hypixel/guild/name/krypton', description=playerGEXP[3],
                                      color=16755200)
    playerGEXPMessage.set_author(name='Guild Experience')
    playerGEXPMessage.set_thumbnail(url='https://www.mc-heads.net/player/' + uuid)
    playerGEXPMessage.add_field(name='Weekly Experience', value='Total: ' + format(playerGEXP[0], ',d') + ' exp', inline=False)
    playerGEXPMessage.add_field(name='Detailed Experience', value=datetime.datetime.strptime(playerGEXP[2][0], '%Y-%m-%d').strftime('%d/%m/%Y') + ': ' + format(playerGEXP[1][0], ',d') + ' exp\n'
                                                                  + datetime.datetime.strptime(playerGEXP[2][1], '%Y-%m-%d').strftime('%d/%m/%Y') + ': ' + format(playerGEXP[1][1], ',d') + ' exp\n'
                                                                  + datetime.datetime.strptime(playerGEXP[2][2], '%Y-%m-%d').strftime('%d/%m/%Y') + ': ' + format(playerGEXP[1][2], ',d') + ' exp\n'
                                                                  + datetime.datetime.strptime(playerGEXP[2][3], '%Y-%m-%d').strftime('%d/%m/%Y') + ': ' + format(playerGEXP[1][3], ',d') + ' exp\n'
                                                                  + datetime.datetime.strptime(playerGEXP[2][4], '%Y-%m-%d').strftime('%d/%m/%Y') + ': ' + format(playerGEXP[1][4], ',d') + ' exp\n'
                                                                  + datetime.datetime.strptime(playerGEXP[2][5], '%Y-%m-%d').strftime('%d/%m/%Y') + ': ' + format(playerGEXP[1][5], ',d') + ' exp\n'
                                                                  + datetime.datetime.strptime(playerGEXP[2][6], '%Y-%m-%d').strftime('%d/%m/%Y') + ': ' + format(playerGEXP[1][6], ',d') + ' exp\n', inline=True)
    playerGEXPMessage.set_footer(text='Krypton Bot made by Yuushi#0001')
    return playerGEXPMessage


def getWeeklyGEXPTop():
    weeklyEXPDict = {}
    weeklyEXPContent1 = ''
    weeklyEXPContent2 = ''
    for i in range(len(dataDB)):
        uuid = dataDB.all()[i]['uuid']
        weeklyEXP = dataDB.all()[i]['weeklyEXP']
        weeklyEXPDict[uuid] = weeklyEXP
    weeklyEXPDict = {k: v for k, v in sorted(weeklyEXPDict.items(), key=lambda item: item[1], reverse=True)}
    for i in range(round(len(weeklyEXPDict) / 2)):
        name = requests.get('https://api.hypixel.net/player?key=' + apiKey + '&uuid=' + list(weeklyEXPDict.keys())[i]).json()["player"]["displayname"]
        weeklyEXPContent1 = weeklyEXPContent1 + '`#' + str(i + 1) + '` ' + name + ': ' + format(weeklyEXPDict[list(weeklyEXPDict.keys())[i]], ',d') + ' exp\n'
    for i in range(round(len(weeklyEXPDict) / 2), len(weeklyEXPDict)):
        name = requests.get('https://api.hypixel.net/player?key=' + apiKey + '&uuid=' + list(weeklyEXPDict.keys())[i]).json()["player"]["displayname"]
        weeklyEXPContent2 = weeklyEXPContent2 + '`#' + str(i + 1) + '` ' + name + ': ' + format(weeklyEXPDict[list(weeklyEXPDict.keys())[i]], ',d') + ' exp\n'
    return weeklyEXPContent1, weeklyEXPContent2, weeklyEXPDict


def getWeeklyGEXPTopMessage():
    messageContent = getWeeklyGEXPTop()
    weeklyGEXPTopMessage = discord.Embed(title='Krypton\'s Leaderboard', url='https://plancke.io/hypixel/guild/name/krypton',
                                         color=16755200)
    weeklyGEXPTopMessage.add_field(name='Position #1 to #' + str(round(len(messageContent[2]) / 2)), value=messageContent[0], inline=True)
    weeklyGEXPTopMessage.add_field(name='Position #' + str(round(len(messageContent[2]) / 2) + 1) + ' to #' + str(len(messageContent[2])), value=messageContent[1], inline=True)
    weeklyGEXPTopMessage.set_author(name='Weekly Guild Experience')
    weeklyGEXPTopMessage.set_footer(text='Krypton Bot made by Yuushi#0001')
    return weeklyGEXPTopMessage


def getDailyGEXPTop():
    dailyEXPDict = {}
    dailyEXPContent1 = ''
    dailyEXPContent2 = ''
    for i in range(len(dataDB)):
        uuid = dataDB.all()[i]['uuid']
        dailyEXP = dataDB.all()[i]['dailyEXP']
        dailyEXPDict[uuid] = dailyEXP
    dailyEXPDict = {k: v for k, v in sorted(dailyEXPDict.items(), key=lambda item: item[1], reverse=True)}
    for i in range(round(len(dailyEXPDict) / 2)):
        name = requests.get('https://api.hypixel.net/player?key=' + apiKey + '&uuid=' + list(dailyEXPDict.keys())[i]).json()["player"]["displayname"]
        dailyEXPContent1 = dailyEXPContent1 + '`#' + str(i + 1) + '` ' + name + ': ' + format(dailyEXPDict[list(dailyEXPDict.keys())[i]], ',d') + ' exp\n'
    for i in range(round(len(dailyEXPDict) / 2), len(dailyEXPDict)):
        name = requests.get('https://api.hypixel.net/player?key=' + apiKey + '&uuid=' + list(dailyEXPDict.keys())[i]).json()["player"]["displayname"]
        dailyEXPContent2 = dailyEXPContent2 + '`#' + str(i + 1) + '` ' + name + ': ' + format(dailyEXPDict[list(dailyEXPDict.keys())[i]], ',d') + ' exp\n'
    return dailyEXPContent1, dailyEXPContent2, dailyEXPDict


def getDailyGEXPTopMessage():
    messageContent = getDailyGEXPTop()
    dailyGEXPTopMessage = discord.Embed(title='Krypton\'s Leaderboard', url='https://plancke.io/hypixel/guild/name/krypton',
                                        color=16755200)
    dailyGEXPTopMessage.add_field(name='Position #1 to #' + str(round(len(messageContent[2]) / 2)), value=messageContent[0], inline=True)
    dailyGEXPTopMessage.add_field(name='Position #' + str(round(len(messageContent[2]) / 2) + 1) + ' to #' + str(len(messageContent[2])), value=messageContent[1], inline=True)
    dailyGEXPTopMessage.set_author(name='Daily Guild Experience')
    dailyGEXPTopMessage.set_footer(text='Krypton Bot made by Yuushi#5964')
    return dailyGEXPTopMessage

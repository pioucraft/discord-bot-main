import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord import app_commands
import os
import youtube_dl
import json
import random
import time
import requests


#set the client and the chdir
token = 
intents = discord.Intents().all()
bot = commands.Bot(command_prefix = "!?!", intents = intents)
os.chdir(r"/home/emmanuel_macron/Documents/programinc/discord-bot-main/")

#initialize the bot
@bot.event
async def on_ready():
    print("bot is ready")
    #sync commands
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(f"failed to sync commands: {e}")


#help command
@bot.tree.command(name=f"help", description="montre l'aide")
async def help(interaction: discord.Interaction):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        embed = discord.Embed(type = "rich", title = "help", description = f"1. /play: joue une musique de youtube dans le salon vocal  \n 2. /stop: arêtte la musique et quitte le salon vocal \n 3. /level montre le niveau d'un membre \n 4. /exactlevel: montre le niveau exact d'un membre en utilisant des décimales \n 5. /meme: génère un même aléatoire (provenant de r/rance). \n 6. utilise /help-politics pour montre l'aide en rapport avec le jeu des politiciens \n JE RAPELLE QUE LE BOT EST EN BÊTA ET QU'IL PEUT Y AVOIR DES BUGS, SI VOUS TROUVEZ UN BUG OU UNE INCOHÉRENCE MERCI DE LE REPORTER A UN ADMIN.", color=0x2e60aa)
        await interaction.response.send_message(embed=embed)

#/help politics command
@bot.tree.command(name=f"help-politics", description="montre l'aide en rapport avec le jeu des politiciens")
async def help_politics(interaction: discord.Interaction):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        embed = discord.Embed(type = "rich", title = "help", description = f"le jeu des politiciens est un jeu qui vous permet de collectionner des politiciens, des armes et de l'argent grâce a discord. \n Pour gagner de l'argent il suffit de faire /drop ou de parler dans le chat, la commande /drop vous permet aussi si vous avez de la chance de gagner une arme ou bien même mieux un politicien américain. \n Ensuite vous pouvez utiliser /money pour voir toute votre fortune et /pay pour envoyer de l'argent à un autre utilisateur. \n Pour voir vos armes il suffi de faire /list-guns et /show-gun pour voir une arme spécifique. Vous pouvez aussi envoyer des armes avec la commande /send-gun. \n Les politiciens dont vous êtes propriétaires peuvent êtres listés avec /list-politics mais si vous voulez voir les informations concernants un politicien précis il faudra utiliser /show-politic. \n plus tard il y aura une commande /shop pour acheter des objets et aussi un mode 'histoire'. \n JE RAPELLE QUE LE BOT EST EN BÊTA ET QU'IL PEUT Y AVOIR DES BUGS, SI VOUS TROUVEZ UN BUG OU UNE INCOHÉRENCE MERCI DE LE REPORTER A UN ADMIN.", color=0x2e60aa)
        await interaction.response.send_message(embed=embed)


#/play command
@bot.tree.command(name=f"play", description="le bot va jouer la musique de ton choix")
async def play(interaction: discord.Interaction, music: str):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        if (interaction.user.voice):
            await interaction.response.send_message("je vais faire de mon mieux pour te satisfaire")
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            YDL_OPTIONS = {'format': 'bestaudio'}
            if music.startswith("https://"):
                #load an url
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(music, download=False)
                    url2 = info['formats'][0]['url']
            else:
                #search on youtube
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    url = f"ytsearch: {music}"
                    info = ydl.extract_info(url, download=False)['entries'][0]
                    url2 = info['formats'][0]["url"]
            #play the music
            source = FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
            player = voice.play(source)

        else:
            await interaction.response.send_message("merci de rejoindre un salon vocal et de réessayer la commande")

#stop the music
@bot.tree.command(name="stop-music", description="le bot va arrêter de jouer la musique")
async def level(interaction: discord.Interaction):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        await interaction.response.send_message("j'essaie d'arrêter la musique")
        if (interaction.user.voice):
            await interaction.guild.voice_client.disconnect()



#show the level of the user
@bot.tree.command(name="level", description="affiche ton niveau ou celui d'un autre utilisateur")
async def level(interaction: discord.Interaction, user: discord.User):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        
        #set an embed
        embed = discord.Embed(type = "rich", title = "niveau", description = f"{user.mention} est niveau {users[str(user.id)]['level']} et a {users[str(user.id)]['experience']} xp", color=0x2e60aa)
        embed.set_image(url = "https://media.tenor.com/iS-rIkKhpMgAAAAd/god-bless-america-american-flag.gif")
        await interaction.response.send_message(embed=embed)

#show the exact level of the user
@bot.tree.command(name="exactlevel", description="affiche ton niveau exact ou celui d'un autre utilisateur avec des décimales")
async def level(interaction: discord.Interaction, user: discord.User):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        
        #set an embed
        embed = discord.Embed(type = "rich", title = "niveau exact", description = f"{user.mention} est niveau {str(float(users[str(user.id)]['experience']) ** (1/4))} et a {users[str(user.id)]['experience']} xp", color=0x2e60aa)
        embed.set_image(url = "https://media.tenor.com/iS-rIkKhpMgAAAAd/god-bless-america-american-flag.gif")
        await interaction.response.send_message(embed=embed)


#welcome message
@bot.event
async def on_member_join(member):
        channel = bot.get_channel(1062012487173681152)
        bienvenue = bot.get_channel(1050103281315233852)
        #set an embed
        embed = discord.Embed(type = "rich", title = "bienvenue", description = f"bienvenue {member.mention} sur america, n'oublie pas de regarder {bienvenue.mention}", color=0x2e60aa)
        embed.set_image(url = "https://media.tenor.com/iS-rIkKhpMgAAAAd/god-bless-america-american-flag.gif")
        await channel.send(embed=embed)




#quoifeur and xp
@bot.event
async def on_message(message):
    if not message.channel.guild:
        if not message.author.bot:
            print("quelqu'un a essayé de dm le bot")
    else:
        message.content = message.content
        message.content = message.content.lower()
        message.content = message.content.replace("kwa", "quoi")
        message.content = message.content.replace("qwa", "quoi")
        message.content = message.content.replace("koi", "quoi")
        message.content = message.content.replace("qoi", "quoi")
        message.content = message.content.replace("kaka", "caca")
        message.content = message.content.replace("oe", "ouais")
        message.content = message.content.replace("ouai", "ouais")
        message.content = message.content.replace(" ", "")
        message.content = message.content.replace("!", "")
        message.content = message.content.replace("?", "")
        message.content = message.content.replace("?", "")
        if not message.author.bot:
                with open("users.json", "r") as f:
                    users = json.load(f)
        
                letters = len(message.content)
                if letters > 40:
                    letters = 40
                await update_data(users, message.author, letters)
                await update_politic_data(message.author, users)
                users[str(message.author.id)]["experience"] = users[str(message.author.id)]["experience"] + letters
                users[str(message.author.id)]["money"] = users[str(message.author.id)]["money"] + letters
                await level_up(users, message.author, message.channel)

                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)


                if message.content.endswith('quoi'):
                    await message.channel.send("feur")
                    print("feur")
                if message.content.endswith('non'):
                    await message.channel.send("bril")
                    print("bril")
                if message.content.endswith('oui'):
                    await message.channel.send("stiti")
                    print("stiti")
                if message.content.endswith('caca'):
                    await message.channel.send("mogus")
                    print("mogus")
                if message.content.endswith('ouais'):
                    await message.channel.send("stern")
                    print("stern")




#update the user data if not in users.json
async def update_data(users, user, letters):
    if not user.bot:
        if not str(user.id) in users:
            users[str(user.id)] = {}
        if not "experience" in users[str(user.id)]:
            users[str(user.id)]["experience"] = letters
            users[str(user.id)]["level"] = 1

#level up the user if enough xp
async def level_up(users, user, channel):
    experience = users[str(user.id)]["experience"]
    lvl_start = users[str(user.id)]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await channel.send("{} a atteint le niveau {}".format(user.mention, lvl_end))
        users[str(user.id)]["level"] = lvl_end

        #add roles
        if lvl_end >= 5 and not discord.utils.get(user.guild.roles, name="americain bg") in user.roles:
            await channel.send("bravo {} tu as atteint le niveau 5, tu vas donc recevoir le role americain bg".format(user.mention))
            await user.add_roles(discord.utils.get(user.guild.roles, name="americain bg"))

        if lvl_end >= 10 and not discord.utils.get(user.guild.roles, name="americain très bg") in user.roles:
            await channel.send("bravo {} tu as atteint le niveau 10, tu vas donc recevoir le role americain très bg".format(user.mention))
            await user.add_roles(discord.utils.get(user.guild.roles, name="americain très bg"))

        if lvl_end >= 15 and not discord.utils.get(user.guild.roles, name="americain ultra mega bg") in user.roles:
            await channel.send("bravo {} tu as atteint le niveau 15, tu vas donc recevoir le role americain ultra mega bg".format(user.mention))
            await user.add_roles(discord.utils.get(user.guild.roles, name="americain ultra mega bg"))
        
        if lvl_end >= 20 and not discord.utils.get(user.guild.roles, name="tah l'americain") in user.roles:
            await channel.send("bravo {} tu as atteint le niveau 20, tu vas donc recevoir le role americain tah l'americain".format(user.mention))
            await user.add_roles(discord.utils.get(user.guild.roles, name="tah l'americain"))
            

'''
politics part

'''
#/drop command
@bot.tree.command(name="drop", description="drop une lootbox avec des politiciens et des armes dedans")
async def drop(interaction: discord.interactions):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        await update_politic_data(interaction.user, users)
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
        if time.time() - users[str(interaction.user.id)]["politics"]["lastdrop"] > 30 * 60:
            with open("politics.json", "r") as f:
                politics = json.load(f)
            #get a politic
            if random.randint(1, 10) == 1:
                politic = random.randint(0, 45)
                politic_name = politics[politic]["presidentName"]
                party = politics[politic]["politicalParty"]
                politic_id = str(politics[politic]["_id"])
                embed = discord.Embed(type = "rich", title = politic_name, description = f"bravo, tu as gagneé {politic_name} du parti {party}", color=0x2e60aa)
                embed.set_image(url = politics[politic]["imgThumb"])
                await interaction.response.send_message(embed=embed)

                #save the politic to the users.json
                with open("users.json", "r") as f:
                        users = json.load(f)
                if not politic_id in users[str(interaction.user.id)]["politics"]["list"]:
                    users[str(interaction.user.id)]["politics"]["list"].append(politic_id)
                    users[str(interaction.user.id)]["politics"]["lastdrop"] = time.time()
                    with open("users.json", "w") as f:
                        json.dump(users, f, indent=4)

            #get a gun
            elif random.randint(1, 5) == 1:
                with open("guns.json", "r") as f:
                    guns = json.load(f)
                gun = random.randint(0, 9)
                gun_name = guns[gun]["name"]
                rarity = random.randint(1, 5)
                basefirerate = random.randint(10, 100)
                firerate = basefirerate * rarity
                embed = discord.Embed(type="rich", title=gun_name, description=f"bravo tu as gagné un/une {gun_name} qui fait {str(firerate)} dégats par seconde et qui est de rareté {await rarity_name(rarity)}")
                await interaction.response.send_message(embed=embed)

                #store the data of the guns into users.json
                with open("users.json", "r") as f:
                    users = json.load(f)
                await update_politic_data(interaction.user, users)
                gun_id = users[str(interaction.user.id)]["guns"]["number"]
                users[str(interaction.user.id)]["guns"]["number"] += 1
                users[str(interaction.user.id)]["guns"][gun_id] = {}
                users[str(interaction.user.id)]["guns"][gun_id]["rarity"] = str(rarity)
                users[str(interaction.user.id)]["guns"][gun_id]["basefirerate"] = str(basefirerate)
                users[str(interaction.user.id)]["guns"][gun_id]["firerate"] = str(firerate)
                users[str(interaction.user.id)]["guns"][gun_id]["_id"] = guns[gun]["_id"]
                users[str(interaction.user.id)]["guns"][gun_id]["id"] = gun_id

            
                users[str(interaction.user.id)]["politics"]["lastdrop"] = time.time()
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)

            #get money
            else:
                money = random.randint(1, 100)
                await interaction.response.send_message(f"bravo tu as gagné {str(money)} $")
                with open("users.json", "r") as f:
                    users = json.load(f)
                await update_politic_data(interaction.user, users)
                users[str(interaction.user.id)]["politics"]["lastdrop"] = time.time()
                users[str(interaction.user.id)]["money"] = int(users[str(interaction.user.id)]["money"]) + money
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)
                time.sleep(0.1)

        else: 
            waitime = int(30 - ((time.time() - users[str(interaction.user.id)]["politics"]["lastdrop"]) / 60)) 
            await interaction.response.send_message(f"tu dois encore attendre {waitime} minutes avant ton prochain drop")
#show the money
@bot.tree.command(name="money", description="montre l'argent d'un utilisateur")
async def drop(interaction: discord.interactions, user: discord.User):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
                users = json.load(f)
        embed = discord.Embed(type = "rich", title = "argent", description = f"{user.mention} a {users[str(user.id)]['money']} $", color=0x2e60aa)
        embed.set_image(url = "https://media.tenor.com/iS-rIkKhpMgAAAAd/god-bless-america-american-flag.gif")
        await interaction.response.send_message(embed=embed)
        

#pay someone
@bot.tree.command(name="pay", description="envoyer de l'argent a un autre utilisateur")
async def pay(interaction: discord.Interaction, receiver: discord.User, amount: int):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        if users[str(interaction.user.id)]["money"] < amount:
            await interaction.response.send_message("tu n'as pas assez d'argent")
        elif str(amount).startswith("-"):
            await interaction.response.send_message("tu ne peux pas envoyer un nombre négatif d'argent")
        else:
            await update_politic_data(receiver, users)
            users[str(receiver.id)]["money"] += amount
            users[str(interaction.user.id)]["money"] -= amount
            await interaction.response.send_message(f"{amount}$ ont étés transférés a {receiver.mention}")
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

#list yours guns
@bot.tree.command(name="list-guns", description="fait une liste de toutes tes armes")
async def list_guns(interaction: discord.Interaction, page: int):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        with open("guns.json", "r") as f:
            guns = json.load(f)
            gun_number = users[str(interaction.user.id)]["guns"]["number"]
            message = f"voici la liste des armes que tu as à la page {page}: \n"
            show_number = (gun_number) - ((page - 1) * 10)
            if show_number > 10:
                show_number = 10
            for i in range (0, show_number):
                number_gun = i + ((page - 1) * 10)
                gun_id = int(users[str(interaction.user.id)]["guns"][str(number_gun)]["_id"])
                gun_local_id = int(users[str(interaction.user.id)]["guns"][str(number_gun)]["id"])
                gun_name = guns[gun_id - 1]["name"]
                rarity = int(users[str(interaction.user.id)]["guns"][str(number_gun)]["rarity"])
                firerate = int(users[str(interaction.user.id)]["guns"][str(number_gun)]["firerate"])
                message = message + f"{str(number_gun + 1)}. {gun_name}, dont la rareté est {await rarity_name(rarity)}, qui fait {firerate} dégats par seconde et dont l'id est {str(gun_local_id)} \n"

            await interaction.response.send_message(message)

#list your politics
@bot.tree.command(name="list-politics", description="fait une liste de tous tes politiciens")
async def list_politics(interaction: discord.Interaction):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        with open("politics.json", "r") as f:
            politics = json.load(f)
        politics_number = len(users[str(interaction.user.id)]["politics"]["list"])
        message = "les politiciens que tu as sont \n"
        for i in range(0, politics_number):
            politic_id = users[str(interaction.user.id)]["politics"]["list"][i]
            politic_name = politics[int(politic_id)]["presidentName"]
            message = message + f"{politic_name} dont l'id est {politic_id}, \n"
        await interaction.response.send_message(message)

#send a gun to someone
@bot.tree.command(name="send-gun", description="envoie une de tes armes à un de tes amis")
async def send_gun(interaction: discord.Interaction, receiver: discord.User, gun_id: int):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        if not str(gun_id) in users[str(interaction.user.id)]["guns"]:
            await interaction.response.send_message(f"tu n'as pas d'arme avec l'id {gun_id}")
        else:
            await update_politic_data(receiver, users)
            new_id = users[str(receiver.id)]["guns"]["number"]
            users[str(receiver.id)]["guns"][str(new_id)] = {}
            users[str(receiver.id)]["guns"]["number"] += 1
            users[str(receiver.id)]["guns"][str(new_id)]["rarity"] = users[str(interaction.user.id)]["guns"][str(gun_id)]["rarity"]
            users[str(receiver.id)]["guns"][str(new_id)]["basefirerate"] = users[str(interaction.user.id)]["guns"][str(gun_id)]["basefirerate"]
            users[str(receiver.id)]["guns"][str(new_id)]["firerate"] = users[str(interaction.user.id)]["guns"][str(gun_id)]["firerate"]
            users[str(receiver.id)]["guns"][str(new_id)]["_id"] = users[str(interaction.user.id)]["guns"][str(gun_id)]["_id"]
            users[str(receiver.id)]["guns"][str(new_id)]["id"] = new_id
            users[str(interaction.user.id)]["guns"][str(gun_id)]["rarity"] = "5"
            users[str(interaction.user.id)]["guns"][str(gun_id)]["basefirerate"] = "1"
            users[str(interaction.user.id)]["guns"][str(gun_id)]["firerate"] = "1"
            users[str(interaction.user.id)]["guns"][str(gun_id)]["_id"] = "1"
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

#view a specific gun
@bot.tree.command(name="show-gun", description="montre les informations a propos d'une amre spécifique que tu as")
async def show_gun(interaction: discord.Interaction, gun_id: int):
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        with open("guns.json", "r") as f:
            guns = json.load(f)
        if not str(gun_id) in users[str(interaction.user.id)]["guns"]:
            await interaction.response.send_message("tu n'as pas d'arme avec cet id")
        else:
            gun_global_id = users[str(interaction.user.id)]["guns"][str(gun_id)]["_id"]
            firerate = users[str(interaction.user.id)]["guns"][str(gun_id)]["firerate"]
            basefirerate = users[str(interaction.user.id)]["guns"][str(gun_id)]["basefirerate"]
            rarity = users[str(interaction.user.id)]["guns"][str(gun_id)]["rarity"]
            gun_name = guns[int(gun_global_id) - 1]["name"]
            gun_description = guns[int(gun_global_id) - 1]["description"]
            embed = discord.Embed(type = "rich", title = gun_name, description = f"{gun_name} qui est de rareté {await rarity_name(int(rarity))}, qui fait {basefirerate} dégats par secondes de base, qui grâce à sa rareté fait {firerate} dégats par secondes et dont la description est: {gun_description}", color=0x2e60aa)
            embed.set_image(url = "https://media.tenor.com/iS-rIkKhpMgAAAAd/god-bless-america-american-flag.gif")
            await interaction.response.send_message(embed=embed)

#show a politic
@bot.tree.command(name="show-politic", description="montre les informations a propos d'un politicien spécifique")
async def show_politic(interaction: discord.Interaction, politic_id: int): 
    if not interaction.channel.guild:
        print("quelqu'un a essayé de dm le bot")
    else:  
        with open("politics.json", "r") as f:
            politics = json.load(f)
        politic_name = politics[politic_id]["presidentName"]
        politic_elected_number = politics[politic_id]["presidentElectedNumber"]
        politic_vice_president = politics[politic_id]["vicePresident"]
        politic_party = politics[politic_id]["politicalParty"]
        politic_birth = politics[politic_id]["dateOfBirth"]
        embed = discord.Embed(type = "rich", title = politic_name, description = f"{politic_name} dont le vice président est {politic_vice_president} est le {politic_elected_number} président des états-unis, est du parti {politic_party} et est né le {politic_birth}", color=0x2e60aa)
        embed.set_image(url = "https://media.tenor.com/iS-rIkKhpMgAAAAd/god-bless-america-american-flag.gif")
        await interaction.response.send_message(embed=embed)



async def update_politic_data(user, users):
    if not user.bot:
        if not str(user.id) in users:
            users[str(user.id)] = {}
        if not "politics" in users[str(user.id)]:
            users[str(user.id)]["money"] = 1
            users[str(user.id)]["guns"] = {}
            users[str(user.id)]["guns"]["number"] = 0
            users[str(user.id)]["politics"] = {}
            users[str(user.id)]["politics"]["list"] = []
            users[str(user.id)]["politics"]["lastdrop"] = 0
            team = {}

async def rarity_name(rarity):
    if rarity == 1:
        rarity = "common"
    elif rarity == 2:
        rarity = "uncommon"
    elif rarity == 3:
        rarity = "rare"
    elif rarity == 4:
        rarity = "epic"
    elif rarity == 5:
        rarity = "legendary"
    return rarity



'''

end politics part

'''




'''

here we have some stupid features

'''

#/meme command
@bot.tree.command(name="meme", description="va récuperer un même aléatoire sur https://meme-api.com/gimme")
async def meme(interacton: discord.Interaction):
    meme_json = json.loads(requests.get("https://meme-api.com/gimme/rance/").content)
    while meme_json["nsfw"] or meme_json["spoiler"] == True:
        meme_json = json.loads(requests.get("https://meme-api.com/gimme/rance/").content)
    embed = discord.Embed(type="rich", title = meme_json["title"], description= meme_json["postLink"], color=0x2e60aa)
    embed.set_image(url = meme_json["url"])
    await interacton.response.send_message(embed=embed)
    
    

#run the bot with the token
bot.run(token)
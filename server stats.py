import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import csv
from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt

bot = commands.Bot(command_prefix='-')


@bot.event
async def on_ready():
    print ("Bot is online and ready to go!")
    await bot.wait_until_ready()
    #channel=bot.get_channel('435757614979088384')
    #await bot.send_message(channel,datetime.now())

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong")
    
@bot.event
async def on_message(message):
    print(message.channel)


async def time_check(newmessage,editmessage):
    await bot.wait_until_ready()
    while not bot.is_closed:
        now = datetime.strftime(datetime.now(), '%S')
        newchannel = bot.get_channel('435757614979088384')
        editchannel = bot.get_channel('699998420730904697')
        if int(now)%10 == 0:
            file =open("log.csv","r",encoding='UTF-8')
            data=csv.reader(file)
            times=[]
            for row in data:
                times.append(float(datetime.strftime((datetime.strptime(row[1].split(" ")[1].split(".")[0], '%H:%M:%S')),'%H')))
                
            density = gaussian_kde(times)
            xs = np.linspace(0,24,200)
            density.covariance_factor = lambda : .25
            density._compute_covariance()
            fig, ax = plt.subplots()
            ax.set_ylabel('Density')
            ax.set_xlabel('Risk')
            plt.plot(xs,density(xs))
            plt.savefig("Times.png")
            plt.show()
            file.close()
            if newmessage!=None:
                newmessage = await bot.delete_message(newmessage)
            newmessage = await bot.send_file(newchannel,'Times.png')
            print(newmessage.attachments[0]["url"])
            if editmessage!=None:
                editmessage = await bot.edit_message(editmessage,newmessage.attachments[0]["url"])
            else:
                editmessage = await bot.send_message(editchannel,newmessage.attachments[0]["url"])
            time = 1
        else:
            time = 0.1
        await asyncio.sleep(time)

newmessage=None
editmessage=None
bot.loop.create_task(time_check(newmessage,editmessage))

bot.run('NDM0NzQ5NjI2NDQ5NTI2ODI2.XpMVkA.OI1sZSMQBMFhX-3HWCp1xuWY5TU')



'699998420730904697'




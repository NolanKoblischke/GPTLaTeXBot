import gpt
import discord
from discord.ext.commands import bot
from discord.ext import commands
import sympy
import cv2
import json

settings = json.loads(open('settings.json').read())  # Load settings for ServerID, Gpt_Api_key, and Bot Token
bot = commands.Bot(command_prefix='.')


# Initialize Bot
@bot.event
async def on_ready():
    print("text2LaTeX bot is online.")
    print('Logged in as {0.user}'.format(bot))


# When a message is received convert message contents to LaTeX then reply with LaTeX png
@bot.event
async def on_message(message):
    if message.content.startswith('!tex '):
        tex = message.content[5:]
        print('{}: LaTeX={}'.format(message.author.name, tex))

        await bot.wait_until_ready()

        channel = bot.get_channel(int(settings['serverId']))

        try:
            latexRaw = gpt.generate(tex).strip().split("\n")[0]
            await channel.send("`"+latexRaw+"`")
            latex = "$$" + latexRaw + "$$"  # Generate LaTeX from text and format
            print("Generated LaTeX: " + latex)
        except AttributeError:
            await channel.send("Failed: GPT-3 server is overloaded, try again later")

        filename = 'tempImg.png'

        try:
            sympy.preview(latex, viewer='file', filename=filename, euler=False)  # Generate LaTeX image
            img = cv2.imread(filename)
            color = [255, 255, 255]  # White background
            top, bottom, left, right = [10] * 4
            # Make image wider
            img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
            cv2.imwrite(filename, img_with_border)

            try:
                await channel.send(file=discord.File(filename))  # Send image to discord
            except discord.errors.HTTPException as e:
                print("Failed: API returned an empty string")
                print(repr(e))
                await channel.send("Failed: API returned an empty string")
        except RuntimeError as e:
            print("Failed: Could not parse the generated LaTeX string")
            print(repr(e))
            await channel.send("Failed: Could not parse the generated LaTeX string")


bot.run(settings['botToken'])

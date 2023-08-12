import discord
import os
from discord.ext import commands , tasks
from facebook_scraper import get_posts
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')



@bot.command()
async def scrape(ctx , first):
    print("scr")
    PAGE_NAME = 'officialroutineofnepalbanda'
    scraped_data = []
    try:
        print("first")
        print(first)
        posts = get_posts(PAGE_NAME, pages=1 , cookies = 'cook.txt') 
        for post in posts:
             if first == '1':
               print("first post")
               text = post.get('text', 'No text available')
               post_image =  post.get('image' , 'image chhaina')
            
               embed=discord.Embed(title="MECHI MMC",  description=text )
               embed.set_image(url = post_image)
               await ctx.send(embed=embed)
               first = '0'
               date_of_post = post.get('time')
             new_date_of_post = post.get('time')

             if new_date_of_post > date_of_post:
              print("old post")
              text = post.get('text', 'No text available')
              post_image =  post.get('image' , 'image chhaina')
              embed=discord.Embed(title="MECHI MMC",  description=text )
              embed.set_image(url = post_image)
              await ctx.send(embed=embed)
              date_of_post = new_date_of_post
             else:
               print("post skipped")




    except Exception as e:
        scraped_data.append(f"An error occurred: {e}")
 
@bot.command()
async def start(ctx ):
    print("ttt")
   
    first = '1'
    i = 0
    
    while True:
        if i == 0:
         await scrape(ctx , '1')
         i =1
        else:
         await scrape(ctx , '0')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
load_dotenv()
bot.run(os.getenv("TOKEN"))



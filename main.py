import discord
import os
from discord.ext import commands, tasks
from facebook_scraper import get_posts
from dotenv import load_dotenv
import asyncio

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

date_of_post =0
first = '1'
# @bot.command()
async def scrape(ctx):
    # scraping logic
    global first
    global date_of_post
    # print("scrape call bhayo")
    PAGE_NAME = "mechimultiplecampus.official"
    scraped_data = []
    

    try:
        # print("first post inside try"+ first)
        posts = get_posts(PAGE_NAME, pages=3, cookies="cook.txt")
        print(posts)
        for post in posts:
            print("inside post loop")
            if first == '1':
                print("first post=" + first)
                text = post.get("text", "No text available")
                post_image = post.get("images", "image chhaina")
                embed = discord.Embed(title= "",description=text)
                embed.set_author(name='Mechi Multiple Campus', url=post['post_url'], icon_url='https://scontent.fktm3-1.fna.fbcdn.net/v/t39.30808-6/359794631_752045040262800_2453124096265258578_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=be3454&_nc_ohc=QRR_QyYZgnMAX97Vs4-&_nc_ht=scontent.fktm3-1.fna&oh=00_AfDP6GzY4O6SAXH63AXMD6XDJSDPED_b0yf59i_g15UNdQ&oe=64DC8E4D')
                for image in post_image:

                    embed.set_image(url=image)
                # await ctx.send("data fetched...")
                await ctx.send(embed=embed)
                # await ctx.send("data should be posted here....")
                date_of_post = post.get("time")
                first= '0'
            else:
                new_date_of_post = post.get("time")
                if new_date_of_post > date_of_post:
                    print("old post ="+ first)
                    text = post.get("text", "No text available")
                    post_image =  post.get("images", "image chhaina")
                    embed = discord.Embed(title="", description=text)
                    embed.set_author(name='Mechi Multiple Campus', url=post['post_url'], icon_url='https://scontent.fktm3-1.fna.fbcdn.net/v/t39.30808-6/359794631_752045040262800_2453124096265258578_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=be3454&_nc_ohc=QRR_QyYZgnMAX97Vs4-&_nc_ht=scontent.fktm3-1.fna&oh=00_AfDP6GzY4O6SAXH63AXMD6XDJSDPED_b0yf59i_g15UNdQ&oe=64DC8E4D')
                    for image in post_image:
                        embed.set_image(url=image)
                    # await ctx.send("data fetched...")
                    await ctx.send(embed=embed)
                    # await ctx.send("data should be posted here....")
                    date_of_post = new_date_of_post
                else:
                    print("post skipped")
                    break

    except Exception as e:
        scraped_data.append(f"An error occurred: {e}")

    
@tasks.loop(seconds=10)  # Adjust the interval as needed
async def scrape_task(ctx):
    await scrape(ctx)
        


@bot.command()
async def start(ctx):
    print("start command called")
    if not scrape_task.is_running():
        await ctx.send("Scraping task started.")
        await scrape_task.start(ctx)
    else:
        await ctx.send("Scraping task is already running.")

@bot.command()
async def stop(ctx):
    if scrape_task.is_running():
        scrape_task.cancel()
        await ctx.send("Scraping task stopped.")
    else:
        await ctx.send("Scraping task is not running.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

load_dotenv()
bot.run(os.getenv("TOKEN"))

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

@bot.command()
async def scrape(ctx):
    # Your scraping logic here
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
            if first == "1":
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

    

first = '1'
@tasks.loop(minutes=5)  # Adjust the interval as needed
async def scrape_task(ctx, channel_id, first_post):
    # Get the channel where you want to send the updates
    channel = bot.get_channel(int(channel_id))

    
    # Your scraping logic here
    global first
    # await ctx.send("scrapping is under scrape_task function")
    # print("first  ko value in  scrape_task"+ first)
    if first=='1':
        await scrape(ctx)
        # print("first = 1 call bhayo")
        first = '0'
    else:
        # print("first 0 bhayo")
        await scrape(ctx)


@bot.command()
async def start(ctx):
    channel_id = 999
    print("channel id = "+channel_id)
    # print("start command called")
    if not scrape_task.is_running():
        first_post = '1'
        await ctx.send("Scraping task started.")
        await scrape_task.start(ctx, channel_id, first_post)
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

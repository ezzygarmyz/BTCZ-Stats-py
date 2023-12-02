import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord import Embed, Intents, Activity, ActivityType, Status, Interaction

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

API_URL = "https://api.coingecko.com/api/v3/coins/bitcoinz"
API_URL0 = "https://k1pool.com/api/stats/btcz"


if TOKEN is None:
    raise ValueError("BOT_TOKEN not found in the environment variables.")


intents = Intents().all()
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    activity = Activity(type=ActivityType.listening, name="To BTCZ")
    await bot.change_presence(status=Status.online, activity=activity),


@bot.command(name="stats")
async def stats(ctx: Interaction):
    
    response = requests.get(API_URL)
    response0 = requests.get(API_URL0)

    if response.status_code == 200:
        data = response.json()
        market_price = data["market_data"]["current_price"]
        market_cap = data["market_data"]["market_cap"]
        market_volume = data["market_data"]["total_volume"]
        price_percentage_24 = data["market_data"]["price_change_percentage_24h"]
        price_percentage_7d = data["market_data"]["price_change_percentage_7d"]
        price_percentage_14d = data["market_data"]["price_change_percentage_14d"]
        market_usd = "{:,}".format(market_cap["usd"])
        volume_24 = "{:,}".format(market_volume["usd"])
        last_updated = data["market_data"]["last_updated"]
        last_updated_datetime = datetime.fromisoformat(last_updated.replace("Z", ""))
        formatted_last_updated = last_updated_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
    if response0.status_code == 200:
        data0 = response0.json()
        network_diff = data0["networkDiff"]
        network_hashrate = data0["networkSpeedStr"]
        
        embed = Embed(
            title="BitcoinZ Stats : Coingecko",
            description=f"",
            color=0x00FF00,  
        )
        embed.add_field(
            name="__Current Price__ :",
            value=f"- **$** `{market_price['usd']}`\n- **€** `{market_price['eur']}`\n- **£** `{market_price['gbp']}`\n- **₽** `{market_price['rub']}`",
            inline=False,
        )
        embed.add_field(
            name="__Network Difficulty__ :", value=f"- `{network_diff}`", inline=False
        )
        embed.add_field(
            name="__Network Hashrate__ :",
            value=f"- `{network_hashrate}` ",
            inline=False,
        )
        embed.add_field(
            name="__Market Cap__ :", value=f"- **$** `{market_usd}`", inline=True
        )
        embed.add_field(
            name="__24H Trading Vol__ :", value=f"- **$** `{volume_24}`", inline=False
        )
        embed.add_field(
            name="__24H percent change__ :",
            value=f"- **%** `{price_percentage_24:.1f}`",
            inline=True,
        )
        embed.add_field(
            name="__7D percent change__ :",
            value=f"- **%** `{price_percentage_7d:.1f}`",
            inline=True,
        )
        embed.add_field(
            name="__14D percent change__ :",
            value=f"- **%** `{price_percentage_14d:.1f}`",
            inline=True,
        )
        embed.set_footer(text=f"Last Update : {formatted_last_updated}")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send(
            "Failed to fetch BitcoinZ stats. Please try again later."
        )


# Run the bot
bot.run(TOKEN)

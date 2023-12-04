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

#Mining Pools API:

TOMARS = "https://btcz.2mars.biz/api/stats"
DARK = "https://btcz.darkfibermines.com/api/stats"
ZERG = "https://zergpool.com/api/currencies"


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
    response2mars = requests.get(TOMARS)
    responsedark = requests.get(DARK)
    responsezerg = requests.get(ZERG)

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
        total_supply = data["market_data"]["total_supply"]
        max_supply = data["market_data"]["max_supply"]
        circulating_supply = data["market_data"]["circulating_supply"]
        sentiment = data["sentiment_votes_up_percentage"]
        last_updated = data["market_data"]["last_updated"]
        last_updated_datetime = datetime.fromisoformat(last_updated.replace("Z", ""))
        formatted_last_updated = last_updated_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        if response0.status_code == 200:
            data0 = response0.json()
            network_diff = data0["networkDiff"]
            network_hashrate = data0["networkSpeedStr"]
            workersk1 = data0["minersTotal"]
        if response2mars.status_code == 200:
            data2mars = response2mars.json()
            workers2mars = data2mars["global"]["workers"]
        
        if responsedark.status_code == 200:
            datadark = responsedark.json()
            workersdark = datadark["global"]["workers"]
        
        if responsezerg.status_code == 200:
            datazerg = responsezerg.json()
            workerszerg = datazerg["BTCZ"]["workers"]
        else:
            workerszerg = 0

        totalworkers = (workersk1 + workersdark + workers2mars + workerszerg)
        
        embed = Embed(
            title="BitcoinZ Stats : [ Coingecko ]",
            description=f"",
            color=0x00FF00,  
        )
        embed.add_field(
            name="\U0001F4B0 __Current Price__ :",
            value=f"- **$ :** `{market_price['usd']}` | **Sats :** `{market_price['sats']:.5f}`"
            f"\n- **€ :** `{market_price['eur']}` | **Ł :** `{market_price['ltc']:.8f}`"
            f"\n- **£ :** `{market_price['gbp']}` | **¥ :** `{market_price['jpy']}`"
            f"\n- **₽ :** `{market_price['rub']}` | **₺ :** `{market_price['try']}`",
            inline=False,
        )
        embed.add_field(
            name="\U0001F525 __Network Difficulty__ :", value=f"- `{network_diff}`", inline=True
        )
        embed.add_field(
            name="\U000026CF __Network Hashrate__ :",
            value=f"- `{network_hashrate}` ",
            inline=True,
        )
        embed.add_field(
            name="\U0001F477 __Total Workers__ :",
            value=f"- `{totalworkers}` ",
            inline=True,
        )
        embed.add_field(
            name="__Market Cap__ :", value=f"- **$** `{market_usd}`", inline=True
        )
        embed.add_field(
            name="__24H Trading Vol__ :", value=f"- **$** `{volume_24}`", inline=True
        )
        embed.add_field(
            name="\U0001F3C5 __Market Rank__ :", value=f"- `{market_rank}`", inline=True
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
        embed.add_field(
            name="__Total Supply__ :",
            value=f"- `{int(total_supply)}`",
            inline=True,
        )
        embed.add_field(
            name="__Max Supply__ :",
            value=f"- `{int(max_supply)}`",
            inline=True,
        )
        embed.add_field(
            name="__Circulating Supply__ :",
            value=f"- `{int(circulating_supply)}`",
            inline=True,
        )
        if sentiment <= 10:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▱▱▱▱▱▱▱▱▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 90:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▰▰▰▰▰▰▰ \U0001F600",
                inline=False,
            )
        elif sentiment >= 80:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▰▰▰▰▰▰▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 70:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▰▰▰▰▰▱▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 60:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▰▰▰▰▱▱▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 50:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▰▰▰▱▱▱▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 40:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▰▰▱▱▱▱▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 30:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▰▱▱▱▱▱▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 20:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▰▱▱▱▱▱▱▱ \U0001F600",
                inline=False,
            )
        elif sentiment >= 10:
            embed.add_field(
                name="__Sentiment__ :",
                value=f"- \U00002639 ▰▰▱▱▱▱▱▱▱▱ \U0001F600",
                inline=False,
            )
        embed.set_footer(text=f"Last Update : {formatted_last_updated}")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send(
            "Failed to fetch BitcoinZ stats. Please try again later."
        )


# Run the bot
bot.run(TOKEN)

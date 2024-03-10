from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
import asyncio
import discord
from discord.ext import commands
import os
import configparser

#region statics
# w3 = Web3(Web3.HTTPProvider('https://json-rpc.evm.shimmer.network'))
w3 = Web3(Web3.AsyncHTTPProvider('https://json-rpc.evm.shimmer.network'), modules={'eth': (AsyncEth,)}, middlewares=[])
cabi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "token0",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "token1",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getReserves",
        "outputs": [
            {
                "internalType": "uint112",
                "name": "_reserve0",
                "type": "uint112"
            },
            {
                "internalType": "uint112",
                "name": "_reserve1",
                "type": "uint112"
            },
            {
                "internalType": "uint32",
                "name": "_blockTimestampLast",
                "type": "uint32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

configpath = 'IOTA/various/evm/treasury_transparency/startup.cfg'
config = configparser.RawConfigParser()
config.read(configpath)

TOKENS = eval(config['watchlist']['tokens'])
LPS = eval(config['watchlist']['lps'])
TREASURYADDRESSES = eval(config['watchlist']['treasuryaddresses'])
LENDTOKENS = eval(config['watchlist']['lendtokens'])
LIMITTOKENS = eval(config['watchlist']['limittokens'])

DISCORDTOKEN = os.getenv('DISCORD_TOKEN')
DISCORDCHANNEL = eval(config['discord']['discordchannel'])
ADMINS = eval(config['discord']['admins'])

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
#endregion

async def output_status(channel):

    embed = discord.Embed(title="Tangle Treasury", url="https://www.tangletreasury.org/", description="Below is a list of all treasury holdings", color=0xFF5733)

    for token in TOKENS.keys():
        if TOKENS[token]['amount'] > 0:
            dec = 1
            if 'formatDec' in TOKENS[token].keys():
                dec = TOKENS[token]['formatDec']
            embed.add_field(name=TOKENS[token]['sym'], value = f'{TOKENS[token]['amount']:.{dec}f}')

    for token, pair in LPS.items():
        if pair['tok0amount'] > 0:
            embed.add_field(name=pair['name'], value='', inline=False)
            dec = 1
            if 'formatDec' in TOKENS[pair['tok0']].keys():
                dec = TOKENS[pair['tok0']]['formatDec']
            embed.add_field(name=TOKENS[pair['tok0']]['name'], value = f'{pair['tok0amount']:.{dec}f}')
            dec = 1
            if 'formatDec' in TOKENS[pair['tok1']].keys():
                dec = TOKENS[pair['tok1']]['formatDec']
            embed.add_field(name=TOKENS[pair['tok1']]['name'], value = f'{pair['tok1amount']:.{dec}f}')
    embed.set_footer(text='')
    await channel.send(embed=embed)
    
async def update_status():
    needsUpdate = False
    for id, value in TOKENS.items():
        try:
            contract = w3.eth.contract(abi=cabi, address=id)
            decimals = await contract.functions.decimals().call()
            amount = 0
            for address in TREASURYADDRESSES:
                amount += await contract.functions.balanceOf(address).call() * 10**-decimals
            if 'sym' not in value.keys():
                value['sym'] = await contract.functions.symbol().call()
            if amount != TOKENS[id]['amount']:
                needsUpdate = True
                TOKENS[id]['amount'] = amount
        except:
            pass

    for id, pair in LPS.items():
        try:
            contract = w3.eth.contract(abi=cabi, address=id)
            total = await contract.functions.totalSupply().call()
            reserves = await contract.functions.getReserves().call()
            tok0 = await contract.functions.token0().call()
            tok1 = await contract.functions.token1().call()
            tok0Contract = w3.eth.contract(abi=cabi, address = tok0)
            tok1Contract = w3.eth.contract(abi=cabi, address = tok1)
            decimals0 = await tok0Contract.functions.decimals().call()
            decimals1 = await tok1Contract.functions.decimals().call()
            if 'tok0' not in pair.keys():
                pair['tok0'] = tok0
            if 'tok1' not in pair.keys():
                pair['tok1'] = tok1

            if tok0 not in TOKENS.keys():
                TOKENS[tok0] = {
                    'amount': 0,
                    'formatDec': 2
                }
            if tok1 not in TOKENS.keys():
                TOKENS[tok1] = {
                    'amount': 0,
                    'formatDec': 2
                }

            bal = 0
            for address in TREASURYADDRESSES:
                bal += await contract.functions.balanceOf(address).call() 

            share = bal / total 
            if bal != pair['amount']:
                needsUpdate = True
                pair['amount'] = bal
                
            LPS[id]['tok0amount'] = reserves[0] * share * 10**-decimals0
            LPS[id]['tok1amount'] = reserves[1] * share * 10**-decimals1
        except:
            pass

    return needsUpdate

async def update_thread():
    await asyncio.sleep(3)
    channel = bot.get_channel(DISCORDCHANNEL)
    while True: 
        if await update_status():
            await output_status(channel)
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def addtoken(ctx, *args):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        try:
            if len(args) >= 2:
                TOKENS[args[0]]={'amount':0}
            if len(args) > 2:
                TOKENS[args[0]]['formatDec'] = args[1]
            config.set('watchlist', 'tokens', TOKENS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def deltoken(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        try:
            del TOKENS[arg]
            config.set('watchlist', 'tokens', TOKENS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addlp(ctx, *args):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        try:
            if len(args) > 1:
                LPS[args[0]]={'name': ' '.join(args[1:]), 'amount':0, 'tok0amount': 0,'tok1amount': 0}
            config.set('watchlist', 'lps', LPS)
            
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def dellp(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        try:
            del LPS[arg]
            config.set('watchlist', 'lps', LPS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addwallet(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        try:
            TREASURYADDRESSES.append(arg)
            config.set('watchlist', 'treasuryaddresses', TREASURYADDRESSES)

            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def delwallet(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        try:
            TREASURYADDRESSES.remove(arg)

            config.set('watchlist', 'treasuryaddresses', TREASURYADDRESSES)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def update(ctx):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        try:
            await update_status()
            await output_status(ctx.message.channel)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addlending(ctx, *args):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        await ctx.message.add_reaction('⛔')

@bot.command()
async def addlimit(ctx, *args):
    if ctx.author.id in ADMINS and ctx.channel.id == DISCORDCHANNEL:
        await ctx.message.add_reaction('⛔')   

async def main():
    asyncio.create_task(update_thread())
    await bot.start(DISCORDTOKEN)

if __name__ == "__main__":
    asyncio.run(main()) 
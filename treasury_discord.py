from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
import asyncio
import discord
from discord.ext import commands
import os
import configparser
import aiohttp
import time
from iota_sdk import Client, NodeIndexerAPI, Utils
import json
from datetime import datetime

#region statics
w3 = Web3(AsyncHTTPProvider('https://json-rpc.evm.shimmer.network'), modules={'eth': (AsyncEth,)}, middlewares=[])
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
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "getPrincipalByTokenId",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amount0",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amount1",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
        {
            "internalType": "uint256",
            "name": "tokenId",
            "type": "uint256"
        }
        ],
        "name": "positions",
        "outputs": [
        {
            "internalType": "uint96",
            "name": "nonce",
            "type": "uint96"
        },
        {
            "internalType": "address",
            "name": "operator",
            "type": "address"
        },
        {
            "internalType": "address",
            "name": "token0",
            "type": "address"
        },
        {
            "internalType": "address",
            "name": "token1",
            "type": "address"
        },
        {
            "internalType": "uint24",
            "name": "fee",
            "type": "uint24"
        },
        {
            "internalType": "int24",
            "name": "tickLower",
            "type": "int24"
        },
        {
            "internalType": "int24",
            "name": "tickUpper",
            "type": "int24"
        },
        {
            "internalType": "uint128",
            "name": "liquidity",
            "type": "uint128"
        },
        {
            "internalType": "uint256",
            "name": "feeGrowthInside0LastX128",
            "type": "uint256"
        },
        {
            "internalType": "uint256",
            "name": "feeGrowthInside1LastX128",
            "type": "uint256"
        },
        {
            "internalType": "uint128",
            "name": "tokensOwed0",
            "type": "uint128"
        },
        {
            "internalType": "uint128",
            "name": "tokensOwed1",
            "type": "uint128"
        }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "fee",
        "outputs": [
            {
                "internalType": "uint24",
                "name": "",
                "type": "uint24"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "poolInfo",
        "outputs": [
            {
                "internalType": "contract IERC20",
                "name": "lpToken",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "lpSupply",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "allocPoint",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "lastRewardTime",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "accRewardPerShare",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "depositFeeBP",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "userInfo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "rewardDebt",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "underlying",
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
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "balanceOfUnderlying",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs":[],
        "name":"getTokenX",
        "outputs":[
                {
                    "internalType":"contract IERC20","name":"","type":"address"
                }
            ],
        "stateMutability":"view","type":"function"
    },
    {
        "inputs":[],
        "name":"getTokenY",
        "outputs":[
            {
                "internalType":"contract IERC20","name":"","type":"address"
            }
        ],
        "stateMutability":"view","type":"function"
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
        "name": "stakeAmount0",
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
    },
    {
        "inputs":[
            {
                "internalType":"address",
                "name":"owner",
                "type":"address"
            },
            {
                "internalType":"uint256",
                "name":"index",
                "type":"uint256"
            }
        ],
        "name":"tokenOfOwnerByIndex",
        "outputs":
        [
            {
                "internalType":"uint256",
                "name":"",
                "type":"uint256"
            }
        ],
        "stateMutability":"view",
        "type":"function"
    }
]

path = ''
# path = 'IOTA/various/evm/treasury_transparency/'
configpath = path+'startup.cfg'

config = configparser.RawConfigParser()
config.read(configpath)

TOKENS = eval(config["watchlist"]["tokens"])
LPSV2 = eval(config["watchlist"]["lpsv2"])
TREASURYADDRESSES = eval(config["watchlist"]["treasuryaddresses"])
DEEPR = eval(config["watchlist"]["deepr"])
SWAPLINE = eval(config["watchlist"]["swapline"])
TANGLESWAP = eval(config["watchlist"]["tangleswap"])
TANGLEHELPER = eval(config["watchlist"]["tanglehelper"])
FARMS = eval(config["watchlist"]["farms"])
TANGLESWAP = eval(config["watchlist"]["tangleswap"])
IOTABEE = eval(config["watchlist"]["iotabee"])
IOTABEEPOSADDR = eval(config["watchlist"]["iotabeeposaddr"])

DISCORDTOKEN = os.getenv('DISCORD_TOKEN')
ADMINCHANNELS = eval(config["discord"]["adminchannels"])
TREASURYCHANNELS = eval(config["discord"]["treasurychannels"])
PCHANNELS = eval(config["discord"]["pchannels"])
VFREQUENCY = eval(config["discord"]["vfrequency"])
ADMINS = eval(config["discord"]["admins"])
SUPERUSER = eval(config["discord"]["superuser"])

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

iota = {
    'price': 0,
    'price1h': 0,
    'price24h': 0,
    'mc': 0,
    'rank': 0,
    'watchlists': 0,
    'sentimentUP': 0,
    'sentimentDOWN': 0,
    'twitter': 0,
    'circulating': 0,
    'supply': 0
}
smr = {
    'price': 0,
    'price1h': 0,
    'price24h': 0,
    'mc': 0,
    'rank': 0,
    'watchlists': 0,
    'sentimentUP': 0,
    'sentimentDOWN': 0,
    'twitter':0,
    'circulating': 0,
    'supply': 0
}

ptime = 0
vtime = 0

EVENTS = {}
VOTINGS = {'SMR' : {},
           'IOTA': {}
        }
KNOWNWALLETS = {}


#endregion

def smr_to_iota(addr):
    byt = Utils.bech32_to_hex(addr)
    smr = Utils.hex_to_bech32(byt, 'iota')
    return smr

def iota_to_smr(addr):
    byt = Utils.bech32_to_hex(addr)
    smr = Utils.hex_to_bech32(byt, 'smr')
    return smr

def parse_vote(hex_str):
    participation_bytes = bytearray.fromhex(hex_str[2:])
    participations_len = participation_bytes.pop(0)
    participations = {}

    for i in range(participations_len):
        event_id = '0x'+participation_bytes[:32].hex()
        del participation_bytes[:32]
        answers_len = participation_bytes.pop(0)
        answers = []
        for i in range(answers_len):
            answer =participation_bytes.pop(0)
            answers.append(answer)

        participations[event_id] = answers

    return participations

# async def update_voting():
#     await asyncio.sleep(5)
#     client_smr = Client(nodes= ["https://api.shimmer.network"])
#     client_iota = Client(nodes= ["https://iota-node.tanglebay.com"])

#     while True:
#         try:
#             events = {
#                 '69194943b788eb67bfd3b1e258041af1cbb8f501489c5d826e6cd970cfaf01eb': {0: {0:['Yes',0], 1: ['No',0], 2: ['Abstain',0]}},
#                 '0a2e8afc01146f6283233e7d69fbd1a7455078f239fd33a22c05bf2c529ed633': {0: {0:['Yes',0], 1: ['No',0], 2: ['Abstain',0]}}
#             }
            
#             evs = []

#             all_addr_smr = {}
#             all_addr_iota = {}

#             query_parameters = NodeIndexerAPI.QueryParameters(
#             tag='0x'+b'PARTICIPATE'.hex(),
#             created_after=1710111420
#             )
#             output_ids_smr = client_smr.basic_output_ids(query_parameters).items
#             outputs_smr = client_smr.get_outputs(output_ids_smr)

#             output_ids_iota = client_iota.basic_output_ids(query_parameters).items
#             outputs_iota = client_iota.get_outputs(output_ids_iota)

#             for o in outputs_smr:
#                 addr_hash = o.output.unlockConditions[0].address.pubKeyHash
#                 #addr = client.hex_to_bech32(addr_hash, 'smr')
#                 addr = Utils.hex_to_bech32(addr_hash, 'smr')
            
#                 features = o.output.features
#                 weight = int(o.output.amount)
#                 txid = o.metadata.transactionId
#                 for f in features:
#                     if f.type == 2:
#                         data = f.data[2:]
#                         num = int(data[:2], 16)
#                         data = data[2:]
#                         for i in range(num):
#                             eventid = data[:32*2]
#                             if eventid not in evs:
#                                 evs.append(eventid)
                        
#                             data = data[32*2:]
#                             answercount = int(data[:2], 16)
#                             data = data[2:]
#                             answers = data[:answercount*2]
#                             data = data[answercount*2:]
#                             if eventid in events:
#                                 for j in range(answercount):
#                                     answ = int(answers[j*2:j*2+2],16)
#                                     events[eventid][j][(answ-1) % len(events[eventid][j])][1]+=weight

#                                 all_addr_smr[addr] = [datetime.fromtimestamp(o.metadata.milestoneTimestampBooked).strftime("%m/%d/%Y, %H:%M:%S"), weight, events[eventid][j][(answ-1) % len(events[eventid][j])][0]]

    
#             for o in outputs_iota:
#                 addr_hash = o.output.unlockConditions[0].address.pubKeyHash
#                 #addr = client.hex_to_bech32(addr_hash, 'smr')
#                 addr = Utils.hex_to_bech32(addr_hash, 'iota')
            
#                 features = o.output.features
#                 weight = int(o.output.amount)
#                 txid = o.metadata.transactionId
#                 for f in features:
#                     if f.type == 2:
#                         data = f.data[2:]
#                         num = int(data[:2], 16)
#                         data = data[2:]
#                         for i in range(num):
#                             eventid = data[:32*2]
#                             if eventid not in evs:
#                                 evs.append(eventid)
                        
#                             data = data[32*2:]
#                             answercount = int(data[:2], 16)
#                             data = data[2:]
#                             answers = data[:answercount*2]
#                             data = data[answercount*2:]
#                             if eventid in events:
#                                 for j in range(answercount):
#                                     answ = int(answers[j*2:j*2+2],16)
#                                     events[eventid][j][(answ-1) % len(events[eventid][j])][1]+=weight

#                                 all_addr_iota[addr] = [datetime.fromtimestamp(o.metadata.milestoneTimestampBooked).strftime("%m/%d/%Y, %H:%M:%S"), weight, events[eventid][j][(answ-1) % len(events[eventid][j])][0]]

#             with open(path+'addr_smr.json', 'w') as fp:
#                 json.dump(all_addr_smr, fp, indent=2)

#             with open(path+'addr_iota.json', 'w') as fp:
#                 json.dump(all_addr_iota, fp, indent=2)

#             with open(path+'events.json', 'w') as fp:
#                 json.dump(events, fp, indent=2)

#         except Exception as e:
#             pass
#         await asyncio.sleep(VFREQUENCY)

async def update_votings():
    smr_node = "https://api.shimmer.network"
    iota_node = "https://iota-node.tanglebay.com"
    part_endpoint = '/api/participation/v1/events'

    client_smr = Client(nodes= [smr_node])
    client_iota = Client(nodes= [iota_node])

    while True:
        try:
            async with session.get(smr_node+part_endpoint, timeout=5) as resp:
                smreventids = (await resp.json())['eventIds']
            async with session.get(iota_node+part_endpoint, timeout=5) as resp:
                iotaeventids =(await resp.json())['eventIds']


            pullSmrOuts = False
            pullSmrMilestone = 9999999999999999999
            #smrMileStone = client_smr.get_info().nodeInfo.status.confirmedMilestone.index
            for id in [s for s in smreventids if s not in EVENTS]:
                async with session.get(smr_node+part_endpoint+'/'+id, timeout=5) as resp:
                    EVENTS[id] = await resp.json()
                async with session.get(smr_node+part_endpoint+'/'+id+'/status', timeout=5) as resp:
                    status = await resp.json()
                    EVENTS[id]['status'] = status['status']
                    if status['status']=='commencing' or status['status']=='holding':
                        pullSmrOuts = True
                        pullSmrMilestone = min(pullSmrMilestone, EVENTS[id]['milestoneIndexCommence'])
                    for i in range(len(status['questions'])):
                        for j in range(len(status['questions'][i]['answers'])):
                            if j < len(EVENTS[id]['payload']['questions'][i]['answers']):
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['current'] = status['questions'][i]['answers'][j]['current']
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['accumulated'] = status['questions'][i]['answers'][j]['accumulated']
                            elif status['questions'][i]['answers'][j]['value'] == 0:
                                EVENTS[id]['payload']['questions'][i]['answers'].append(status['questions'][i]['answers'][j])
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['text'] = 'Abstain'

                    
            pullIotaOuts = False
            pullIotaMilestone = 9999999999999999999
            for id in [s for s in iotaeventids if s not in EVENTS]:
                async with session.get(iota_node+part_endpoint+'/'+id, timeout=5) as resp:
                    EVENTS[id] = await resp.json()
                async with session.get(iota_node+part_endpoint+'/'+id+'/status', timeout=5) as resp:
                    status = await resp.json()
                    EVENTS[id]['status'] = status['status']
                    if status['status']=='commencing' or status['status']=='holding':
                        pullIotaOuts = True
                        pullIotaMilestone = min(pullIotaMilestone, EVENTS[id]['milestoneIndexCommence'])
                    for i in range(len(status['questions'])):
                        for j in range(len(status['questions'][i]['answers'])):
                            if j < len(EVENTS[id]['payload']['questions'][i]['answers']):
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['current'] = status['questions'][i]['answers'][j]['current']
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['accumulated'] = status['questions'][i]['answers'][j]['accumulated']
                            elif status['questions'][i]['answers'][j]['value'] == 0:
                                EVENTS[id]['payload']['questions'][i]['answers'].append(status['questions'][i]['answers'][j])
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['text'] = 'Abstain'

            if pullSmrOuts:
                milestone = client_smr.get_milestone_by_index(pullSmrMilestone)
                qp = NodeIndexerAPI.QueryParameters(
                    tag='0x'+b'PARTICIPATE'.hex(),
                    created_after=milestone.timestamp
                )
                output_ids_smr = client_smr.basic_output_ids(qp).items
                outputs_smr = client_smr.get_outputs(output_ids_smr)
                for o in outputs_smr:
                    addr = Utils.hex_to_bech32(o.output.unlockConditions[0].address.pubKeyHash, 'smr')
                    features = o.output.features
                    weight = int(o.output.amount)
                    for f in features:
                        if f.type == 2:
                            for eventid, votes in parse_vote(f.data).items():
                                if eventid not in VOTINGS['SMR']:
                                    VOTINGS['SMR'][eventid] = []
                                answers = []
                                for i in range(len(votes)):
                                    answer = [e['text'] for e in EVENTS[eventid]['payload']['questions'][i]['answers'] if e['value']==votes[i]]
                                    if answer:
                                        answers.append(answer[0])
                                    else:
                                        answers.append('No')

                                VOTINGS['SMR'][eventid].append([addr, datetime.fromtimestamp(o.metadata.milestoneTimestampBooked).strftime("%m/%d/%Y, %H:%M:%S"), weight, answers])

            if pullIotaOuts:
                milestone = client_iota.get_milestone_by_index(pullIotaMilestone)
                qp = NodeIndexerAPI.QueryParameters(
                    tag='0x'+b'PARTICIPATE'.hex(),
                    created_after=milestone.timestamp
                )
                output_ids_iota = client_iota.basic_output_ids(qp).items
                outputs_iota = client_iota.get_outputs(output_ids_iota)
                for o in outputs_iota:
                    addr = Utils.hex_to_bech32(o.output.unlockConditions[0].address.pubKeyHash, 'iota')
                    features = o.output.features
                    weight = int(o.output.amount)
                    for f in features:
                        if f.type == 2:
                            for eventid, votes in parse_vote(f.data).items():
                                if eventid not in VOTINGS['IOTA']:
                                    VOTINGS['IOTA'][eventid] = []
                                answers = []
                                for i in range(len(votes)):
                                    answer = [e['text'] for e in EVENTS[eventid]['payload']['questions'][i]['answers'] if e['value']==votes[i]]
                                    if answer:
                                        answers.append(answer[0])
                                    else:
                                        answers.append('No')

                                VOTINGS['IOTA'][eventid].append([addr, datetime.fromtimestamp(o.metadata.milestoneTimestampBooked).strftime("%m/%d/%Y, %H:%M:%S"), weight, answers])

        except Exception as e:
            pass
        await asyncio.sleep(VFREQUENCY)

async def update_price():
    iota_url = 'https://api.coingecko.com/api/v3/coins/iota?localization=false&tickers=false&market_data=true&community_data=true&developer_data=false'
    smr_url = 'https://api.coingecko.com/api/v3/coins/shimmer?localization=false&tickers=false&market_data=true&community_data=true&developer_data=false'
    while True:
        try:
            async with session.get(iota_url, timeout=5) as resp:
                iotarsp = await resp.json()
                iota["sentimentUP"] = iotarsp["sentiment_votes_up_percentage"]
                iota["sentimentDOWN"] = iotarsp["sentiment_votes_down_percentage"]
                iota["twitter"] = iotarsp["community_data"]["twitter_followers"]
                iota["price"] = iotarsp["market_data"]["current_price"]["usd"]
                iota["price1h"] = iotarsp["market_data"]["price_change_percentage_1h_in_currency"]["usd"]
                iota["price24h"] = iotarsp["market_data"]["price_change_percentage_24h_in_currency"]["usd"]
                iota["mc"] = iotarsp["market_data"]["market_cap"]["usd"]
                iota["rank"] = iotarsp["market_data"]["market_cap_rank"]
                iota["supply"] = iotarsp["market_data"]["total_supply"]
                iota["circulating"] = iotarsp["market_data"]["circulating_supply"]

            async with session.get(smr_url, timeout=5) as resp:
                smrrsp = await resp.json()
                smr["sentimentUP"] = smrrsp["sentiment_votes_up_percentage"]
                smr["sentimentDOWN"] = smrrsp["sentiment_votes_down_percentage"]
                smr["twitter"] = smrrsp["community_data"]["twitter_followers"]
                smr["price"] = smrrsp["market_data"]["current_price"]["usd"]
                smr["price1h"] = smrrsp["market_data"]["price_change_percentage_1h_in_currency"]["usd"]
                smr["price24h"] = smrrsp["market_data"]["price_change_percentage_24h_in_currency"]["usd"]
                smr["mc"] = max(smrrsp["market_data"]["market_cap"]["usd"], smr["price"] * 1813620509)
                smr["rank"] = smrrsp["market_data"]["market_cap_rank"]
                smr["watchlists"] = smrrsp["watchlist_portfolio_users"]
                smr["supply"] = smrrsp["market_data"]["total_supply"]
                smr["circulating"] = max(smrrsp["market_data"]["circulating_supply"], smr["supply"])

        except:
            pass
        await asyncio.sleep(60)
    pass

async def output_status(channel):

    #embed = discord.Embed(title="Tangle Treasury", url="https://www.tangletreasury.org/", description="Treasury ERC-20 and LP Tokens:", color=0xFF5733)
    embed = discord.Embed()
    #embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url='https://cdn.discordapp.com/avatars/1216381699122921572/2935a67fc7f656c5d1c575e9f42b2c08.png?size=256')
    #embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240")
    embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url='https://cdn.discordapp.com/attachments/1108370354319147051/1218224680905998468/image.png?ex=6606e325&is=65f46e25&hm=3e1cdf04c7f02a93e5224f5edfdcf16154a2c803507730f27d9d4a839db167e5')

    embed.add_field(name='__Tokens on ShimmerEVM:__', value='', inline=False)
    for token in TOKENS.keys():
        if TOKENS[token]["amount"] > 0:
            dec = 1
            if 'formatDec' in TOKENS[token].keys():
                dec = TOKENS[token]["formatDec"]
            embed.add_field(name=TOKENS[token]["sym"], value = f'{TOKENS[token]["amount"]:,.{dec}f}'.rstrip('0').rstrip('.'))

    embed.add_field(name='__Shimmersea:__', value='', inline=False)
    for pool, pair in LPSV2.items():
        if pair["tok0amount"] > 0:
            # embed.add_field(name=pair["name"]+':', value='', inline=False)
            dec1 = 1
            if 'formatDec' in TOKENS[pair["tok0"]].keys():
                dec1 = TOKENS[pair["tok0"]]["formatDec"]
            # embed.add_field(name=TOKENS[pair["tok0"]]["sym"], value = f'{pair["tok0amount"]:,.{dec}f}')
            dec2 = 1
            if 'formatDec' in TOKENS[pair["tok1"]].keys():
                dec2 = TOKENS[pair["tok1"]]["formatDec"]
            tok0string = f'{pair["tok0amount"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            tok1string = f'{pair["tok1amount"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["tok0"]]["sym"]}-{TOKENS[pair["tok1"]]["sym"]}', value = f'{tok0string}-{tok1string}')
    #embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png")

    embed.add_field(name='__IOTABee:__', value='', inline=False)
    for id, pair in IOTABEE.items():
        if pair["amount"] > 0:
            # embed.add_field(name=pair["name"]+':', value='', inline=False)

            dec1 = 1
            if 'formatDec' in TOKENS[pair["X"]].keys():
                dec1 = TOKENS[pair["X"]]["formatDec"]
            # embed.add_field(name=TOKENS[pair["X"]]["sym"], value = f'{pair["depositX"]:,.{dec}f}')
        

            dec2 = 1
            if 'formatDec' in TOKENS[pair["Y"]].keys():
                dec2 = TOKENS[pair["Y"]]["formatDec"]
            # embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{pair["depositX"]:,.{dec1}f}-{pair["depositY"]:,.{dec2}f}')
            Xstring = f'{pair["depositX"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            Ystring = f'{pair["depositY"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{Xstring}-{Ystring}')
    
    await channel.send(embed=embed)

    #embed = discord.Embed(title="Tangle Treasury", url="https://www.tangletreasury.org/", description="Treasury Limit Order and Lend Tokens:", color=0xFF5733)
    embed = discord.Embed()
    #embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240")
    # embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url='https://cdn.discordapp.com/avatars/1216381699122921572/2935a67fc7f656c5d1c575e9f42b2c08.png?size=256')
    embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url='https://cdn.discordapp.com/attachments/1108370354319147051/1218224680905998468/image.png?ex=6606e325&is=65f46e25&hm=3e1cdf04c7f02a93e5224f5edfdcf16154a2c803507730f27d9d4a839db167e5')

    #embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png")
    embed.add_field(name='__Swapline:__', value='', inline=False)
    for pool, pair in SWAPLINE.items():
        if pair["depositX"] + pair["depositY"] > 0:
            # embed.add_field(name=pair["name"]+':', value='', inline=False)

            dec1 = 1
            if 'formatDec' in TOKENS[pair["X"]].keys():
                dec1 = TOKENS[pair["X"]]["formatDec"]
            # embed.add_field(name=TOKENS[pair["X"]]["sym"], value = f'{pair["depositX"]:,.{dec}f}')
        

            dec2 = 1
            if 'formatDec' in TOKENS[pair["Y"]].keys():
                dec2 = TOKENS[pair["Y"]]["formatDec"]
            #embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{pair["depositX"]:,.{dec1}f}-{pair["depositY"]:,.{dec2}f}')
            Xstring = f'{pair["depositX"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            Ystring = f'{pair["depositY"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{Xstring}-{Ystring}')
    
    embed.add_field(name='__TangleSwap:__', value='', inline=False)
    for pool, pair in TANGLESWAP.items():
        if pair["amount"] > 0:
            # embed.add_field(name=pair["name"]+':', value='', inline=False)

            dec1 = 1
            if 'formatDec' in TOKENS[pair["X"]].keys():
                dec1 = TOKENS[pair["X"]]["formatDec"]
            # embed.add_field(name=TOKENS[pair["X"]]["sym"], value = f'{pair["depositX"]:,.{dec}f}')
        

            dec2 = 1
            if 'formatDec' in TOKENS[pair["Y"]].keys():
                dec2 = TOKENS[pair["Y"]]["formatDec"]
            # embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{pair["depositX"]:,.{dec1}f}-{pair["depositY"]:,.{dec2}f}')
            Xstring = f'{pair["depositX"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            Ystring = f'{pair["depositY"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{Xstring}-{Ystring}')
    
    
    embed.add_field(name='__DeepR:__', value='', inline=False)
    for pool, token in DEEPR.items():
        if token["amount"] > 0:
            #embed.add_field(name=token["name"]+':', value='', inline=False)
            dec = 1
            if 'formatDec' in TOKENS[token["token"]].keys():
                dec = TOKENS[token["token"]]["formatDec"]
            embed.add_field(name=TOKENS[token["token"]]["sym"], value = f'{token["amount"]:,.{dec}f}'.rstrip('0').rstrip('.'))
            
    #embed.set_footer(text='footers are overrated')
    await channel.send(embed=embed)

async def update_thread():
    await asyncio.sleep(3)
    channels = []
    for chan in TREASURYCHANNELS:
        channels.append(bot.get_channel(chan))
    while True: 
        if await update_status():
            config.set('watchlist', 'lendtokens', DEEPR)
            config.set('watchlist', 'tokens', TOKENS)
            config.set('watchlist', 'lpsv2', LPSV2)
            config.set('watchlist', 'swapline', SWAPLINE)
            config.set('watchlist', 'treasuryaddresses', TREASURYADDRESSES)
            config.set('watchlist', 'farms', FARMS)
            config.set('watchlist', 'tangleswap', TANGLESWAP)
            config.set('watchlist', 'iotabee', IOTABEE)
            with open(configpath, 'w') as configfile:
                config.write(configfile)

            for c in channels:
                try:
                    await output_status(c)
                except:
                    pass
        await asyncio.sleep(60*60*24)
   
async def update_status():
    upFarms = await update_farms() #run first
    upLP = await update_univ2()
    upSwap = await update_swapline()
    upTangle = await update_tangleswap()
    upBee = await update_univ3()
    upLend = await update_lending()
    upTok = await update_tokens()
    upLum = await update_lum()
    return upFarms or upTok or upLP or upTangle or upBee or upSwap  or upLend or upLum

async def update_tokens():
    needsUpdate = False
    for id, value in TOKENS.items():
        try:
            contract = w3.eth.contract(abi=cabi, address=id)
            decimals = await contract.functions.decimals().call()
            amount = 0
            for address in TREASURYADDRESSES:
                amount += await contract.functions.balanceOf(address).call() * 10**-decimals
            if 'sym' not in value.keys():
                value["sym"] = await contract.functions.symbol().call()

            if abs(max(amount, 0.000000000000001)/max(TOKENS[id]["amount"], 0.000000000000001)-1) > 0.01:
                needsUpdate = True
            TOKENS[id]["amount"] = amount
        except:
            pass
    return needsUpdate

async def update_univ2():
    needsUpdate = False
    for id, pair in LPSV2.items():
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
                pair["tok0"] = tok0
            if 'tok1' not in pair.keys():
                pair["tok1"] = tok1

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
            farms = []
            for f in FARMS.values():
                for i in range(len(f)):
                    if f[i]["poolID"]==id:
                        farms.append(f[i])
            for f in farms:
                bal += f["amount"]
            share = bal / total 
            
            if abs(max(bal, 0.000000000000001)/max(pair["amount"], 0.000000000000001)-1) > 0.01:
                needsUpdate = True
            
            pair["amount"] = bal
            LPSV2[id]["tok0amount"] = reserves[0] * share * 10**-decimals0
            LPSV2[id]["tok1amount"] = reserves[1] * share * 10**-decimals1
        except:
            pass
    return needsUpdate

async def update_swapline():
    needsUpdate = False
    for address in TREASURYADDRESSES:
        try:
            async with session.get('https://api-c.swapline.com/api/v1/user-positions/'+address, timeout=5) as resp:
                positions = await resp.json()
                for p in positions:
                    amount = sum([float(l["amountXRaw"]+l["amountYRaw"]) for l in p["userBinLiquidities"]])
                    pair = Web3.to_checksum_address(p["pairAddress"])
             
                    if pair not in SWAPLINE:
                        contract = w3.eth.contract(abi=cabi, address=pair)
                        X = await contract.functions.getTokenX().call()
                        Y = await contract.functions.getTokenY().call()
                        tokXContract = w3.eth.contract(abi=cabi, address = X)
                        tokYContract = w3.eth.contract(abi=cabi, address = Y)
                        
                        if X not in TOKENS:
                            xsym = await tokXContract.functions.symbol().call()
                            TOKENS[X] = {
                                'amount': 0,
                                'formatDec': 2,
                                'sym': xsym
                            }
                        if Y not in TOKENS:
                            ysym = await tokYContract.functions.symbol().call()
                            TOKENS[Y] = {
                                'amount': 0,
                                'formatDec': 2,
                                'sym': ysym
                            }
                    
                        name = f'Swapline {TOKENS[X]["sym"]}-{TOKENS[Y]["sym"]}'
                        SWAPLINE[pair] = {'name': name, 'amount': 0, 'depositX': 0.0, 'depositY': 0.0, 'X': X, 'Y': Y}
                    
                    if abs(max(amount, 0.000000000000001)/max(SWAPLINE[pair]["amount"], 0.000000000000001)-1) > 0.01:
                        needsUpdate = True
                    SWAPLINE[pair]["amount"] = amount

                    SWAPLINE[pair]["depositX"] = p["depositX"]
                    SWAPLINE[pair]["depositY"] = p["depositY"]
                pass    
        except Exception as e:
            pass
    return needsUpdate

async def update_lending():
    needsUpdate = False
    for id, value in DEEPR.items():
        try:
            contract = w3.eth.contract(abi=cabi, address=id)
            underlying = await contract.functions.underlying().call()
            if underlying not in TOKENS:
                sym = await underlying.functions.symbol().call()
                TOKENS[underlying] = {
                    'amount': 0,
                    'formatDec': 2,
                    'sym': sym
                }
                needsUpdate = True
            ucontract = w3.eth.contract(abi=cabi, address=underlying)
            decimals = await ucontract.functions.decimals().call()
            amount = 0
            for address in TREASURYADDRESSES:
                amount += await contract.functions.balanceOfUnderlying(address).call() * 10**-decimals

            if abs(max(amount, 0.000000000000001)/max(DEEPR[id]["amount"], 0.000000000000001)-1) > 0.01:
                needsUpdate = True
            DEEPR[id]["amount"] = amount
        except:
            pass
    return needsUpdate

async def update_farms():
    needsUpdate = False
    for id, value in FARMS.items():
        try:
            contract = w3.eth.contract(abi=cabi, address=id)
            length = await contract.functions.poolLength().call()

            for i in range(length):
                if i not in value.keys():
                    value[i] = {'amount': 0}

                if 'poolID' not in value[i].keys():
                    poolID = (await contract.functions.poolInfo(i).call())[0]
                    value[i]["poolID"] = poolID
                amount = 0
                for address in TREASURYADDRESSES:
                    amount += (await contract.functions.userInfo(i, address).call())[0]

                if abs(max(amount, 0.000000000000001)/max(FARMS[id][i]["amount"], 0.000000000000001)-1) > 0.01:
                    needsUpdate = True
                
                FARMS[id][i]["amount"] = amount
        except:
            pass
    return needsUpdate

async def update_lum():
    pass

async def update_tangleswap():
    needsUpdate = False
    for address in TREASURYADDRESSES:
        try:
            async with session.get('https://backend.tangleswap.space/api/v1/chains/148/wallet/'+address+'/positions', timeout=5) as resp:
                positions = await resp.json()
                for p in positions:
                    amount = int(p["liquidity"])
                    pair = Web3.to_checksum_address(p["poolAddress"])
                    pid = pair+str(p["id"])
             
                    
                    X = Web3.to_checksum_address(p["token0Address"])
                    Y = Web3.to_checksum_address(p["token1Address"])
                    tokXContract = w3.eth.contract(abi=cabi, address = X)
                    tokYContract = w3.eth.contract(abi=cabi, address = Y)
                    decimals0 = await tokXContract.functions.decimals().call()
                    decimals1 = await tokYContract.functions.decimals().call()

                    if X not in TOKENS:
                        xsym = await tokXContract.functions.symbol().call()
                        TOKENS[X] = {
                            'amount': 0,
                            'formatDec': 2,
                            'sym': xsym
                        }
                        needsUpdate = True
                    if Y not in TOKENS:
                        ysym = await tokYContract.functions.symbol().call()
                        TOKENS[Y] = {
                            'amount': 0,
                            'formatDec': 2,
                            'sym': ysym
                        }
                        needsUpdate = True
                    
                    if pid not in TANGLESWAP: 
                        name = f'Tangleswap {TOKENS[X]["sym"]}-{TOKENS[Y]["sym"]}'
                        TANGLESWAP[pid] = {'name': name, 'amount': 0, 'depositX': 0.0, 'depositY': 0.0, 'X': X, 'Y': Y}
                        needsUpdate = True

                    if abs(max(amount, 0.000000000000001)/max(TANGLESWAP[pid]["amount"], 0.000000000000001)-1) > 0.01:
                        needsUpdate = True
                    TANGLESWAP[pid]["amount"] = amount
                    

                    hcontract =  w3.eth.contract(abi=cabi, address = TANGLEHELPER)
                    pos = await hcontract.functions.getPrincipalByTokenId(p["id"]).call()
                    
                    TANGLESWAP[pid]["depositX"] = pos[0] * 10**-decimals0
                    TANGLESWAP[pid]["depositY"] = pos[1] * 10**-decimals1
                
                pass    
        except Exception as e:
            pass
    return needsUpdate

async def update_univ3():
    needsUpdate = False

    #blockscout grrrr
    try:
        foundAll = False
        transfers= []
        farm = '0xa2c8B10F8307246B0252090a8073b6a5c04c7Ff0'
        async with session.get('https://explorer.evm.shimmer.network/api/v2/addresses/'+farm+'/token-transfers?type=validated&filter=to', timeout=10) as resp0:
            transfers.append(await resp0.json())
        blocknumber = transfers[-1]['next_page_params']['block_number']
        index =  transfers[-1]['next_page_params']['index']
        while not foundAll:
            async with session.get('https://explorer.evm.shimmer.network/api/v2/addresses/0xa2c8B10F8307246B0252090a8073b6a5c04c7Ff0/token-transfers?type=validated&filter=to&block_number='+str(blocknumber)+'&index='+str(index), timeout=10) as resp0:
                transfers.append(await resp0.json())
                if transfers[-1]['next_page_params']:
                    blocknumber = transfers[-1]['next_page_params']['block_number']
                    index =  transfers[-1]['next_page_params']['index']
                else:
                    foundAll=True
        fts = [item['total']['token_id'] for t in transfers for item in t['items'] if item['from']['hash'] in TREASURYADDRESSES]
    except Exception as e:
        pass
    #####
    for address in TREASURYADDRESSES+[farm]:
        try:
            async with session.get('https://dex.iotabee.com/v3/nfts/'+address+'/'+IOTABEEPOSADDR, timeout=5) as resp:
                positions = await resp.json()
            if address==farm:
                positions = [p for p in positions if p['tokenid'] in fts]
            for p in positions:
                pair = Web3.to_checksum_address(p["pool"])
                tokenid =int(p["tokenid"])
            
                X = Web3.to_checksum_address(p["token0"])
                Y = Web3.to_checksum_address(p["token1"])
                tokXContract = w3.eth.contract(abi=cabi, address = X)
                tokYContract = w3.eth.contract(abi=cabi, address = Y)
                decimals0 = await tokXContract.functions.decimals().call()
                decimals1 = await tokYContract.functions.decimals().call()

                if X not in TOKENS:
                    xsym = await tokXContract.functions.symbol().call()
                    TOKENS[X] = {
                        'amount': 0,
                        'formatDec': 2,
                        'sym': xsym
                    }
                    needsUpdate = True
                if Y not in TOKENS:
                    ysym = await tokYContract.functions.symbol().call()
                    TOKENS[Y] = {
                        'amount': 0,
                        'formatDec': 2,
                        'sym': ysym
                    }
                    needsUpdate = True
                
                if tokenid not in IOTABEE: 
                    name = f'IOTABEE {TOKENS[X]["sym"]}-{TOKENS[Y]["sym"]}'
                    IOTABEE[tokenid] = {'name': name, 'amount': 0, 'depositX': 0.0, 'depositY': 0.0, 'X': X, 'Y': Y}
                    needsUpdate = True
                NFTContract = w3.eth.contract(abi=cabi, address=IOTABEEPOSADDR)
                position = await NFTContract.functions.positions(tokenid).call()
                bal = position[7]

                if abs(max(bal, 0.000000000000001)/max(IOTABEE[tokenid]["amount"], 0.000000000000001)-1) > 0.01:
                    needsUpdate = True
                IOTABEE[tokenid]["amount"] = bal
                
                pairContract = w3.eth.contract(abi=cabi, address=pair)

                total = await pairContract.functions.liquidity().call()
                share = bal / max(total, 0.000000000000001)

                poolX = await tokXContract.functions.balanceOf(pair).call()
                poolY = await tokYContract.functions.balanceOf(pair).call()

                IOTABEE[tokenid]["depositX"] = share * poolX * 10**-decimals0
                IOTABEE[tokenid]["depositY"] = share * poolY * 10**-decimals1
                
                pass    
        except Exception as e:
            pass
    return needsUpdate


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def addpchannel(ctx, arg):
    if ctx.author.id in ADMINS:
        try:
            PCHANNELS.append(int(arg))
            config.set('discord', 'pchannels', PCHANNELS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def delpchannel(ctx, arg):
    if ctx.author.id in ADMINS:
        try:
            PCHANNELS.remove(int(arg))
            config.set('discord', 'pchannels', PCHANNELS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addtchannel(ctx, arg):
    if ctx.author.id in ADMINS:
        try:
            TREASURYCHANNELS.append(int(arg))
            config.set('discord', 'treasurychannels', TREASURYCHANNELS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def deltchannel(ctx, arg):
    if ctx.author.id in ADMINS:
        try:
            TREASURYCHANNELS.remove(int(arg))
            config.set('discord', 'treasurychannels', TREASURYCHANNELS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addadmin(ctx, arg):
    if ctx.author.id in SUPERUSER:
        try:
            ADMINS.append(int(arg))
            config.set('discord', 'admins', ADMINS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def deladmin(ctx, arg):
    if ctx.author.id in SUPERUSER:
        try:
            ADMINS.remove(int(arg))
            config.set('discord', 'admins', ADMINS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command(brief='add ERC-20 token to watchlist `!addtoken <token address> <decimals>`')
async def addtoken(ctx, *args):
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
        try:
            if len(args) >= 1:
                TOKENS[args[0]]={'amount':0}
            if len(args) > 1:
                TOKENS[args[0]]["formatDec"] = args[1]
            config.set('watchlist', 'tokens', TOKENS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def deltoken(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
        try:
            clear = [k for k,v in TOKENS.items() if k==arg or v["sym"].lower()==arg.lower()]
            for c in clear:
                del TOKENS[c]

            config.set('watchlist', 'tokens', TOKENS)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addv2lp(ctx, *args):
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
        try:
            if len(args) > 1:
                LPSV2[args[0]]={'name': ' '.join(args[1:]), 'amount':0, 'tok0amount': 0,'tok1amount': 0}
            config.set('watchlist', 'lps', LPSV2)
            
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def delv2lp(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
        try:
            clear = [k for k,v in LPSV2.items() if k==arg or v["name"].lower() == arg.lower()]
            for c in clear:
                del LPSV2[c]

            config.set('watchlist', 'lps', LPSV2)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            print(e)
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addwallet(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
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
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
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
    if ctx.author.id in ADMINS:
        try:
            await ctx.message.add_reaction('⏳')
            await update_status()
            await output_status(ctx.message.channel)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            print(e)
            await ctx.message.add_reaction('⛔')

@bot.command()
async def output(ctx):
    if ctx.author.id in ADMINS:
        try:
            await output_status(ctx.message.channel)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            print(e)
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addlending(ctx, *args):
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
        try:
            if len(args) > 2:
                DEEPR[args[0]]={'amount':0, 'name': ' '.join(args[2:]), 'token': args[1]}
                
            config.set('watchlist', 'lendtokens', DEEPR)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def dellending(ctx, *args):
    arg = ' '.join(args)
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
        try:
            clear = [k for k,v in DEEPR.items() if k==arg or v["name"].lower()==arg.lower()]
            for c in clear:
                del DEEPR[c]

            config.set('watchlist', 'lendtokens', DEEPR)
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def addfarm(ctx, arg):
    if ctx.author.id in ADMINS and ctx.channel.id in ADMINCHANNELS:
        try:
            FARMS[arg] = {}
            config.set('watchlist', 'farms', FARMS)

            with open(configpath, 'w') as configfile:
                config.write(configfile)
            await ctx.message.add_reaction('✅')
        except:
            await ctx.message.add_reaction('⛔')

@bot.command(aliases=['P'])
async def p(ctx):
    global ptime
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        if time.time() > ptime + 2:
            try:
                # embed = discord.Embed(title="Marketdata", color=0xFF5733)
                embed = discord.Embed()
                embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240")
                #embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url='https://cdn.discordapp.com/avatars/1216381699122921572/2935a67fc7f656c5d1c575e9f42b2c08.png?size=256')

                iota_out = f'''
                `Price: ${iota["price"]:.3f}`
                `1H: {iota["price1h"]:.2f}%`
                `24H: {iota["price24h"]:.2f}%`
                `MCAP:  ${int(iota["mc"]):,}`
                `Twitter:  {iota["twitter"]}`
                `Watchlists: {iota["watchlists"]}`
                `Sentiment: ↑{iota["sentimentUP"]:.1f}% ↓{iota["sentimentDOWN"]:.1f}%`
                '''
                smr_out = f'''
                `Price: ${smr["price"]:.4f}`
                `1H: {smr["price1h"]:.2f}%`
                `24H: {smr["price24h"]:.2f}%`
                `MCAP:  ${int(smr["mc"]):,}`
                `Twitter:  {smr["twitter"]}`
                `Watchlists: {smr["watchlists"]}`
                `Sentiment: ↑{smr["sentimentUP"]:.1f}% ↓{smr["sentimentDOWN"]:.1f}%`
                '''
                embed.add_field(name=f'IOTA #{iota["rank"]}', value = iota_out)
                embed.add_field(name=f'SMR #{smr["rank"]}', value = smr_out)
                # embed.add_field(name=f'IOTA #{iota["rank"]}', value = '')
                # embed.add_field(name=f'SMR #{smr["rank"]}', value = '\n')

                # embed.add_field(name='', value='', inline=False)

                # embed.add_field(name='Price', value=f'${iota["price"]:.3f}', inline=True)
                # embed.add_field(name='Price', value=f'${smr["price"]:.4f}', inline=True)

                # embed.add_field(name='', value='', inline=False)

                # embed.add_field(name='1H', value=f'{iota["price1h"]:.2f}%', inline=True)
                # embed.add_field(name='1H', value=f'{smr["price1h"]:.2f}%', inline=True)

                # embed.add_field(name='', value='', inline=False)

                # embed.add_field(name='24H', value=f'{iota["price24h"]:.2f}%', inline=True)
                # embed.add_field(name='24H', value=f'{smr["price24h"]:.2f}%', inline=True)

                # embed.add_field(name='', value='', inline=False)

                # embed.add_field(name='MCAP', value=f'${int(iota["mc"]):,}', inline=True)
                # embed.add_field(name='MCAP', value=f'${int(smr["mc"]):,}', inline=True)

                # embed.add_field(name='', value='', inline=False)

                # embed.add_field(name='Twitter', value=f'{iota["twitter"]}', inline=True)
                # embed.add_field(name='Twitter', value=f'{smr["twitter"]}', inline=True)

                # embed.add_field(name='', value='', inline=False)

                # embed.add_field(name='Watchlists', value=f'{iota["watchlists"]}', inline=True)
                # embed.add_field(name='Watchlists', value=f'{smr["watchlists"]}', inline=True)

                # embed.add_field(name='', value='', inline=False)

                # embed.add_field(name='Sentiment', value=f'↑{iota["sentimentUP"]:.1f}% ↓{iota["sentimentDOWN"]:.1f}%', inline=True)
                # embed.add_field(name='Sentiment', value=f'↑{smr["sentimentUP"]:.1f}% ↓{smr["sentimentDOWN"]:.1f}%', inline=True)
                #embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png")
                embed.set_footer(text='data provided by coingecko')
                await ctx.send(embed=embed)
                await ctx.message.add_reaction('✅')
                ptime=time.time()
            except:
                await ctx.message.add_reaction('⛔')
        else:
            await ctx.message.add_reaction('⏱️')

# @bot.command()
# async def votes(ctx):
#     if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
#         try:
#             global vtime
#             if time.time() > ptime + VFREQUENCY or ctx.author.id in ADMINS:
#                 await ctx.send(file=discord.File(path+'addr_iota.json'))
#                 await ctx.send(file=discord.File(path+'addr_smr.json'))
#                 await ctx.send(file=discord.File(path+'events.json'))
#                 await ctx.message.add_reaction('✅')
#             else:
#                 await ctx.message.add_reaction('⏱️')
#         except Exception as e:
#             await ctx.message.add_reaction('⛔')
            
@bot.command()
async def convert(ctx, arg):
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        try:
            if 'iota' in arg:
                converted = iota_to_smr(arg)
                await ctx.send(converted)
                await ctx.message.add_reaction('✅')
            elif 'smr' in arg:
                converted = smr_to_iota(arg)
                await ctx.send(converted)
                await ctx.message.add_reaction('✅')
            else:
                await ctx.message.add_reaction('⛔')
        except Exception as e:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def voting(ctx, *args):
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        try:
            if len(args) > 0 and ('smr' in ' '.join(args).lower() or 'iota' in ' '.join(args).lower()):
                filterevent = ''
                for arg in args:
                    if not 'smr' in arg.lower() and not 'iota' in arg.lower():
                        filterevent=arg
                for arg in args:
                    votes = []
                    if 'smr' in arg:
                        tok = 'SMR'
                    elif 'iota' in arg:
                        tok = 'IOTA'
                    for k, vs in VOTINGS[tok].items():
                        if filterevent.lower() in k.lower() or filterevent.lower() in EVENTS[k]['name'].lower():
                            eventvotes = [v for v in vs if v[0]==arg]
                            for e in eventvotes:
                                votes.append([k,e])
                    for v in votes:
                        embed = discord.Embed(title=f'Votes of {arg}', color=0xFF5733)
                        embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240")
                        # embed.add_field(name=EVENTS[v[0]]['name'], value=EVENTS[v[0]]['additionalInfo'], inline=False)
                        embed.add_field(name=EVENTS[v[0]]['name'], value='', inline=False)
                        embed.add_field(name=v[1][1], value=f'{v[1][2]/10**6:,.0f} {tok}', inline=False)
                        for i in range(len(v[1][3])):
                            question = EVENTS[v[0]]['payload']['questions'][i]['text']
                            answer = v[1][3][i]
                            embed.add_field(name=question, value=answer)
                        await ctx.send(embed=embed)
                await ctx.message.add_reaction('✅')
            else:
                filterevent = ' '.join(args).lower()
                for k,v in {**VOTINGS['SMR'],**VOTINGS['IOTA']}.items():
                    if filterevent in k.lower() or filterevent in EVENTS[k]['name'].lower():
                        with open(k+".json", "w") as file:
                            json.dump(v, file, indent=2)
                        
                        await ctx.send(EVENTS[k]['name'], file=discord.File(k+".json"))
                await ctx.message.add_reaction('✅')
                
        except Exception as e:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def events(ctx, *args):
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        try:
            filterevents = ' '.join(args).lower()
            events = [v for e,v in EVENTS.items() if (filterevents in e.lower() or filterevents in v['name'].lower()) and (v['status']=='commencing' or v['status']=='holding' or len(args)>0)]
            for e in events:
                embed = discord.Embed(title=f'{e['name']}', color=0xFF5733)
                embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240")
                questions = e['payload']['questions']
                for i in range(len(questions)):
                    question = questions[i]['text']
                    embed.add_field(name=question, value='', inline=False)
                    answers = questions[i]['answers']
                    for j in range(len(answers)):
                        answer = answers[j]
                        if 'igp' in e['name'].lower():
                            circ = iota['circulating']
                            tok = 'IOTA'
                        else:
                            tok = 'SMR'
                            circ = smr['circulating']
                        embed.add_field(name=answer['text'], value=f'{0.001*answer['current']:,.0f} {tok} ({0.1*answer['current']/circ:.2f}%)')
                await ctx.send(embed=embed)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('⛔')

async def main():
    asyncio.create_task(update_thread())
    asyncio.create_task(update_price())
    asyncio.create_task(update_votings())
    global session
    session = aiohttp.ClientSession()
    await bot.start(DISCORDTOKEN)

if __name__ == "__main__":
    asyncio.run(main()) 
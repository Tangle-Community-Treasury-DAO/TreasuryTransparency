# region imports
import os, configparser, time, json, copy
from datetime import datetime, timedelta

import asyncio, aiohttp

from iota_sdk import Client, NodeIndexerAPI, Utils

from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth

import discord
from discord.ext import commands
from discord.utils import get

import pandas as pd
# endregion

# region statics

path = ''
# path = 'IOTA/various/evm/treasurytransparency/'
# rpc provider, add an abi to cavi if needed
w3 = Web3(AsyncHTTPProvider('https://json-rpc.evm.shimmer.network'), modules={'eth': (AsyncEth,)}, middlewares=[])
cabi = [
    {
        "inputs": [],
        "name": "poolLength",
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
            "internalType": "address",
            "name": "",
            "type": "address"
            },
            {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
            }
        ],
        "name": "userNFTs",
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
        
        ],
        "name": "liquidity",
        "outputs": [
        {
            "internalType": "uint128",
            "name": "",
            "type": "uint128"
        }
        ],
        "stateMutability": "view",
        "type": "function"
    },
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
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "userNFTs",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "getUserNFTs",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
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

# load statics from config
configpath = path+'startup.cfg'

config = configparser.RawConfigParser()
config.read(configpath)

TOKENS = eval(config["watchlist"]["tokens"]) # ERC-20 tokens
LPSV2 = eval(config["watchlist"]["lpsv2"]) # Uniswap V2 Liquidity Pools
TREASURYADDRESSES = eval(config["watchlist"]["treasuryaddresses"]) # Wallet addresses of treasury
DEEPR = eval(config["watchlist"]["deepr"]) # deepr lending pools
SWAPLINE = eval(config["watchlist"]["swapline"]) # swapline liquidity pools
TANGLESWAP = eval(config["watchlist"]["tangleswap"]) # tangleswap liquidity pools
TANGLEHELPER = eval(config["watchlist"]["tanglehelper"]) # tangleswap helper SC to determine positions
FARMS = eval(config["watchlist"]["farms"]) # shimmersea farms
IOTABEE = eval(config["watchlist"]["iotabee"]) # iotabee positions
IOTABEEPOSADDR = eval(config["watchlist"]["iotabeeposaddr"]) # iotabee position NFT
IOTABEEFARM = eval(config["watchlist"]["iotabeefarm"]) #iota bee 

DISCORDTOKEN = os.getenv('DISCORD_TOKEN') # discord bot token, export it first
ADMINCHANNELS = eval(config["discord"]["adminchannels"]) # discord channel id for administrative actions
TREASURYCHANNELS = eval(config["discord"]["treasurychannels"]) # discord channels to post treasury holdings
PCHANNELS = eval(config["discord"]["pchannels"]) # discord channels for p-bot
VFREQUENCY = eval(config["discord"]["vfrequency"]) # frequency in seconds to update current governance votings
PFREQUENCY = eval(config["discord"]["pfrequency"]) # frequency in seconds to update current price
ADMINS = eval(config["discord"]["admins"]) # admins with all priviliges except for adding/deleting admins
SUPERUSER = eval(config["discord"]["superuser"]) # superusers

#define discord bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# iota and smr price metrics for p bot
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
    'supply': 0,
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

# 
ptime = 0 # allows p command every ptime seconds
vtime = 0 # same for !votes but currently inactive

# current events and votes
EVENTS = {}
VOTINGS = {'SMR' : {},
           'IOTA': {}
        }
KNOWNWALLETS = {}


# endregion

# region helpers and data pull methods
# convert smr to iota addr, no safety checks
def smr_to_iota(addr): 
    byt = Utils.bech32_to_hex(addr)
    smr = Utils.hex_to_bech32(byt, 'iota')
    return smr

# convert iota to smr addr, no safety checks
def iota_to_smr(addr):
    byt = Utils.bech32_to_hex(addr)
    smr = Utils.hex_to_bech32(byt, 'smr')
    return smr

# small method to parse a vote from output data
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

# events progress bar
def progress_bar(percent):
    bar_length = 20
    num_blocks = int(bar_length * percent / 100)
    if num_blocks < bar_length / 2:
        bar = '|' + '█' * num_blocks + '░' * int((bar_length - num_blocks-6)/2) + f' {percent:.2f}%' + '░' * round((bar_length - num_blocks-6)//2) + '|'
    else:
        bar = '|' + '█' * int((num_blocks-6)/2) + f' {percent:.2f}%' + '█' * round((num_blocks-6)/2) + '░' * (bar_length - num_blocks) + '|'
    bar = '|' + '█' * num_blocks + '░' * (bar_length - num_blocks) + '|'
    return bar

def get_percentage(start, end, t):
    return 100*min((max(t-start, 0)) / (end-start),1)

# thread to update current event standings frequently
async def update_votings():
    smr_node = "https://shimmer-node.tanglebay.com"
    # smr_node = "https://api.shimmer.network"
    iota_node = "https://iota-node.tanglebay.com"
    part_endpoint = '/api/participation/v1/events'

    client_smr = Client(nodes= [smr_node])
    client_iota = Client(nodes= [iota_node])
    # repeat infinitely every VFREQUENCY seconds
    while True:
        try:
            # pull SMR event ids from nodes participation plugin
            async with session.get(smr_node+part_endpoint, timeout=5) as resp:
                smreventids = (await resp.json())['eventIds']
            async with session.get(iota_node+part_endpoint, timeout=5) as resp:
                iotaeventids =(await resp.json())['eventIds']

            pullSmrOuts = False
            pullSmrMilestone = 9999999999999999999
            smrMilestone = client_smr.get_info().nodeInfo.status.confirmedMilestone.index
            for id in smreventids:
                #pull basic event information from nodes participation plugin
                async with session.get(smr_node+part_endpoint+'/'+id, timeout=10) as resp:
                    EVENTS[id] = await resp.json()
                #pull current event information from nodes participation plugin
                async with session.get(smr_node+part_endpoint+'/'+id+'/status', timeout=10) as resp:
                    status = await resp.json()
                    EVENTS[id]['status'] = status['status']
                    EVENTS[id]['milestone'] = smrMilestone
                    EVENTS[id]['startTimeStamp'] = client_smr.get_milestone_by_index(EVENTS[id]['milestoneIndexStart']).timestamp
                    #if currently an event active, pull all outputs after event starting date later on
                    if status['status']=='commencing' or status['status']=='holding':
                        pullSmrOuts = True
                        pullSmrMilestone = min(pullSmrMilestone, EVENTS[id]['milestoneIndexCommence'])
                    milestone = client_smr.get_milestone_by_index(smrMilestone)
                    EVENTS[id]['lastUpdated'] = milestone.timestamp
                    #insert current eevnt sandings into EVENTS object
                    for i in range(len(status['questions'])):
                        for j in range(len(status['questions'][i]['answers'])):
                            if j < len(EVENTS[id]['payload']['questions'][i]['answers']):
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['current'] = status['questions'][i]['answers'][j]['current']
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['accumulated'] = status['questions'][i]['answers'][j]['accumulated']
                            elif status['questions'][i]['answers'][j]['value'] == 0:
                                EVENTS[id]['payload']['questions'][i]['answers'].append(status['questions'][i]['answers'][j])
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['text'] = 'Abstain'
            
            # repeat the same with IOTA 
            pullIotaOuts = False
            pullIotaMilestone = 9999999999999999999
            iotaMilestone = client_iota.get_info().nodeInfo.status.confirmedMilestone.index
            #for id in [s for s in iotaeventids if s not in EVENTS]:
            for id in iotaeventids:
                async with session.get(iota_node+part_endpoint+'/'+id, timeout=5) as resp:
                    EVENTS[id] = await resp.json()
                async with session.get(iota_node+part_endpoint+'/'+id+'/status', timeout=5) as resp:
                    status = await resp.json()
                    EVENTS[id]['status'] = status['status']
                    EVENTS[id]['milestone'] = iotaMilestone
                    EVENTS[id]['startTimeStamp'] = client_iota.get_milestone_by_index(EVENTS[id]['milestoneIndexStart']).timestamp
                    if status['status']=='commencing' or status['status']=='holding':
                        pullIotaOuts = True
                        pullIotaMilestone = min(pullIotaMilestone, EVENTS[id]['milestoneIndexCommence'])
                    milestone = client_iota.get_milestone_by_index(iotaMilestone)
                    EVENTS[id]['lastUpdated'] = milestone.timestamp
                    for i in range(len(status['questions'])):
                        for j in range(len(status['questions'][i]['answers'])):
                            if j < len(EVENTS[id]['payload']['questions'][i]['answers']):
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['current'] = status['questions'][i]['answers'][j]['current']
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['accumulated'] = status['questions'][i]['answers'][j]['accumulated']
                            elif status['questions'][i]['answers'][j]['value'] == 0:
                                EVENTS[id]['payload']['questions'][i]['answers'].append(status['questions'][i]['answers'][j])
                                EVENTS[id]['payload']['questions'][i]['answers'][j]['text'] = 'Abstain'

            # if smr event currently active, pull all outputs for the !votes command and store them in VOTINGS
            if pullSmrOuts:
                milestone = client_smr.get_milestone_by_index(pullSmrMilestone)
                qp = NodeIndexerAPI.QueryParameters(
                    tag='0x'+b'PARTICIPATE'.hex(),
                    created_after=milestone.timestamp
                )
                output_ids_smr = client_smr.basic_output_ids(qp).items
                outputs_smr = client_smr.get_outputs(output_ids_smr)
                VOTINGS['SMR']={}

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

            # same with IOTA
            if pullIotaOuts:
                milestone = client_iota.get_milestone_by_index(pullIotaMilestone)
                qp = NodeIndexerAPI.QueryParameters(
                    tag='0x'+b'PARTICIPATE'.hex(),
                    created_after=milestone.timestamp
                )
                output_ids_iota = client_iota.basic_output_ids(qp).items
                outputs_iota = client_iota.get_outputs(output_ids_iota)
                VOTINGS['IOTA']={}
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
            print(e)
        await asyncio.sleep(VFREQUENCY)
        
# update and store price metrics in static variables from coingecko 
async def update_price():
    iota_url = 'https://api.coingecko.com/api/v3/coins/iota?localization=false&tickers=false&market_data=true&community_data=true&developer_data=false'
    smr_url = 'https://api.coingecko.com/api/v3/coins/shimmer?localization=false&tickers=false&market_data=true&community_data=true&developer_data=false'
    # pull every PFREQUENCY seconds
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
                iota["supply"] = iotarsp["market_data"]["max_supply"]
                iota["circulating"] = iotarsp["market_data"]["circulating_supply"]
                # net_launch = 1681113738
                # now = time.time()
                # bi_weeks_passed = (now - net_launch) // (2*7*86400)
                # iota["circulating"] = 2529939788+54896344+7664631+2*552000000*(0.1+0.9*min(bi_weeks_passed/208,1))+325469717*(0.1+0.9*min(bi_weeks_passed/208,1))+161000000*(0.1+0.9*min(bi_weeks_passed/104,1))+230000000*(0.1+0.9*min(bi_weeks_passed/104,1))


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
                smr["supply"] = smrrsp["market_data"]["max_supply"]
                # smr["circulating"] = max(smrrsp["market_data"]["circulating_supply"], smrrsp["market_data"]["total_supply"])
                smr["circulating"] = smrrsp["market_data"]["max_supply"]
            # explorer_url = 'https://explorer-api.iota.org/networks'
            # async with session.get(explorer_url, timeout=5) as resp:
            #     explorerRsp = await resp.json()
            #     iotanet = [r for r in explorerRsp["networks"] if r['network']=='mainnet']
            #     smrnet = [r for r in explorerRsp["networks"] if r['network']=='shimmer']
            #     iota["circulating2"] = iotanet[0]['circulatingSupply']* 10**-6
            #     smr["circulating2"] =  smrnet[0]['circulatingSupply']* 10**-6
        except Exception as e:
            print(e)
        await asyncio.sleep(PFREQUENCY)
    pass

# print current treasury holdings and positions into specified channel
async def output_status(channel):
    
    embed = discord.Embed()
    embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url='https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240')

    # add ERC-20 tokens to output messaged 
    embed.add_field(name='__Tokens on ShimmerEVM:__', value='', inline=False)
    for token in TOKENS.keys():
        if TOKENS[token]["amount"] > 0:
            dec = 1
            if 'formatDec' in TOKENS[token].keys():
                dec = TOKENS[token]["formatDec"]
            # format with dec decimals and thousand-seperator and strip unnecessary .0
            embed.add_field(name=TOKENS[token]["sym"], value = f'{TOKENS[token]["amount"]:,.{dec}f}'.rstrip('0').rstrip('.'))

    # format and append ShimmerSEA LP positions
    embed.add_field(name='__Shimmersea:__', value='', inline=False)
    for pool, pair in LPSV2.items():
        if pair["tok0amount"] > 0:
            dec1 = 1
            if 'formatDec' in TOKENS[pair["tok0"]].keys():
                dec1 = TOKENS[pair["tok0"]]["formatDec"]
            dec2 = 1
            if 'formatDec' in TOKENS[pair["tok1"]].keys():
                dec2 = TOKENS[pair["tok1"]]["formatDec"]
            tok0string = f'{pair["tok0amount"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            tok1string = f'{pair["tok1amount"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["tok0"]]["sym"]}-{TOKENS[pair["tok1"]]["sym"]}', value = f'{tok0string}-{tok1string}')

    # format and append iotabee positions
    embed.add_field(name='__IOTABee:__', value='', inline=False)
    for id, pair in IOTABEE.items():
        if pair["amount"] > 0:
            dec1 = 1
            if 'formatDec' in TOKENS[pair["X"]].keys():
                dec1 = TOKENS[pair["X"]]["formatDec"]

            dec2 = 1
            if 'formatDec' in TOKENS[pair["Y"]].keys():
                dec2 = TOKENS[pair["Y"]]["formatDec"]

            Xstring = f'{pair["depositX"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            Ystring = f'{pair["depositY"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{Xstring}-{Ystring}')
    
    # cut here because embed can only hold 25 fields
    await channel.send(embed=embed)

    embed = discord.Embed()
    embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url='https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240')

    # format and append swapline positions
    embed.add_field(name='__Swapline:__', value='', inline=False)
    for pool, pair in SWAPLINE.items():
        if pair["depositX"] + pair["depositY"] > 0:
            dec1 = 1
            if 'formatDec' in TOKENS[pair["X"]].keys():
                dec1 = TOKENS[pair["X"]]["formatDec"]

            dec2 = 1
            if 'formatDec' in TOKENS[pair["Y"]].keys():
                dec2 = TOKENS[pair["Y"]]["formatDec"]
            
            Xstring = f'{pair["depositX"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            Ystring = f'{pair["depositY"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{Xstring}-{Ystring}')
    
    #format and append tangleswap positions
    embed.add_field(name='__TangleSwap:__', value='', inline=False)
    for pool, pair in TANGLESWAP.items():
        if pair["amount"] > 0:
            dec1 = 1
            if 'formatDec' in TOKENS[pair["X"]].keys():
                dec1 = TOKENS[pair["X"]]["formatDec"]

            dec2 = 1
            if 'formatDec' in TOKENS[pair["Y"]].keys():
                dec2 = TOKENS[pair["Y"]]["formatDec"]
            
            Xstring = f'{pair["depositX"]:,.{dec1}f}'.rstrip('0').rstrip('.')
            Ystring = f'{pair["depositY"]:,.{dec2}f}'.rstrip('0').rstrip('.')
            embed.add_field(name=f'{TOKENS[pair["X"]]["sym"]}-{TOKENS[pair["Y"]]["sym"]}', value = f'{Xstring}-{Ystring}')
    
    #format and append deepr positions
    embed.add_field(name='__DeepR:__', value='', inline=False)
    for pool, token in DEEPR.items():
        if token["amount"] > 0:
            dec = 1
            if 'formatDec' in TOKENS[token["token"]].keys():
                dec = TOKENS[token["token"]]["formatDec"]
            embed.add_field(name=TOKENS[token["token"]]["sym"], value = f'{token["amount"]:,.{dec}f}'.rstrip('0').rstrip('.'))
            
    await channel.send(embed=embed)

# thread for updating all positions every 24h
async def update_thread():
    await asyncio.sleep(3)
    channels = []
    # post update to all channels in TREASURYCHANNELS
    for chan in TREASURYCHANNELS:
        channels.append(bot.get_channel(chan))
    out_counter = 0
    while True: 
        #if positions changed - output the new holdings and save them in config
        out_counter = (out_counter+1)%24
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

            if out_counter == 0:
                for c in channels:
                    try:
                        await output_status(c)
                    except Exception as e:
                        print(e)
        await asyncio.sleep(60*60)
   
# update all holdings
async def update_status():
    # every update own variable because python skips all further methods in "or" clause 
    # if it found a true one already
    threads = [update_farms() ,update_swapline(), update_tangleswap(), update_univ3(), update_lending() , update_tokens()]
    results = await asyncio.gather(*threads, return_exceptions=True)
    upLP = await update_univ2() # requires update on farms first
    # upSwap = await update_swapline()
    # upTangle = await update_tangleswap()
    # upBee = await update_univ3()
    # upLend = await update_lending()
    # upTok = await update_tokens()
    # upLum = await update_lum()
    #return any position changed
    # return upFarms or upTok or upLP or upTangle or upBee or upSwap  or upLend or upLum
    return upLP or any(results)

# update ERC-20 holdings, can handle any ERC-20
# all information about tokens in any pools are pulled from this TOKENS variable
async def update_tokens():
    needsUpdate = False
    for id, value in TOKENS.items():
        try:
            contract = w3.eth.contract(abi=cabi, address=id)
            decimals = await contract.functions.decimals().call()
            amount = 0
            # get and sum up in all wallets
            for address in TREASURYADDRESSES:
                amount += await contract.functions.balanceOf(address).call() * 10**-decimals
            
            # make sure token has a symbol
            if 'sym' not in value.keys():
                value["sym"] = await contract.functions.symbol().call()

            # if position changed by more than 1%, return it needs an output
            if abs(max(amount, 0.000000000000001)/max(TOKENS[id]["amount"], 0.000000000000001)-1) > 0.01:
                needsUpdate = True
            TOKENS[id]["amount"] = amount
        except Exception as e:
            print(e)
    return needsUpdate

# update uniswap v2 LP positions, can handle any v2 LP
async def update_univ2():
    needsUpdate = False
    for id, pair in LPSV2.items():
        try:
            contract = w3.eth.contract(abi=cabi, address=id)

            #get total liquidity in pool
            total = await contract.functions.totalSupply().call()

            #get total tokens in pool
            reserves = await contract.functions.getReserves().call()
            tok0 = await contract.functions.token0().call()
            tok1 = await contract.functions.token1().call()

            #pull information about both tokens in pool
            tok0Contract = w3.eth.contract(abi=cabi, address = tok0)
            tok1Contract = w3.eth.contract(abi=cabi, address = tok1)
            decimals0 = await tok0Contract.functions.decimals().call()
            decimals1 = await tok1Contract.functions.decimals().call()

            # make sure LPSV2 knows the tokens in that LP
            if 'tok0' not in pair.keys():
                pair["tok0"] = tok0
            if 'tok1' not in pair.keys():
                pair["tok1"] = tok1

            # add those tokens to TOKENS if not known yet
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

            # get and sum up liqudiity over all treasury wallets
            for address in TREASURYADDRESSES:
                bal += await contract.functions.balanceOf(address).call() 
            
            # add liquidity from farms
            farms = []
            for f in FARMS.values():
                for i in range(len(f)):
                    if f[i]["poolID"]==id:
                        farms.append(f[i])
            for f in farms:
                bal += f["amount"]

            # calculate treasury share in the pool
            share = bal / total 
            
            # if liquidity changed, we need a new balance output in channel
            if abs(max(bal, 0.000000000000001)/max(pair["amount"], 0.000000000000001)-1) > 0.01:
                needsUpdate = True
            
            # store our positions for the output
            pair["amount"] = bal
            LPSV2[id]["tok0amount"] = reserves[0] * share * 10**-decimals0
            LPSV2[id]["tok1amount"] = reserves[1] * share * 10**-decimals1
        except Exception as e:
            print(e)
    return needsUpdate

# update swapline positions through their API
async def update_swapline():
    needsUpdate = False
    swap_back = copy.deepcopy(SWAPLINE)
    for pair in SWAPLINE:
        SWAPLINE[pair]["amount"] = 0
        SWAPLINE[pair]["depositX"] = 0
        SWAPLINE[pair]["depositY"] = 0

    for address in TREASURYADDRESSES:
        try:
            # get all positions in all treasury wallets
            async with session.get('https://api-c.swapline.com/api/v1/user-positions/'+address, timeout=5) as resp:
                positions = await resp.json()
                for p in positions:
                    amount = sum([float(l["amountXRaw"]+l["amountYRaw"]) for l in p["userBinLiquidities"]])
                    pair = Web3.to_checksum_address(p["pairAddress"])

                    # get LP information from the contract
                    if pair not in SWAPLINE:
                        contract = w3.eth.contract(abi=cabi, address=pair)
                        X = await contract.functions.getTokenX().call()
                        Y = await contract.functions.getTokenY().call()
                        tokXContract = w3.eth.contract(abi=cabi, address = X)
                        tokYContract = w3.eth.contract(abi=cabi, address = Y)
                        
                        # add any new found tokens to TOKENS
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
                    
                        # automatically set a name for that pool 
                        # because it does not need to be addded manually
                        name = f'Swapline {TOKENS[X]["sym"]}-{TOKENS[Y]["sym"]}'
                        SWAPLINE[pair] = {'name': name, 'amount': 0, 'depositX': 0.0, 'depositY': 0.0, 'X': X, 'Y': Y}
                    
                    # needs a balance output to channel if liquidity changed more than 1%
                    if abs(max(amount, 0.000000000000001)/max(SWAPLINE[pair]["amount"], 0.000000000000001)-1) > 0.01:
                        needsUpdate = True
                    SWAPLINE[pair]["amount"] = amount

                    SWAPLINE[pair]["depositX"] = p["depositX"]
                    SWAPLINE[pair]["depositY"] = p["depositY"]
                pass    
        except Exception as e:
            SWAPLINE = swap_back
            print(e)
    return needsUpdate

# update deepr lending positions
async def update_lending():
    needsUpdate = False
    for id, value in DEEPR.items():
        try:
            # pull lending pool information from smart contract
            contract = w3.eth.contract(abi=cabi, address=id)
            underlying = await contract.functions.underlying().call()

            # add any new found tokens to TOKENS
            if underlying not in TOKENS:
                sym = await underlying.functions.symbol().call()
                TOKENS[underlying] = {
                    'amount': 0,
                    'formatDec': 2,
                    'sym': sym
                }

                # new tokens found means we need to print balance to channel
                needsUpdate = True

            ucontract = w3.eth.contract(abi=cabi, address=underlying)
            decimals = await ucontract.functions.decimals().call()
            amount = 0

            # get and sum up our deposited liquidity in all treasury wallets
            for address in TREASURYADDRESSES:
                amount += await contract.functions.balanceOfUnderlying(address).call() * 10**-decimals
            
            # if liquidity changed, we need to print balance to channel
            if abs(max(amount, 0.000000000000001)/max(DEEPR[id]["amount"], 0.000000000000001)-1) > 0.01:
                needsUpdate = True
            DEEPR[id]["amount"] = amount
        except Exception as e:
            print(e)
    return needsUpdate

# update all farms of v2 liquidity tokens
async def update_farms():
    needsUpdate = False
    for id, value in FARMS.items():
        try:
            # get amount of pools in that farm
            contract = w3.eth.contract(abi=cabi, address=id)
            length = await contract.functions.poolLength().call()

            for i in range(length):
                #if we have not pulled pools from this farm yet, add them to FARMS
                if i not in value.keys():
                    value[i] = {'amount': 0}

                if 'poolID' not in value[i].keys():
                    poolID = (await contract.functions.poolInfo(i).call())[0]
                    value[i]["poolID"] = poolID
                
                # get LP tokens deposited from all treasury wallets and pool i
                amount = 0
                for address in TREASURYADDRESSES:
                    amount += (await contract.functions.userInfo(i, address).call())[0]

                # if our LP token amount changed by >1%, we need to print new balance to channels
                if abs(max(amount, 0.000000000000001)/max(FARMS[id][i]["amount"], 0.000000000000001)-1) > 0.01:
                    needsUpdate = True
                
                FARMS[id][i]["amount"] = amount
        except Exception as e:
            print(e)
    return needsUpdate

# pull staked and boosted Lum and mLum tokens
# WIP
async def update_lum():
    pass

# update tangleswap positions
async def update_tangleswap():
    needsUpdate = False
    tangle_back = copy.deepcopy(TANGLESWAP)
    for pair in TANGLESWAP:
        TANGLESWAP[pair]["amount"] = 0
        TANGLESWAP[pair]["depositX"] = 0
        TANGLESWAP[pair]["depositY"] = 0
    for address in TREASURYADDRESSES:
        try:
            # get all position NFT IDs from tangleswap API
            async with session.get('https://backend.tangleswap.space/api/v1/chains/148/wallet/'+address+'/positions', timeout=5) as resp:
                positions = await resp.json()
                for p in positions:
                    amount = int(p["liquidity"])
                    pair = Web3.to_checksum_address(p["poolAddress"])
                    pid = pair+str(p["id"])

                    # get information about both pooled Tokens from their ERC-20 SCs
                    X = Web3.to_checksum_address(p["token0Address"])
                    Y = Web3.to_checksum_address(p["token1Address"])
                    tokXContract = w3.eth.contract(abi=cabi, address = X)
                    tokYContract = w3.eth.contract(abi=cabi, address = Y)
                    decimals0 = await tokXContract.functions.decimals().call()
                    decimals1 = await tokYContract.functions.decimals().call()

                    # add any new found tokens to TOKENS
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
                    
                    # add any new found positioN NFTs to TANGLESWAP
                    if pid not in TANGLESWAP: 
                        name = f'Tangleswap {TOKENS[X]["sym"]}-{TOKENS[Y]["sym"]}'
                        TANGLESWAP[pid] = {'name': name, 'amount': 0, 'depositX': 0.0, 'depositY': 0.0, 'X': X, 'Y': Y}
                        needsUpdate = True

                    # if our liquidity changed, we need to print the new balance
                    if abs(max(amount, 0.000000000000001)/max(TANGLESWAP[pid]["amount"], 0.000000000000001)-1) > 0.01:
                        needsUpdate = True
                    TANGLESWAP[pid]["amount"] = amount
                    
                    # pull our deposited tokens through the tangleswap helper SC
                    hcontract =  w3.eth.contract(abi=cabi, address = TANGLEHELPER)
                    pos = await hcontract.functions.getPrincipalByTokenId(p["id"]).call()
                    
                    TANGLESWAP[pid]["depositX"] = pos[0] * 10**-decimals0
                    TANGLESWAP[pid]["depositY"] = pos[1] * 10**-decimals1
                    
        except Exception as e:
            TANGLESWAP = tangle_back
            print(e)
    return needsUpdate

# update IOTABee positions, can handle any uniswap v3 LP
async def update_univ3():# 
    needsUpdate = False
    ### GET IOTABEE FARM ADDRESSES FROM: https://iotabee.com/js/app.ca61174f.js

    iota_back = copy.deepcopy(IOTABEE)
    for tokenid in IOTABEE:
        IOTABEE[tokenid]["amount"] = 0
        IOTABEE[tokenid]["depositX"] = 0
        IOTABEE[tokenid]["depositY"] = 0
  
    #region get deposited NFTs from blockchain, outdated
    # blockscout grrrr
    # since the staking SC isn't verified and we can't read it yet, 
    # we need to find all deposits of treasury position NFTs into the staking SC.
    # try:
    #     foundAll = False
    #     transfers= []
    #     farm = '0xa2c8B10F8307246B0252090a8073b6a5c04c7Ff0'

    #     # get all transactions to the staking SC / farm through blockscout API
    #     async with session.get('https://explorer.evm.shimmer.network/api/v2/addresses/'+farm+'/token-transfers?type=validated&filter=to', timeout=10) as resp0:
    #         transfers.append(await resp0.json())
    #     blocknumber = transfers[-1]['next_page_params']['block_number']
    #     index =  transfers[-1]['next_page_params']['index']

    #     # cycle through all pages until all transactions to the farm are found
    #     while not foundAll:
    #         async with session.get('https://explorer.evm.shimmer.network/api/v2/addresses/0xa2c8B10F8307246B0252090a8073b6a5c04c7Ff0/token-transfers?type=validated&filter=to&block_number='+str(blocknumber)+'&index='+str(index), timeout=10) as resp0:
    #             transfers.append(await resp0.json())
    #             if transfers[-1]['next_page_params']:
    #                 blocknumber = transfers[-1]['next_page_params']['block_number']
    #                 index =  transfers[-1]['next_page_params']['index']
    #             else:
    #                 foundAll=True
        
    #     # note all NFT IDs that got deposited into the farm / staking pool by any treasury wallet
    #     fts = [int(item['total']['token_id']) for t in transfers for item in t['items'] if item['from']['hash'] in TREASURYADDRESSES]
    # except Exception as e:
    #     pass

    #endregion

    # https://github.com/iotadex/ibstake/blob/fd732e1a9dd4b4cc5545d3d095ac2eea75a1897d/artifacts/contracts/stakeNFT721.sol/StakeNFT721.json#L391
    
    #get deposited positions in farm
    fts = []
    for farmAddress in IOTABEEFARM:
        fc = w3.eth.contract(abi=cabi, address=farmAddress)
        for address in TREASURYADDRESSES:
            i = 0
            foundAll = False
            while not foundAll:
                try:
                    NFTid = await fc.functions.userNFTs(address, i).call()
                    fts.append(NFTid)
                    i+=1
                except:
                    foundAll = True
    #####
    for address in TREASURYADDRESSES+IOTABEEFARM:
        try:
            # get all currently owned position NFTs from iotabee api 
            # as well as all NFTs owned by the staking pool / farm
            async with session.get('https://dex.iotabee.com/v3/nfts/'+address+'/'+IOTABEEPOSADDR, timeout=5) as resp:
                positions = await resp.json()

            # we only want those position NFTs in the farm that belong to treasury
            if address in IOTABEEFARM:
                positions = [p for p in positions if int(p['tokenid']) in fts]

            # for all position NFTs, pull liquidity tokens from v3 contract
            for p in positions:
                pair = Web3.to_checksum_address(p["pool"])
                tokenid =int(p["tokenid"])

                # get information about both pooled tokens
                X = Web3.to_checksum_address(p["token0"])
                Y = Web3.to_checksum_address(p["token1"])
                tokXContract = w3.eth.contract(abi=cabi, address = X)
                tokYContract = w3.eth.contract(abi=cabi, address = Y)
                decimals0 = await tokXContract.functions.decimals().call()
                decimals1 = await tokYContract.functions.decimals().call()

                # add any new found tokens to TOKENS
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
                
                # if they haven't been found before, add new position NFTs to IOTABEE
                if tokenid not in IOTABEE: 
                    name = f'IOTABEE {TOKENS[X]["sym"]}-{TOKENS[Y]["sym"]}'
                    IOTABEE[tokenid] = {'name': name, 'amount': 0, 'depositX': 0.0, 'depositY': 0.0, 'X': X, 'Y': Y}
                    needsUpdate = True
                
                # get treasury liquidity amount
                NFTContract = w3.eth.contract(abi=cabi, address=IOTABEEPOSADDR)
                position = await NFTContract.functions.positions(tokenid).call()
                bal = position[7]

                # if treasury liquidity changed, we need to print new balance
                if abs(max(bal, 0.000000000000001)/max(IOTABEE[tokenid]["amount"], 0.000000000000001)-1) > 0.01:
                    needsUpdate = True
                IOTABEE[tokenid]["amount"] = bal
                
                # get total liquidity of pool
                pairContract = w3.eth.contract(abi=cabi, address=pair)
                total = await pairContract.functions.liquidity().call()

                # get pools token balance
                poolX = await tokXContract.functions.balanceOf(pair).call()
                poolY = await tokYContract.functions.balanceOf(pair).call()

                # calculate our share of pool for an estimation of deposited tokens
                share = bal / max(total, 0.000000000000001)
                
                IOTABEE[tokenid]["depositX"] = share * poolX * 10**-decimals0
                IOTABEE[tokenid]["depositY"] = share * poolY * 10**-decimals1
  
        except Exception as e:
            IOTABEE = iota_back
            print(e)
    return needsUpdate

# endregion

# region discord bot commands and events

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# adds a channel-id by an admin where users can query p
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

# deletes a previously added channel for p
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

# adds a channel where the bot prints treasury balances
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

# deletes a previously added channel for treasury balance outputs
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

# superuser can add an admin by discord user-id
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

# superuser can delete an admin by discord user-id
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

# adds an ERC-20 token to watchlist, only by an Admin in an admin channel
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

# deletes a ERC-20 token from watchlist
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

# adds any uniswap v2 lp to the watchlist
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

# removes a previously added v2 lp from watchlist
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

# adds a wallet to the watchlsit
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

# deletes a wallet from watchlsit
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

# forces an update of balances and prints them in the channel
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

# forces an output of last stored treasury balances
@bot.command()
async def output(ctx):
    if ctx.author.id in ADMINS:
        try:
            await output_status(ctx.message.channel)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            print(e)
            await ctx.message.add_reaction('⛔')

# adds a lending smart contract to watchlist
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

# deletes a previously added lending SC from watchlist
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

# adds a farm for uniswap v2 LP tokens to watchlist
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

# prints current SMR and IOTA token information
@bot.command(aliases=['P', "pi", "Pi"])
async def p(ctx):
    global ptime
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        # only print every ptime seconds at most
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
       
# converts SMR to IOTA addresses and vice versa
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

# displays votes, filtered by address and/or event id/name
@bot.command(aliases=["vote", "v", "V"])
async def votes(ctx, *args):
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        try:
            # if submitted filter contains an address
            if len(args) > 0 and ('smr' in ' '.join(args).lower() or 'iota' in ' '.join(args).lower()):
                filterevent = ''
                for arg in args:
                    # if one of the filters is an event filter
                    if not 'smr' in arg.lower() and not 'iota' in arg.lower():
                        filterevent=arg
                # output for each filtered wallet address
                for arg in args:
                    votes = []
                    # if we filter a SMR or IOTA wallet
                    if 'smr' in arg:
                        tok = 'SMR'
                    elif 'iota' in arg:
                        tok = 'IOTA'
                    
                    # filter out VOTINGS by specified event names/ids
                    for k, vs in VOTINGS[tok].items():
                        if filterevent.lower() in k.lower() or filterevent.lower() in EVENTS[k]['name'].lower():
                            eventvotes = [v for v in vs if v[0]==arg]
                            for e in eventvotes:
                                votes.append([k,e])
                    
                    # output all filtered votes
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
                # only event filters, so will output a file with all voting wallets
                filterevent = ' '.join(args).lower()
                for k,v in {**VOTINGS['SMR'],**VOTINGS['IOTA']}.items():
                    if filterevent in k.lower() or filterevent in EVENTS[k]['name'].lower():
                        # for vote in v:
                        #     answs = vote.pop()
                        #     for a in answs:
                        #         vote.append(a)
                        with open(k+".json", "w") as file:
                            json.dump(v, file, indent=2)
                        with open(k+'.json', encoding='utf-8') as inputfile:
                            df = pd.read_json(inputfile)

                        df.to_csv(k+'.csv', encoding='utf-8', header=False, index=False)

                        #await ctx.send(EVENTS[k]['name'], file=discord.File(k+".json"))
                        await ctx.send(EVENTS[k]['name'], file=discord.File(k+".csv"))
                await ctx.message.add_reaction('✅')
                
        except Exception as e:
            await ctx.message.add_reaction('⛔')

# displays events, filtered by name and/or id
@bot.command(aliases=["event", "e", "E"])
async def events(ctx, *args):
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        try:
            filterevents = ' '.join(args).lower()
            # filter by specified name/id fragment
            # if none specified only take currently active events
            events = [v for e,v in EVENTS.items() if (filterevents in e.lower() or filterevents in v['name'].lower()) and (v['status']=='commencing' or v['status']=='holding' or len(args)>0)]
            # print filtered events
            for e in events:
                if 'igp' in e['name'].lower():
                    now = time.time()
                    stardustStart = 1696384800
                    if e['startTimeStamp'] <= stardustStart:
                        circ = 2779530283
                    else:
                        bi_weeks_passed = (now - stardustStart) // (2*7*86400)
                        bi_weeks_event_start = ((e['startTimeStamp']) - stardustStart) // (2*7*86400)
                        vesting4 = 552000000*2+325469717
                        vesting2 = 161000000+230000000
                        difference = (bi_weeks_passed-bi_weeks_event_start)*0.9*(vesting4*int(bi_weeks_passed<=104)/104+vesting2*int(bi_weeks_passed<=52)/52)

                        circ = iota['circulating'] - difference

                    # circ2 = iota['circulating2']
                    tok = 'IOTA'
                    emoji = get(ctx.message.guild.emojis, name="iota")
                    #tok = emoji
                    iconurl = 'https://cdn.discordapp.com/emojis/1218594954914435082.png?size=240'
                else:
                    tok = 'SMR'
                    emoji = get(ctx.message.guild.emojis, name="shimmer")
                    #tok = emoji
                    iconurl = 'https://cdn.discordapp.com/emojis/1218595450286768169.png?size=240'
                    #circ2 = smr['circulating']
                    #circ2 = smr['circulating2'] 
                    circ = smr['circulating']

                if not emoji:
                    emoji = tok
                embed = discord.Embed(title=f'{e["name"]}', color=0xFF5733)
                if 'lastUpdated' in e:
                    embed.timestamp = datetime.fromtimestamp(e["lastUpdated"])
                embed.set_author(name="Tangle Treasury",url="https://www.tangletreasury.org/", icon_url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240")
                #embed.set_author(name="Tangle Treasury",url="https://www.tangletreasury.org/", icon_url=iconurl)
                remaining_seconds = max(int((e["lastUpdated"]-e["startTimeStamp"])*((e["milestoneIndexEnd"]-e["milestoneIndexStart"])/(e["milestone"]-e["milestoneIndexStart"])-1) - time.time()+ e["lastUpdated"]),0)
                # days = remaining_seconds // 86400
                # hours = (remaining_seconds % 86400) // 3600
                # minutes = (remaining_seconds % 3600) // 60
                remaining = str(timedelta(seconds=remaining_seconds))

                embed.add_field(name = f'{progress_bar(get_percentage( e["milestoneIndexStart"], e["milestoneIndexEnd"], e["milestone"]))} {remaining} remaining', value='')

                questions = e['payload']['questions']
                for i in range(len(questions)):
                    question = questions[i]['text']
                    goal = 0.05 * circ * (e['milestoneIndexEnd'] - e['milestoneIndexStart'])
                    #goal2 = 0.05 * circ2 * (e['milestoneIndexEnd'] - e['milestoneIndexStart'])
                    timeleft = max(0,(min(e['milestoneIndexEnd']-e['milestone'],e['milestoneIndexEnd'] - e['milestoneIndexStart'])))
                    answers = questions[i]['answers']

                    accumulated = 0.001* sum([a['accumulated'] for a in answers])
                    current = 0.001* sum([a['current'] for a in answers])
                    missing = max((goal - accumulated) / max(timeleft,0.0000000000000001) - current,0)
                    #missing2 = max((goal2 - accumulated) / max(timeleft,0.0000000000000001) - current,0)
                    if missing > circ:# or missing2 > circ2:
                        missing = -1
                    # if missing2+missing ==0:
                    #     embed.add_field(name=question, value=f'0 Tokens missing for 5% Quorum', inline=False)
                    # else:
                    #     embed.add_field(name=question, value=f'{missing2:,.0f}-{missing:,.0f} Tokens missing for 5% Quorum', inline=False)
                    embed.add_field(name=question, value=f'{emoji} {missing:,.0f} missing for 5% Quorum', inline=False)
                    
                    for j in range(len(answers)):
                        answer = answers[j]
                        current = f'{emoji} {0.001*answer["current"]:,.0f} ({0.1*answer["current"]/circ:.2f}%)'#-{0.1*answer["current"]/circ2:.2f}%)'
                        projection = f'Projection: {0.1*(answer["accumulated"]+answer["current"] * (e["milestoneIndexEnd"]-min(max(e["milestone"], e["milestoneIndexStart"]), e["milestoneIndexEnd"])))/(circ*(e["milestoneIndexEnd"]-e["milestoneIndexStart"])):.2f}%'#-{0.1*(answer["accumulated"]+answer["current"] * (e["milestoneIndexEnd"]-min(max(e["milestone"], e["milestoneIndexStart"]), e["milestoneIndexEnd"])))/(circ2*(e["milestoneIndexEnd"]-e["milestoneIndexStart"])):.2f}%'
                        # total = f'{0.001*answer["accumulated"]:,.0f} {tok} ({0.1*answer["accumulated"]/(circ*mscnt):.2f}%)'
                        outstr = f'''{current}
                        {projection}'''
                        
                        embed.add_field(name=answer['text'], value=outstr)
                    if len(embed.fields) > 20:
                        await ctx.send(embed=embed)
                        embed = embed = discord.Embed(title=f'{e["name"]}', color=0xFF5733)
                        if 'lastUpdated' in e:
                            embed.timestamp = datetime.fromtimestamp(e["lastUpdated"])
                        embed.set_author(name="Tangle Treasury", url="https://www.tangletreasury.org/", icon_url="https://cdn.discordapp.com/icons/1212015097468424254/d68d92a0a149a6a121a7f0ecbfcc9459.png?size=240")

                if 'lastUpdated' in e:
                    footer = f'Based on circulating supply of {circ:,.0f} {tok}.\nLast update:'
                    if tok == 'IOTA':
                        footer = f'Based on circulating supply of {circ:,.0f} {tok} at event start.\nLast update:'
                    embed.set_footer(text=footer)
                await ctx.send(embed=embed)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('⛔')

@bot.command()
async def richlist(ctx, *args):
    if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
        try:
            async with session.get('https://chronicle.shimmer.network/api/explorer/v2/ledger/richest-addresses', timeout=10) as resp:
                smrrichlist = (await resp.json())['top']
            async with session.get('https://chronicle.stardust-mainnet.iotaledger.net/api/explorer/v2/ledger/richest-addresses', timeout=10) as resp:
                iotarichlist = (await resp.json())['top']
            with open("iota_richlist.json", "w") as file:
                json.dump(iotarichlist, file, indent=2)
            with open("smr_richlist.json", "w") as file:
                json.dump(smrrichlist, file, indent=2)
            await ctx.send(file=discord.File("iota_richlist.json"))
            await ctx.send(file=discord.File("smr_richlist.json"))
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.message.add_reaction('⛔')

# @bot.command(aliases=["c"])
# async def circulating(ctx, *args):
#     if ctx.channel.id in PCHANNELS or ctx.author.id in ADMINS:
#         try:
#             net_launch = 1681113738
#             now = time.time()
#             bi_weeks_passed = (now - net_launch) // (2*7*86400)
#             total = 2529939788+54896344+7664631+2*552000000*(0.1+0.9*min(bi_weeks_passed/208,1))+325469717*(0.1+0.9*min(bi_weeks_passed/208,1))+161000000*(0.1+0.9*min(bi_weeks_passed/104,1))+230000000*(0.1+0.9*min(bi_weeks_passed/104,1))
#             total2 = iota["circulating2"]
#             total3 = iota["circulating3"]
#             embed = discord.Embed(title='Circulating IOTA Supply', color=0xFF5733)

#             embed.add_field(value=f'{bi_weeks_passed:.0f} biweekly unlocks since 04.10.2023:', name = f'2,529,939,788 old tokens, 54,896,344 DAO +7,664,631 migrated tokens', inline=False)
#             embed.add_field(name=f'{552000000*(0.1+0.9*min(bi_weeks_passed/208,1)):,.0f} UAE, {552000000*(0.1+0.9*min(bi_weeks_passed/208,1)):,.0f} TEA unlocks', value='', inline=False)
#             embed.add_field(name=f'{325469717*(0.1+0.9*min(bi_weeks_passed/208,1)):,.0f} IF unlocks', value='', inline=False)
#             embed.add_field(name=f'{161000000*(0.1+0.9*min(bi_weeks_passed/104,1)):,.0f} Assembly unlocks', value='', inline=False)
#             embed.add_field(name=f'{230000000*(0.1+0.9*min(bi_weeks_passed/104,1)):,.0f} contributor unlocks', value='', inline=False)
#             embed.add_field(name=f'TOTAL: {total:,.0f} IOTA', value='', inline=False)
#             embed.add_field(name=f'Reported by Explorer: {total2:,.0f} IOTA', value='', inline=False)
#             embed.add_field(name=f'Reported by node: {total3:,.0f} IOTA', value='', inline=False)
#             await ctx.send(embed=embed)

#             embed = discord.Embed(title='Circulating SMR Supply', color=0xFF5733)
#             embed.add_field(name=f'Total Supply: {smr["supply"]:,.0f} SMR', value='', inline=False)
#             embed.add_field(name=f'Circulating reported by Coingecko: {smr["circulating"]:,.0f} SMR', value='', inline=False)
#             await ctx.send(embed=embed)
#             await ctx.message.add_reaction('✅')
#         except Exception as e:
#             await ctx.message.add_reaction('⛔')


# endregion 
            
async def main():
    # run thread to update liquidity positions
    asyncio.create_task(update_thread())

    # run thread to update p bot data
    asyncio.create_task(update_price())

    # run thread to update governance votings
    asyncio.create_task(update_votings())

    # single session for better performance
    global session
    session = aiohttp.ClientSession()

    # start bot - this will wait infinitely
    await bot.start(DISCORDTOKEN)

if __name__ == "__main__":
    asyncio.run(main()) 
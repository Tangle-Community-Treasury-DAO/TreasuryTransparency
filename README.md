# Discord bot for tangle treasury transparency

Requirements:
Python 3.10+

web3

discord.py

iota-sdk
```
pip3 install web3
pip3 install discord.py
pip3 install iota-sdk
```

You need to set your bot auth token in your environment:
```
export DISCORD_TOKEN = <insert your token here>
```

Invite your bot to your server and grant it access to all channels you want it to interact.

Set an admin channel's ID and superuser user IDs in the startup.cfg.

Add or remove an admin as superuser with:
```
!addadmin <user-id>
!deladmin <user-id>
```

You can add tokens / pools / farms in startup.cfg if you want to - but it is more convenient to add and delete those through bot commands in discord.

Then just run the bot:
```
python3 treasury_discord.py
````
All admin commands must be run by admins in the specified admin channel.

To add or remove a channel for p-interactions:
```
!addpchannel <channel id>
!delpchannel <channel id>
```
To add or remove a channel for balance-outputs:
```
!addtchannel <channel id>
!addtchannel <channel id>
```

To add or remove a wallet addresses to the watchlist:
```
!addwallet <wallet address>
!delwallet <wallet address>
```

To add or remove a regular ERC-20 token:
```
!addtoken <token address> <decimals>
!deltoken <token address>
```
`decimals` is the amount of decimals shown in the bot's output in discord.

For example to add SMR displaying 2 decimals:
```
!addtoken 0x1074010000000000000000000000000000000000 2
```

To add or remove uniswap V2 LP SCs to the watchlist:
```
!addv2lp <token address> <LP name>
!delv2lp <token address / name>
```
For example:
```
!addv2lp 0x95f00a7125EC3D78d6B2FCD6FFd9989941eF25fC ShimmerSea SMR-LUM
```
and remove it with
```
!delv2lp ShimmerSea SMR-LUM
```

To add or remove a lending SC to the watchlist:
```
!addlending <token address> <token> <name>
!dellending <token address / name>
```
For example:
```
!addlending 0x52F2a6f2B6151245f7F864F4E4aCC206202E4e6a 0x1074010000000000000000000000000000000000 DeepR SMR Lend
!dellending DeepR SMR
```

Simply add a farm SC to the watchlist with
```
!addfarm <farm address>
```

Force an update with:
```
!update
```

Or just post the most recent update with:
```
!output
```

Regular users can utilize the following commands:
`!p` for SMR and IOTA market data
`!convert <smr/iota wallet>` to convert a smr to an iota wallet address or vice versa
`!events <filter arguments>` to get current and previous governance voting events, for example
```
!events
!events IGP
!events 0x69
!events treasury
```

`!votes <filter arguments>` to get currently voting wallets. filter arguments can be wallet addresses or event filters. If no address filter is given, it will send a file with all wallets on the filtered events.
Here are a few examples:
```
!votes
!votes iota142392429
!votes iota144234234 treasury
!votes treasury
!votes iota12312 iota31232
```


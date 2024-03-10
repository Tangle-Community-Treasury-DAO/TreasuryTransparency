# Discord bot for tangle treasury transparency

You need web3 and discord.py:
```
pip3 install web3
pip3 install discord.py
```

You need to set your bot auth token in your environment:
```
export DISCORD_TOKEN = <insert your token here>
```

Set the channel ID in the startup.cfg that you want the bot to be run in.
Set admin IDs in startup.cfg
You can add tokens in startup.cfg if you want to - but you can also add and delete those through bot commands in discord.

Then just run the bot:
```
python3 treasury_discord.py
````
All commands must be run by admins in the specified channel.
To add a regular ERC-20 token:
```
!addtoken <token address> <decimals>
```
`decimals` is the amount of decimals shown in the bot's output in discord.
For example to add SMR displaying 2 decimals:
```
!addtoken 0x1074010000000000000000000000000000000000 2
```

To remove a regular ERC-20 token:
```
!deltoken <token address>
```

Include LP deposits by adding LP tokens:
```
!addlp <token address> <LP name>
```
For example:
```
!addlp 0x95f00a7125EC3D78d6B2FCD6FFd9989941eF25fC ShimmerSea SMR-LUM
```
And remove them with:
```
!dellp <token address>
```

To include more wallet addresses:
```
!addwallet <wallet address>
```
and remove them with:
```
!delwallet <wallet address>
```

Post an update with:
```
!update
```

Lending and limit order positions will be added soon.



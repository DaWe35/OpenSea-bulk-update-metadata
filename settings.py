## Mainnet chains:
#   - arbitrum
#   - avalanche
#   - bsc
#   - ethereum
#   - klaytn
#   - optimism
#   - matic
#   - solana
## Testnet chains:
#   - arbitrum-goerli
#   - avalanche-fuji
#   - bsc-testnet
#   - baobab
#   - goerli
#   - mumbai
#   - optimism-goerli
#   - soldev
CHAIN = 'matic'

# contract address
CONTRACT_ADDRESS = '0x70e4014c46a26d3130f85dabff65cf0446a06f13'

 # Put an array here with all NFTs you want to update
 # list(range(x,y)) will generate an array from x to y like this: [1, 2, 3, ..., 999, 1000]
ASSET_LIST = list(range(11, 1000))

# show more logs
VERBOSE = False

# skip assets what are already indexed by OpenSea (only index assets with "content unavailable yet" label)
SKIP_INDEXED = False

# Error file name
ERROR_FILE_NAME = "errors.txt"

# Save errors in a file
SAVE_IN_FILE = False

# Refresh assets from the error file
REFRESH_FROM_FILE = False

# Automatically get the good url for the selected chain
chains = {
    "https://opensea.io/assets": [ # Mainnet
        "arbitrum",
        "avalanche",
        "bsc",
        "ethereum",
        "klaytn",
        "optimism",
        "matic",
        "solana"
    ],
    "https://testnets.opensea.io/assets": [    # Testnet
        "arbitrum-goerli",
        "avalanche-fuji",
        "bsc-testnet",
        "baobab",
        "goerli",
        "mumbai",
        "optimism-goerli",
        "soldev"
    ]
}

try:
    URL = [url for url, names in chains.items() if CHAIN in names][0]
except:
    print("[-] Unknown chain")
    print("\tPlease check that you entered a chain from the supported chain list")
    print("\tOpen an issue if you still have a problem")
    quit("Quitting...")
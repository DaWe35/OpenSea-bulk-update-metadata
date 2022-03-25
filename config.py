# chain (ethereum or matic)
CHAIN = 'matic'

# contract address
CONTRACT_ADDRESS = '0x70e4014c46a26d3130f85dabff65cf0446a06f13'

 # Put an array here with all NFTs you want to update
 # list(range(x,y)) will generate an array from x to y like this: [1, 2, 3, ..., 999, 1000]
ASSET_LIST = list(range(11, 1000))

# show more logs
VERBOSE = False

# skip assets what are already indexed by OpenSea (only index assets with "content unavailable yet" label)
SKIP_INDEXED = True
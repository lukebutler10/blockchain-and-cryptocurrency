NANOSECONDS = 1
MICROSECONDS = 1000 * NANOSECONDS
MILLISECONDS = 1000 *MICROSECONDS
SECONDS = 1000 * MILLISECONDS

#We do this^ because the "time" module has a useful method time.ns which works in nanoseconds

MINE_RATE = 4 * SECONDS

STARTING_BALANCE = 1000

MINING_REWARD = 50
MINING_REWARD_INPUT = {'address':'*--official-mining-reward--*'} #this will be the Transaction.input parameter of the Transaction object
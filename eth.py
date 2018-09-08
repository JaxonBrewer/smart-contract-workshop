from getpass import getpass
from solc import compile_source
from web3 import Web3, IPCProvider
from web3.contract import ConciseContract

DEFAULT_UNLOCK = 20


class PyEth(object):
	def __init__(self, ipc_path):
		""" Creates an ethereum interface for interacting with the ethereum blockchain

		param ipc_path: Path the geth.ipc file for your geth client
		"""
		self.w3 = Web3(IPCProvider(ipc_path))
		self.main_account = self.w3.eth.accounts[0]
		self.deployed_contracts = {}

	def add_contract(self, contract_address, abi):
		""" add an existing contract at contract address to deployed_contracts
		
		:params contract_address: ethereum address contract was deployed at
		:params abi: application binary interface for contract
		:returns ConsiceContract object
		"""
		deployed_contract = self.w3.eth.contract(address=contract_address, abi=abi)
		contract = ConciseContract(deployed_contract)
		self.deployed_contracts[contract_address] = (contract, abi)
		return contract

	def unlock(self, passphrase=None, duration=DEFAULT_UNLOCK):
		""" unlock main account

		:param passphrase: 
		:param duration: time account will be unlock for in seconds
		"""
		# prompt for passphrase if not pass in
		if passphrase is None:
			passphrase = getpass('Passphrase:')
		self.w3.personal.unlockAccount(self.main_account, passphrase, duration)

	def deploy(self, contract_source, contract_name, *args, passphrase=None, gas=410000):
		""" Compile and deploy a smart contract to the blockchain

		:param contract_source: The contract to compile and deploy as a string
		:param contract_name: Name of the main contract
		:param args: arguements to pass to contract constructor
		:param passphrase: Passphrase to unlock account, will prompt if None
		:param gas: gas limit for contract deploy transaction
		:returns (ConciseContract, abi) for contract deployed
		"""
		# Compile our contract from source
		compiled_sol = compile_source(contract_source)
		contract_interface = compiled_sol['<stdin>:{}'.format(contract_name)]
		abi = contract_interface['abi']
		contract = self.w3.eth.contract(abi=abi, bytecode=contract_interface['bin'])

		# Unlock account and deploy contract
		self.unlock(passphrase, duration=5)
		tx_hash = contract.deploy(
		transaction={'from': self.main_account, 'gas': gas}, args=args)

		# Wait for contract to be mined and get address
		print('Waiting for contract to be mined...')
		tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
		contract_address = tx_receipt['contractAddress']
		print('Contract mined, address: {}'.format(contract_address))

		# Return contract
		contract_instance = self.w3.eth.contract(address=contract_address, abi=abi)
		deployed_contract = ConciseContract(contract_instance)

		self.deployed_contracts[contract_address] = (deployed_contract, abi)
		return deployed_contract, abi

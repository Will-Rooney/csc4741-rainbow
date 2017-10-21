# Cyber Security - CSCI 4741
# Group Project - Rainbow Tables
#
# Author:
#	William Rooney
#
# Team Members:
#	William Rooney
#	Howard Van Dam
#	Jonathan Trejo
#
# Written in python 3.4.4
#	For 2.7 change '_thread' to 'thread'
#

import hashlib, base64, re, os, math, _thread, timeit
from itertools import product
from string import ascii_lowercase, digits
from time import sleep

debug = False

class RainbowTable:
	def __init__(self, k=100, strLength=4, generate=True):

		"""
		RainbowTable Class: builds a rainbow table with k
		reduction functions and k rainbow table entries. Each chain's starting
		plaintext consists of strLength characters of the set [0-9].
		"""
		self.k = k
		self.strLength = strLength
		self.table = {}

		# Create a set of all possible password of length strLength
		if generate: self.passwordSet = [''.join(p) for p in product(digits, repeat=self.strLength)]

	def load(self, fileName):
		"""
		Load a pre-computed rainbow table.
		The first line contains the k value
		an entry contains start and end values that are comma delimited
		each entry in the table is newline delimited
		"""
		try:
			infile = open(fileName, 'r')
			self.k = int(next(infile))
			for line in infile:
				try:
					line = line.strip('\n')
					data = line.split(',')
					self.table[data[0]] = data[1]
				except IndexError:
					print ('Error: Invalid file contents in file:',fileName)
					return
			infile.close()
		except IOError:
			print ('Error: Could not read file:',fileName)

	def save(self, fileName=None):
		"""
		Save the current rainbow table.
		The first line contains the k value
		an entry contains start and end values that are comma delimited
		each entry in the table is newline delimited
		"""
		if fileName == None:
			fileName = 'rainbowTable_len' + str(self.strLength) + '_k' + str(self.k) + '.txt'
		try:
			outfile = open(fileName, 'w')
			outfile.write('%s\n' % str(self.k))
			for start, end in self.table.items():
				outfile.write('%s,%s\n' % (start, end))
			outfile.close()
		except IOError:
			print ('Error: Could not write to file:',fileName)


	def generate(self):
		""" Generate a Rainbow Table with the character set [0-9] or [a-z]; Randomly generate inputs or load inputs from line delimited file """

		for plaintext_Start in self.passwordSet:	
			# Generate Chain
			plaintext_End = plaintext_Start
			for i in range(self.k):
				hash_object = hashlib.md5(plaintext_End.encode())	# Create hash
				plaintext_End = self.R(i, hash_object.hexdigest())	# Reduce to numeric plaintext
			if plaintext_End not in self.table.values():
				self.table[plaintext_Start] = plaintext_End			# If final hash has not been used then add the starting plaintext and ending plaintext to the table

	def R(self, i, hash_object): # Play with this function to find better rainbow table generations
		""" Reduction function #i : Return a plaintext string of length strLength that contains characters [0-9] """
		val = (int(''.join(re.findall("[0-9]+",hash_object))) + i) % 10**self.strLength	# Extract all digits from hash and add i
		plaintext = str(val) 						# Convert back to string
		while len(plaintext) < self.strLength:		# Format String
			plaintext = "0" + plaintext
		return plaintext[-self.strLength:]			# Return last 'strLength' characters of string

	def crack(self,passHash):
		newHash = passHash
		iteration = 1
		passPlaintext = ''
		for iteration in range(self.k):
			for i in range(iteration+1): # Apply R(k-iteration) through R(k) reduction functions on hash
				passPlaintext = self.R(i+(self.k-1-iteration), newHash)
				newHash = hashlib.md5(passPlaintext.encode()).hexdigest()
			for key, val in self.table.items():
				if (passPlaintext == val): # Found a matching end value in rainbow table
					# Generate chain from key
					newPlaintext = key
					for j in range(self.k):
						newHash = hashlib.md5(newPlaintext.encode()).hexdigest()
						if newHash == passHash:
							self.password = newPlaintext
							return True # Found the matching password
						newPlaintext = self.R(j, newHash)
		return False # Failed to find a match

	def reset(self):
		self.table = {}

	def getK(self, minK=2):
		""" Find most optimal k value for rainbow table generation """
		self.reset()
		self.k = maxK = int(math.sqrt(10**self.strLength)) # setting max k to the square root of the number of possible combonations; k length chains * k length rainbow table ~ k^2 plaintexts analyzed
		bestK = 0
		maxSuccess = 0
		bestTableSize = 0
		bestResults = []
		while self.k >= minK:
			self.generate()
			successCount = 0
			for password in self.passwordSet:
				passHash = hashlib.md5(password.encode())
				if self.crack(passHash.hexdigest()):
					successCount += 1
			if successCount >= maxSuccess:
				maxSuccess = successCount
				bestK = self.k
				bestTableSize = len(self.table)
				result = [bestK, bestTableSize, (float(maxSuccess)/len(self.passwordSet))*100]
				bestResults.append(result)
				self.save()
			self.reset()
			self.k -= 1
		return bestResults

"""
----------------------------------------------------------------------------------------------
  TESTS
----------------------------------------------------------------------------------------------
"""
def findBestK(strLen=1):
	#print ('Getting best table for passwords of length:',strLen)
	rainbowTable = RainbowTable(strLength=strLen)
	result1 = rainbowTable.getK()
	print ('Optimal tables for passwords of length: %s' % strLen)
	for result in reversed(result1):
		print ('k:',result[0],'\t TableSize:',result[1],'\t Percent cracked:',result[2],'%')
	print()

def findBestKThreaded():
	try:
		_thread.start_new_thread(findBestK, (1,))
		sleep(1)
		_thread.start_new_thread(findBestK, (2,))
		
		_thread.start_new_thread(findBestK, (3,))
		_thread.start_new_thread(findBestK, (4,))
		_thread.start_new_thread(findBestK, (5,))
	except:
		print ('Error: unable to start thread')

	while 1:
		pass


def crackPass(passHash):
	# Try two 3 character rainbow tables
	rainbowTable1 = RainbowTable(31,3,False)
	rainbowTable2 = RainbowTable(30,3,False)

	rainbowTable1.load('rainbowTable_len3_k31.txt')
	print ('Attempting to crack 3 character password with hash:',passHash)
	if rainbowTable1.crack(passHash):
		print ('Found password:',rainbowTable1.password,'\n')
		return
	else:
		print ('Attack failed: trying new table')
		rainbowTable2.load('rainbowTable_len3_k30.txt')
		if rainbowTable2.crack(passHash):
			print ('Found password:',rainbowTable2.password,'\n')
			return
		else:
			print ('Three character password attack failed\n')

	# Try two 4 character rainbow tables
	rainbowTable3 = RainbowTable(100,4,False)
	rainbowTable4 = RainbowTable(99,4,False)

	rainbowTable3.load('rainbowTable_len4_k100.txt')
	print ('Attempting to crack 4 character password with hash:',passHash)
	if rainbowTable3.crack(passHash):
		print ('Found password:',rainbowTable3.password,'\n')
		return
	else:
		print ('Attack failed: trying new table')
		rainbowTable4.load('rainbowTable_len4_k99.txt')
		if rainbowTable4.crack(passHash):
			print ('Found password:',rainbowTable4.password,'\n')
			return
		else:
			print ('Four character password attack failed\n')

"""
findBestK(1)
findBestK(2)
findBestK(3)
findBestK(4)
findBestK(5)
"""
#findBestKThreaded()

#"""
#password = '8794'
#passHash = hashlib.md5(password.encode()).hexdigest()
passHash = '81dc9bdb52d04dc20036dbd8313ed055'

if os.name == 'nt': os.system('cls')
else: os.system('clear')

start = timeit.default_timer()
crackPass(passHash)
stop = timeit.default_timer()

print ('Execution time:',stop-start,'seconds')
#"""

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

import hashlib, base64, re, os, math
from itertools import product
from string import ascii_lowercase, digits
from time import sleep

debug = False # Further testing needed

class RainbowTable:
	def __init__(self, tableSize=100, k=100, strLength=4, buildTable = True, isAlpha = False):

		"""
		RainbowTable Class: builds a rainbow table with k
		reduction functions and k chains. Each chain's starting
		plaintext ranges from 1 to strLength characters of the set
		of a lowercase alphabet.
		"""
		self.tableSize=tableSize
		self.k = k
		self.strLength = strLength
		self.table = {}
		self.buildTable = buildTable;

		self.isAlpha = isAlpha
		if isAlpha:
			self.charSetSize = 26
		else:
			self.charSetSize = 10

		self.hashPercent = 0

	def generate(self, fileName=None):
		""" Generate a Rainbow Table with the character set [0-9] or [a-z]; Randomly generate inputs or load inputs from line delimited file """
		if debug: print ('Call to generate():')
		hashCalls = 0
		self.inputData = []
		# Load password list
		if fileName is not None and not self.buildTable:
			# table generation from file
			self.inputData = []
			file = open(fileName, 'r')
			for line in file:
				line = line.strip('\n')
				self.inputData.append(line)
			file.close()

		iteration = 0
		# Create a set of all possible password of length strLength
		self.charSet = []
		if self.isAlpha:
			self.charSet = [''.join(p) for p in product(ascii_lowercase, repeat=self.strLength)]
		else:
			self.charSet = [''.join(p) for p in product(digits, repeat=self.strLength)]

		while len(self.table) < self.tableSize: # Loop through password set until the rainbow table is full or input is has expired
			#if debug: print 'Percent Complete:',str(int((float(len(self.table))/self.tableSize)*100)) + '%\tPercent Searched:',str(int((float(iteration)/(self.charSetSize**self.strLength))*100))+'%\tHashCalls:',str(int((float(hashCalls)/(self.charSetSize**self.strLength))*100))+'%'
			
			# Get starting plaintext for chain
			if self.buildTable: # use input from generated set
				if iteration >= len(self.charSet):
					if debug: print ("Failed to fill out table")
					return
				plaintext_Start = self.charSet[iteration]
				#if debug: print 'newPlaintext1'
			else: # use input from file
				if iteration >= len(self.inputData):
					# Exhausted file input, generating rest of input
					if debug: print ("Failed to fill out table")
					self.buildTable = True
					iteration = 0
					plaintext_Start = self.charSet[iteration]
				else:
					plaintext_Start = self.inputData[iteration]
				#if debug: print 'newPlaintext2'

			# Generate Chain
			plaintext_End = plaintext_Start
			for i in range(self.k):
				hash_object = hashlib.md5(plaintext_End.encode())				# Create hash
				hashCalls += 1
				#if debug: print 'new hash'
				if self.isAlpha:
					plaintext_End = self.R_alpha(i, hash_object.hexdigest())	# Reduce to alphabetic plaintext
				else:
					plaintext_End = self.R_num(i, hash_object.hexdigest())		# Reduce to numeric plaintext
				#if debug: print 'newPlaintext3'
			if debug: print (plaintext_Start,'-->',plaintext_End,'-->',hash_object.hexdigest())
			hash_end = hashlib.md5(plaintext_End.encode()).hexdigest()			# Get final hash
			hashCalls += 1
			if hash_end not in self.table.values():
				self.table[plaintext_Start] = hash_end							# If final hash has not been used then add the starting plaintext and ending hash to the table
			#sleep(3)
			iteration += 1

			#if debug: 
				#if os.name == 'nt': os.system('cls')
				#else: os.system('clear')
		self.hashPercent += (float(hashCalls)/(self.charSetSize**self.strLength))*100

	def load(self, fileName):
		""" Load pre-existing Rainbow Table - Not Tested """
		self.inputData = []
		file = open(fileName, 'r')
		for line in file:
			line = line.strip('\n')
			data = line.split(',')
			self.table[data[0]] = data[1]
		file.close()
		self.k = len(self.table)

	def R_alpha(self, i, hash_object):
		""" Reduction function #i --- NEEDS IMPROVEMENT : Majority of chains are ending on similar values"""
		hash_object = str(hash_object) + str(i)
		hash_value = int(hash_object,16)
		hash_value = (hash_value+i) % (26**self.strLength)
		plaintext = self.num_to_alpha(hash_value)
		#print hash_object,'-->',hash_value,'-->',plaintext[-self.strLength:]
		#sleep(0.1)
		temp = 0
		while len(plaintext) < self.strLength:
			#if debug: print 'looking for plaintext',plaintext
			plaintext = self.num_to_alpha(hash_value+i+temp)
			temp += 1
		#print 'found:',plaintext
		return plaintext[-self.strLength:]
		#i = i+2
		#hash_object = str(hash_object) + str(i*i)
		#plaintext = self.num_to_alpha(hash_object)
		#return plaintext[-self.strLength:]

	def num_to_alpha(self, num):
		b64 = base64.b64encode(str(num).encode('ascii'))
		return (''.join(re.findall("[a-z]+",b64.decode('utf-8')))).lower()

	def R_num(self, i, hash_object):
		""" Reduction function #i """
		plaintext = ''.join(re.findall("[0-9]+",hash_object))[-self.strLength:]		# Extract all digits from
		val = int(plaintext)+i 														# Add i
		plaintext = str(val) 														# Convert back to string
		while len(plaintext) < self.strLength:										# Format String
			plaintext = "0" + plaintext
		if len(plaintext) > self.strLength:
			plaintext = plaintext[-self.strLength:]									# Return last 'strLength' characters of string
		return plaintext

	def crack(self,passHash):
		newHash = passHash
		iteration = 1
		passPlaintext = ''
		for iteration in range(self.k):
			for i in range(iteration+1):
				if self.isAlpha: passPlaintext = self.R_alpha(i+(self.k-1-iteration), newHash.hexdigest())
				else: passPlaintext = self.R_num(i+(self.k-1-iteration), newHash.hexdigest())
				newHash = hashlib.md5(passPlaintext.encode())
			#if debug: print ('Iteration:',iteration+1,'-->',newHash.hexdigest())
			for key, val in self.table.items():
				if (newHash.hexdigest() == val):
					#if debug: print ('Match found!')
					# Generate chain from key
					newPlaintext = key
					#if debug: print ('key --> val :',key,'-->',val)
					for j in range(self.k):
						newHash = hashlib.md5(newPlaintext.encode())
						if newHash.hexdigest() == passHash.hexdigest():
							self.password = newPlaintext
							#if debug: print ('Success!')
							return True
						tempPlaintext = ''
						if self.isAlpha: tempPlaintext = self.R_alpha(j, newHash.hexdigest())
						else: tempPlaintext = self.R_num(j, newHash.hexdigest())
						#if debug: print ('\t',newPlaintext,'-->',newHash.hexdigest(),'-->',tempPlaintext)
						newPlaintext = tempPlaintext
		return False

	def reset(self):
		self.table = {}




""" -----------------------------------------------------------------------------------------------------------
	TESTS
	----------------------------------------------------------------------------------------------------------- """
def test(password, buildTable=True, isAlpha=False, fileName=None):
	rainbowTable = RainbowTable(5, 5,1, buildTable, isAlpha)

	passHash = hashlib.md5(password.encode())

	searching = True
	maxK=rainbowTable.charSetSize**rainbowTable.strLength
	print ("Cracking the password hash:",passHash.hexdigest())
	print ('Increasing table string length to',rainbowTable.strLength)
	while searching:
		rainbowTable.reset()
		rainbowTable.generate(fileName)
		#print ('Generated Rainbow Table with',rainbowTable.k,'reduction functions and chains using a max of',rainbowTable.strLength,'digits from 0-9.\n')
		if rainbowTable.crack(passHash):
			print ('Password found:',rainbowTable.password)
			print ('Actual password:',password)
			print 'actual table size:',len(rainbowTable.table),'k:',rainbowTable.k,'hash %:',rainbowTable.hashPercent
			searching = False
		else:
			#print ('Attack Failed: increasing k')
			rainbowTable.k += 1
			rainbowTable.tableSize += 1
			if rainbowTable.k > maxK:
				rainbowTable.strLength += 1
				if rainbowTable.strLength == 2: maxK = math.sqrt(rainbowTable.charSetSize**rainbowTable.strLength)*2
				elif rainbowTable.strLength > 2: maxK = math.sqrt(10**rainbowTable.strLength)
				else: maxK=rainbowTable.charSetSize**rainbowTable.strLength
				print ('Increasing table string length to',rainbowTable.strLength)
				if rainbowTable.strLength > len(password):
					print ('Attacked Failed')
					searching = False

def testR(password):
	rainbowTable = RainbowTable(10,4,True,True)
	passHash = hashlib.md5(password.encode())
	print 'Hash:',passHash
	for i in range (rainbowTable.k):
		plaintext = rainbowTable.R_alpha(i, passHash.hexdigest())
		print 'R' + str(i) + ':',plaintext

def testSingleTable(password, tableSize,k):
	rainbowTable = RainbowTable(tableSize,k,len(password), False, True)
	passHash = hashlib.md5(password.encode())

	print ("Cracking the password hash:",passHash.hexdigest())
	rainbowTable.generate('four_char_passwords_500')
	#print ('Generated Rainbow Table with',rainbowTable.k,'reduction functions and chains using a max of',rainbowTable.strLength,'digits from 0-9.\n')
	if rainbowTable.crack(passHash):
		print ('Password found:',rainbowTable.password)
		print ('Actual password:',password)
	else:
		print ('Attack Failed')




# Numeric password
password = '1234'
test(password, True, False, None)

#print()

# Alphabetic (lowercase) password
password = 'code'
test(password, False, True, "four_char_passwords_500")

# Test Reduction - alpha
#password = 'pass'
#testR(password)

# Test single table
#testSingleTable('pass', 169, 169)
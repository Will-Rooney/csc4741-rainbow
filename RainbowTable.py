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

debug = False # Further testing needed

class RainbowTable:
	def __init__(self, k=100, strLength=4, buildTable = True, isAlpha = False):

		"""
		RainbowTable Class: builds a rainbow table with k
		reduction functions and k chains. Each chain's starting
		plaintext ranges from 1 to strLength characters of the set
		of a lowercase alphabet.
		"""
		self.k = k
		self.strLength = strLength
		self.table = {}
		self.buildTable = buildTable;

		self.isAlpha = isAlpha
		if isAlpha:
			self.charSetSize = 26
		else:
			self.charSetSize = 10

	def generate(self, fileName=None):
		""" Generate a Rainbow Table with the character set [0-9]; Randomly generate inputs or load inputs from line delimited file """
		if debug: print ('Call to generate_num():')

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
		if self.buildTable:
			# Create a set of all possible password of length strLength
			self.charSet = []
			if self.isAlpha:
				self.charSet = [''.join(p) for p in product(ascii_lowercase, repeat=self.strLength)]
			else:
				self.charSet = [''.join(p) for p in product(digits, repeat=self.strLength)]

		while len(self.table) < self.k: # Loop through password set until the rainbow table is full or input is has expired
			if debug: print ('Generation',self.k,'- Percent Complete:',int((float(len(self.table))/self.k)*100),'%\nGeneration',self.k,'- Percent Searched:',int((float(iteration)/(self.charSetSize**self.strLength))*100),'%')
			
			# Get starting plaintext for chain
			if self.buildTable: # use input from generated set
				if iteration >= len(self.charSet):
					if debug: print ("Failed to fill out table")
					return
				plaintext_Start = self.charSet[iteration]
			else: # use input from file
				if iteration >= len(inputData):
					if debug: print ("Failed to fill out table")
					return
				plaintext_Start = self.inputData[iteration]

			# Generate Chain
			plaintext_End = plaintext_Start
			for i in range(self.k):
				hash_object = hashlib.md5(plaintext_End.encode())				# Create hash
				if self.isAlpha:
					plaintext_End = self.R_alpha(i, hash_object.hexdigest())	# Reduce to alphabetic plaintext
				else:
					plaintext_End = self.R_num(i, hash_object.hexdigest())		# Reduce to numeric plaintext
			if debug: print (plaintext_Start,'-->',hash_object.hexdigest())
			hash_end = hashlib.md5(plaintext_End.encode()).hexdigest()			# Get final hash
			if hash_end not in self.table.values():
				self.table[plaintext_Start] = hash_end							# If final hash has not been used then add the starting plaintext and ending hash to the table
			iteration += 1

			if debug: 
				if os.name == 'nt': os.system('cls')
				else: os.system('clear')

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
		hash_value = int(hash_object,16)
		hash_value = (hash_value+i) #% (26**self.strLength)
		plaintext = self.num_to_alpha(hash_value)
		return plaintext[-self.strLength:]

	def num_to_alpha(self, num):
		b64 = base64.b64encode(str(num).encode('ascii'))
		return (''.join(re.findall("[a-zA-z]+",b64.decode('utf-8')))).lower()

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
			if debug: print ('Iteration:',iteration+1,'-->',newHash.hexdigest())
			for key, val in self.table.items():
				if (newHash.hexdigest() == val):
					if debug: print ('Match found!')
					# Generate chain from key
					newPlaintext = key
					if debug: print ('key --> val :',key,'-->',val)
					for j in range(self.k):
						newHash = hashlib.md5(newPlaintext.encode())
						if newHash.hexdigest() == passHash.hexdigest():
							self.password = newPlaintext
							if debug: print ('Success!')
							return True
						tempPlaintext = ''
						if self.isAlpha: tempPlaintext = self.R_alpha(j, newHash.hexdigest())
						else: tempPlaintext = self.R_num(j, newHash.hexdigest())
						if debug: print ('\t',newPlaintext,'-->',newHash.hexdigest(),'-->',tempPlaintext)
						newPlaintext = tempPlaintext
		return False

	def reset(self):
		self.table = {}




""" -----------------------------------------------------------------------------------------------------------
	TESTS
	----------------------------------------------------------------------------------------------------------- """
def test(password,isAlpha=False):
	rainbowTable = RainbowTable(5,1, True, isAlpha)

	passHash = hashlib.md5(password.encode())

	searching = True
	maxK=rainbowTable.charSetSize**rainbowTable.strLength
	print ("Cracking the password hash:",passHash.hexdigest())
	print ('Increasing table string length to',rainbowTable.strLength)
	while searching:
		rainbowTable.reset()
		rainbowTable.generate()
		#print ('Generated Rainbow Table with',rainbowTable.k,'reduction functions and chains using a max of',rainbowTable.strLength,'digits from 0-9.\n')
		if rainbowTable.crack(passHash):
			print ('Password found:',rainbowTable.password)
			print ('Actual password:',password)
			searching = False
		else:
			#print ('Attack Failed: increasing k')
			rainbowTable.k += 1
			if rainbowTable.k > maxK:
				rainbowTable.strLength += 1
				if rainbowTable.strLength == 2: maxK = math.sqrt(rainbowTable.charSetSize**rainbowTable.strLength)*2
				elif rainbowTable.strLength > 2: maxK = math.sqrt(10**rainbowTable.strLength)
				else: maxK=rainbowTable.charSetSize**rainbowTable.strLength
				print ('Increasing table string length to',rainbowTable.strLength)
				if rainbowTable.strLength > len(password):
					print ('Attacked Failed')
					searching = False


# Numeric password
password = '1234'
test(password,False)

print()

# Alphabetic (lowercase) password
password = 'code'
test(password,True)
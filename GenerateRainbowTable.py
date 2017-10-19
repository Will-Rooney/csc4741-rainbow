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

class RainbowTable:
	def __init__(self, k=100, strLength=4):

		"""
		RainbowTable Class: builds a rainbow table with k
		reduction functions and k rainbow table entries. Each chain's starting
		plaintext consists of strLength characters of the set [0-9].
		"""
		self.k = k
		self.strLength = strLength
		self.table = {}

		# Create a set of all possible password of length strLength
		self.passwordSet = [''.join(p) for p in product(digits, repeat=self.strLength)]

	def generate(self):
		""" Generate a Rainbow Table with the character set [0-9] or [a-z]; Randomly generate inputs or load inputs from line delimited file """

		for plaintext_Start in self.passwordSet:	
			if len(self.table) == self.k:
				return True # Rainbow table successfully filled out

			# Generate Chain
			plaintext_End = plaintext_Start
			for i in range(self.k):
				hash_object = hashlib.md5(plaintext_End.encode())	# Create hash
				plaintext_End = self.R(i, hash_object.hexdigest())	# Reduce to numeric plaintext
			if plaintext_End not in self.table.values():
				self.table[plaintext_Start] = plaintext_End			# If final hash has not been used then add the starting plaintext and ending plaintext to the table
			
		return False # Failed to fill out entire rainbow table


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
				passPlaintext = self.R(i+(self.k-1-iteration), newHash.hexdigest())
				newHash = hashlib.md5(passPlaintext.encode())
			for key, val in self.table.items():
				if (passPlaintext == val): # Found a matching end value in rainbow table
					# Generate chain from key
					newPlaintext = key
					for j in range(self.k):
						newHash = hashlib.md5(newPlaintext.encode())
						if newHash.hexdigest() == passHash.hexdigest():
							self.password = newPlaintext
							return True # Found the matching password
						newPlaintext = self.R(j, newHash.hexdigest())
		return False # Failed to find a match

	def reset(self):
		self.table = {}

	def getK(self):
		""" Find most optimal k value for rainbow table generation """
		self.reset()
		self.k = 1
		maxK = math.sqrt(10**self.strLength) # setting max k to the square root of the number of possible combonations; k length chains * k length rainbow table ~ k^2 plaintexts analyzed
		bestK = 0
		maxSuccess = 0
		while self.k <= maxK:
			self.generate()
			successCount = 0
			for password in self.passwordSet:
				passHash = hashlib.md5(password.encode())
				if self.crack(passHash):
					successCount += 1
			if successCount > maxSuccess:
				maxSuccess = successCount
				bestK = self.k
			self.reset()
			self.k += 1
		print ('Best k:',bestK,'\nPercent of passwords cracked:',(float(maxSuccess)/len(self.passwordSet))*100,'%')
		return bestK

""" -----------------------------------------------------------------------------------------------------------
	TESTS
	----------------------------------------------------------------------------------------------------------- """
def findBestK():
	print ('Getting best table for passwords of length: 1')
	rainbowTable1 = RainbowTable(strLength=1)
	k1 = rainbowTable1.getK()
	print ('\nGetting best table for passwords of length: 2')
	rainbowTable2 = RainbowTable(strLength=2)
	k1 = rainbowTable2.getK()
	print ('\nGetting best table for passwords of length: 3')
	rainbowTable3 = RainbowTable(strLength=3)
	k1 = rainbowTable3.getK()
	print ('\nGetting best table for passwords of length: 4')
	rainbowTable4 = RainbowTable(strLength=4)
	k1 = rainbowTable4.getK()
	print ('\nGetting best table for passwords of length: 5')
	rainbowTable5 = RainbowTable(strLength=5)
	k1 = rainbowTable5.getK()

findBestK()

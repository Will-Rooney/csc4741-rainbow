# Cyber Security - CSCI 4741
# Group Project - Rainbow Tables
#
# Authors:
#   William Rooney
#	Howard Van Dam
#	Jonathan Trejo

from random import choice
import random
from string import ascii_lowercase
import hashlib
import base64
import re

debug = True # Further testing needed

class RainbowTable:
	def __init__(self, k=100, maxLength=4):

		"""
		RainbowTable Class: builds a rainbow table with k
		reduction functions and k chains. Each chain's starting
		plaintext ranges from 1 to maxLength characters of the set
		of a lowercase alphabet.
		"""
		self.k = k
		self.maxLength = maxLength
		self.table = {}

	def generate(self):
		if debug: print ('Call to generate():')
		while len(self.table) <= self.k:
			chainStrLen = random.randint(1,self.maxLength)
			plaintext_Start = ''.join(choice(ascii_lowercase) for i in range(chainStrLen))
			while plaintext_Start in self.table:
				plaintext_Start = ''.join(choice(ascii_lowercase) for i in range(chainStrLen))
			if debug: print (plaintext_Start)
			plaintext_End = plaintext_Start
			for i in range(self.k):
				hash_object = hashlib.md5(plaintext_End.encode())
				plaintext_End = self.R(chainStrLen, i, hash_object.hexdigest())
				if debug: print (hash_object.hexdigest(),'->',plaintext_End)
			if plaintext_End not in self.table.values():
				self.table[plaintext_Start] = plaintext_End
				if debug: print ('\n')

	def R(self, strLen, i, hash_object):
		hash_value = int(hash_object,16)
		hash_value = hash_value + i*random.randint(1,100) + i # Generate Ri
		plaintext = base64.b32encode(str(hash_value).encode('ascii'))
		plaintext = plaintext.lower()
		plaintext = plaintext.decode('utf-8')
		plaintext = ''.join(re.findall("[a-z]+",plaintext))
		return plaintext[-strLen:]


	def testR(self):
		plaintext = 'test'
		hash_object = hashlib.md5(plaintext.encode())
		print (plaintext)
		print (hash_object.hexdigest())
		for i in range(self.k):
			newText = self.R(len(plaintext),i,hash_object.hexdigest())
			print ('R'+str(i)+':\t',newText)

if debug:
	rainbowTable = RainbowTable(k=100,maxLength=4)
	#rainbowTable.testR()
	rainbowTable.generate()
	print ('Generating Rainbow Table with',rainbowTable.k,'reduction functions and chains using a max of',rainbowTable.maxLength,'lowercase alphabet characters.\n')
	print (rainbowTable.table.items())
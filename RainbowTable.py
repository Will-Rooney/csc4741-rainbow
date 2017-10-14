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
import os
import time

debug = True # Further testing needed

class RainbowTable:
	def __init__(self, k=100, strLength=4, randomTable = False):

		"""
		RainbowTable Class: builds a rainbow table with k
		reduction functions and k chains. Each chain's starting
		plaintext ranges from 1 to strLength characters of the set
		of a lowercase alphabet.
		"""
		self.k = k
		self.strLength = strLength
		self.table = {}
		self.randomTable = randomTable;

	def generate(self, fileName=None):
		""" Generate a Rainbow Table; Randomly generate inputs or load inputs from line delimited file """
		if debug: print ('Call to generate():')

		# Load password list
		if fileName is not None and not self.randomTable:
			# table generation from file
			self.inputData = []
			file = open(fileName, 'r')
			for line in file:
				line = line.strip('\n')
				self.inputData.append(line)
			file.close()
			self.k = len(self.inputData)
			if debug:
				for s in self.inputData:
					print (s)
				print ('k =',self.k)

		iteration = 0
		while len(self.table) < self.k:
			if debug: print ('Generation - Percent Complete:',(float(len(self.table))/self.k)*100,'%')
			
			# Get starting plaintext for chain
			#if iteration >= self.k: time.sleep(100000)
			if iteration >= self.k or self.randomTable:
				# random table generation
				plaintext_Start = ''.join(choice(ascii_lowercase) for i in range(self.strLength))
				while plaintext_Start in self.table:
					plaintext_Start = ''.join(choice(ascii_lowercase) for i in range(self.strLength))
				if debug: print (plaintext_Start)
			else:
				# table generation from file
				plaintext_Start = self.inputData[iteration]

			# Generate Chain
			plaintext_End = plaintext_Start
			for i in range(self.k):
				hash_object = hashlib.md5(plaintext_End.encode())
				plaintext_End = self.R(i, hash_object.hexdigest())
				#if debug: print (hash_object.hexdigest(),'->',plaintext_End)
			print (plaintext_Start,'-->',hash_object.hexdigest())
			#if hash_object.hexdigest() not in self.table.values():
			self.table[plaintext_Start] = hash_object.hexdigest() # allowing duplicate ending values until reduction function is improved.

			if debug: 
				if os.name == 'nt': os.system('cls')
				else: os.system('clear')

			iteration += 1
		#if not self.randomTable:
			# save rainbow table

	def load(self, fileName):
		""" Load pre-existing Rainbow Table """
		self.inputData = []
		file = open(fileName, 'r')
		for line in file:
			data = line.split(',')
			self.table[data[0]] = data[1]
		file.close()
		self.k = len(self.table)

	def R(self, i, hash_object):
		""" Reduction function #i --- NEEDS IMPROVEMENT : Majority of chains are ending on similar values"""
		hash_value = int(hash_object,16)
		hash_value = (hash_value+i) #% (26**self.strLength)
		plaintext = self.num_to_alpha(hash_value)
		return plaintext[-self.strLength:]

	def num_to_alpha(self, num):
		b64 = base64.b64encode(str(num).encode('ascii'))
		return (''.join(re.findall("[a-zA-z]+",b64.decode('utf-8')))).lower()


	def crack(self,passHash):
		newHash = passHash
		for i in range(self.k):
			passPlaintext = self.R(i, newHash.hexdigest())
			if debug: print (newHash.hexdigest(),'-->',passPlaintext)
			for key, val in self.table.items():
				if (newHash.hexdigest() == val):
					print ('Match found!')
					# Generate chain from key
					newPlaintext = key
					print ('key --> val :',key,'-->',val)
					for j in range(self.k):
						newHash = hashlib.md5(newPlaintext.encode())
						
						if newHash.hexdigest() == passHash.hexdigest():
							self.password = newPlaintext
							print ('Success!')
							return True
						tempPlaintext = self.R(j, newHash.hexdigest())
						if debug: print ('\t',newPlaintext,'-->',newHash.hexdigest(),'-->',tempPlaintext)
						newPlaintext = tempPlaintext
					return False
			newHash = hashlib.md5(passPlaintext.encode())
			print (passPlaintext,'-->',newHash.hexdigest())
			#i = i+1
		return False


	def testR(self):
		plaintext = 'pass'
		hash_object = hashlib.md5(plaintext.encode())
		print (plaintext)
		print (hash_object.hexdigest())
		i=0
		while (self.k-i) != 0:
			newText = self.R(len(plaintext),self.k-i,hash_object.hexdigest())
			print ('R'+str(i)+':\t',newText)
			hash_object= hashlib.md5(newText.encode())
			i = i+1

rainbowTable = RainbowTable(k=100,strLength=4)
#rainbowTable.testR()
rainbowTable.generate("four_char_passwords_500")
print ('Generated Rainbow Table with',rainbowTable.k,'reduction functions and chains using a max of',rainbowTable.strLength,'lowercase alphabet characters.\n')
if debug:
	for k, v in rainbowTable.table.items():
		print (k,'-->',v)
password = 'code'
passHash = hashlib.md5(password.encode())
print ("Cracking the password '",password,"' with hash:",passHash.hexdigest())
if rainbowTable.crack(passHash):
	print ('Password found:',rainbowTable.password)
else:
	print ('Attack Failed')
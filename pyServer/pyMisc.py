import random

letters_numbers = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def generatetoken(length):
	token = ''.join((random.choice(letters_numbers) for i in range(length)))
	return token



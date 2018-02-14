class Funky:

	def __init__(self):
		self.x = 10

	def __call__(self):
		print("Look at me, I work like a function!")
		self.y = 20


if __name__ == "__main__":
	print('In main')

	f = Funky 	# f is a class
	print(f'f is: {f}')

	f_inited = f()	# f_inited is an instance of a class
	print(f'f_inited is: {f_inited}')

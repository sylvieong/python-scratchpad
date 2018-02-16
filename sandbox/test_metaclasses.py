class Funky:

	def __init__(self):
		self.x = 10

	def __call__(self):
		print("Look at me, I work like a function!")
		self.y = 20


def print_fn():
	print(f'__name__ is {__name__}')

if __name__ == "__main__":
	print('In main')

	print_fn()

	f = Funky 	# f is a class
	print(f'f is: {f}')

	f_inited = f()	# f_inited is an instance of a class
	print(f'f_inited is: {f_inited}')

	print(f'f_inited.x: {f_inited.x}') # f_inited.x is 10
	#print(f'f_inited.y: {f_inited.y}') # will give error

	f_inited() # calls __call__ of the instance f_inited

	print(f'f_inited.x: {f_inited.x}') # f_inited.x is 10
	print(f'f_inited.y: {f_inited.y}') # f_inited.y is 20




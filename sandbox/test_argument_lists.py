def test_positional_keyword_args(message, start=0, end=4):
	print(message, start, end)

def test_kwargs(first, **rest):
	print(f'first: {first}')
	if any(rest):
		for key in rest:
			print(f'{key}: {rest[key]}')

def append_to_sequence(myseq):
	myseq += (1,2,3)
	return myseq


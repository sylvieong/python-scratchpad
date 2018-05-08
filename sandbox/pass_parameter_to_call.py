def call(tensor: int, mode: str):
    print(f'In call function, tensor: {tensor}, mode: {mode}')
    return tensor*2

def wrap_mode(mode: str):

    def call_with_mode(tensor: int):
        out = call(tensor, mode)
        return out
    
    return call_with_mode


if __name__ == "__main__":
    call_fn = wrap_mode('a')
    call_fn(3)
    

    

class LayerClass:
    def __call__(self, tensor: int, mode: str):
        print(f'in LayerClass.__call__(), tensor: {tensor}, mode: {mode}')
        return 

    def call_with_mode(self, tensor: int):
        return __call__()


if __name__ == "__main__":
    layer_class = LayerClass()
    layer_class(3, 'train')
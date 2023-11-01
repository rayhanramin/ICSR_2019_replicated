import importlib.util

spec = importlib.util.find_spec('lxml')
if spec:
    print(spec.origin)
else:
    print('lxml module not found')
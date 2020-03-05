def readerFile(file_name):
    gpt = {}
    f = open(file_name, 'r')
    content = f.read()
    exec(content, gpt)
    print(content)
    return gpt

def find(gpt, local_data, data, layer1, *other):
    d = gpt.get(local_data)
    if not d:
        return 0
    return d.get((data, layer1, *other))

gpt = readerFile('gpt')
value = find(gpt, "n08_ckt_params", "minExtensionY", "M0C", "M0")
print(value)

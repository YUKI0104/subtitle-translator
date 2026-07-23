with open('index.html', 'rb') as f:
    data = f.read()

# The exact bytes we need to find:
# onclick=\"editProjField('deliveryDate','')\"
# In the file, this appears as literal characters inside a JS double-quoted string
old = b"onclick=\\\"editProjField('deliveryDate','')\\""
new = b"onclick=\\\"editProjField('deliveryDate','',event)\\""

count = data.count(old)
print(f"Found {count} occurrences")

if count:
    data = data.replace(old, new)
    with open('index.html', 'wb') as f:
        f.write(data)
    print("Replaced!")
else:
    # Debug: find similar pattern
    idx = data.find(b"deliveryDate")
    if idx >= 0:
        print(f"Found deliveryDate at byte {idx}")
        print(f"Context: {data[idx-30:idx+60]}")

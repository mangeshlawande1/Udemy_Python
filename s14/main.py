import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello World, welcome to section 14 "

tokens = enc.encode(text)

print("Tokens :-->",tokens)
#Tokens :  [13225, 5922, 11, 12591, 316, 7102, 220, 1265, 220]

decoded = enc.decode( [13225, 5922, 11, 12591, 316, 7102, 220, 1265, 220])
print("decoded :", decoded)
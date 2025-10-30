import re
s = "132 456 Wq  m e"
s = "".join(word.title() if word.isalpha() else word
            for word in re.split(r'(\s)', s)
            )
print(s)

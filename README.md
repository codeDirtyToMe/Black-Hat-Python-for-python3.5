# Black-Hat-Python-for-python3.5
Redoing all the code examples from the Black Hat Python book in python 3.5.

I noticed a lot of people complaining about the example programs in Black Hat Python not working in python 3+. I've decided to go ahead and covert them to 3.5 as I make my way through the book.

Liberties are being taken with certain conventions as I see fit, so some of the code may not seem all that familiar, but i do indend for all examples to function exactly the same as the book. These differences will be most obvious in the naming of variables and functions as I prefer camelCase. 

Argument parsing is also very different.

The most frequent issue I've run into so far is that the socket library requires bytes objects in order to work which python 2.x used natively, but python 3.x doesn't. So, you'll see lots of .encode() and .decode() methods.

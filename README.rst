========
2long.ru
========

Simple url shortener for fun and profit. It's use redis as storage.

Usage
-----
1) from main page
2) use `http://2long.ru/?url=<your-url>` where <your-url> - your url :)
  a) Bonus `http://2long.ru/\<shortkey\>?clicks` where shortkey - last
  part from short url (`http://2long.ru/SDf2ed` key = SDf2ed)
3) use python client (client.py)

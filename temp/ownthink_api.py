# 本代码修改自 https://www.ownthink.com

import json
import requests

sess = requests.get('https://api.ownthink.com/bot?spoken=最好的编程语言？')

answer = sess.text

answer = json.loads(answer)

print(answer)

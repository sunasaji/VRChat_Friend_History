import requests
import json
from urllib.parse import quote
from sys import exit

def end():
    output_file.close()
    exit()

output_file = open("VRChat_Friend_History.txt", mode='w', encoding='utf-8', errors='ignore', buffering=1)

try:
    credential = json.load(open('credential.json'))
except Exception as e:
    output_file.write(e.args[1])
    end()

apiKey = 'JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26'# 18/04/12 時点で公開されているキー
data = {'apiKey':apiKey}

try:
    response = requests.get('https://api.vrchat.cloud/api/1/auth/user/playermoderated', data=data, auth=(quote(credential["username"]), quote(credential["password"])))

except Exception as e:
    output_file.write(e.args[1])
    end()

if response.status_code == 401:
    output_file.write('ログインに失敗しました') # Failed to login.
    end()

elif response.status_code != 200:
    output_file.write('サーバーに接続できませんでした\n') # Cannot connect to the server.
    output_file.write(response.text)
    end()

else:
    moderations = response.json()
    for i in (list(filter(lambda x: x['type'] == 'unmute',moderations))):
        output_file.write(u"{} {}\n".format(i['created'],i[u'sourceDisplayName']))
    end()

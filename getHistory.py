import json
import requests
from pprint import pprint
history = {}
params = {}
params['token'] = 'xoxp-9983699043-504805614417-737731259063-890c5293cf281947fde80baa70f5cc02'
params['count'] = 1000

with open('ch_list.json') as json_file:
    ch_list = json.load(json_file)
print(ch_list)
for ch_id in ch_list.values():
    params['channel'] = ch_id
    while True:
        res = requests.get("https://slack.com/api/channels.history", params = params)
        res = res.json()
        messages = res['messages']
        for m in messages:
            r = m.get('reactions')
            t = m.get('text')
            if r and t:
                for _r in r:
                    pair = (_r['name'], _r['count'])
                    if history.get(t):
                        history[t].append(pair)
                    else:
                        history[t] = [pair]
        if not res['has_more']:
            break
        params['latest'] = messages[-1]['ts']
    pprint(history)
with open('reaction_history.json', 'w') as f:
    json.dump(history, f)

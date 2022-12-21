def hello(message):
        await message.channel.send("Hello")
        print("THERE! I said Hi! Are you proud of me!?")


def joke(message):
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': FACTS_API})
    parsed = response.json()
    if response.status_code == requests.codes.ok:
        await message.channel.send(parsed[0]['joke'])
    else:
        print("Error:", response.status_code, response.text)

def fact(message):
    limit = 1 
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': FACTS_API})
    parsed = response.json()
    if response.status_code == requests.codes.ok:
        await message.channel.send("Did you know " + parsed[0]['fact'])
        print("Okay random fact sent")
    else:
        print("Error:", response.status_code, response.text)
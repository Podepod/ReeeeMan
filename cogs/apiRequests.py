def readConfig():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/settings")
    
    return json.loads(api_page.text)["data"]

def getCustomText():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/customText")
    
    return json.loads(api_page.text)["data"]

def getPermissionClimbingConfig():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/permissionClimbing")
    
    return json.loads(api_page.text)["data"]

def getRegexSearchWordData():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/searchWordData")

    return json.loads(api_page.text)["data"]

def getRegexReactionData():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/regexReactions")

    return json.loads(api_page.text)["data"]

def getRegexBansData():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/regexBans")

    return json.loads(api_page.text)["data"]
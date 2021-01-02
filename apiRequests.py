import requests
import json

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

def readDMFile():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/DM")

    return json.loads(api_page.text)["data"]

def getCogs():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/cogs/list")

    return json.loads(api_page.text)["data"]

def changeCog(cogName: str, action: str):
    api_link = "http://10.30.20.187:4005/api/bot/cogs/change"

    cogList = getCogs()
    i = 0

    if (action == "load"):
        for cog in cogList:
            if (cogName == cog["name"]):
                if (cog["enabled"]):
                    postBody = {
                        "index": i,
                        "action": "unload"
                    }
                    requests.post(api_link, postBody)
                    return f"{cog['name']} succesfully loaded"
                else:
                    return f"{cog['name']} was already loaded"
            i += 1
        return f"couldn't find {cogName}"

    elif (action == "unload"):
        print("Unload apiRequests")
        for cog in cogList:
            if (cogName == cog["name"]):
                print("gevonden")
                if (cog["enabled"]):
                    print("enabled")
                    postBody = {
                        "index": i,
                        "action": "unload"
                    }
                    requests.post(api_link, postBody)
                    print("post request done")
                    return f"{cog['name']} succesfully unloaded"
                else:
                    return f"{cog['name']} wasn't loaded"
            i += 1
        return f"couldn't find {cogName}"

    elif (action == "reload"):
        pass

    return "action not a valid action."
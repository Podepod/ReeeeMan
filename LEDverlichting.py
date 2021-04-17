from tuyapy import TuyaApi
import json
import re

def read_file(filename):
    with open(filename, "r") as read_file:
        data = json.load(read_file)
        read_file.close()
    return data

class CommandNotFound(Exception):
    def __init__(self, command):
        self.command = command

    def __str__(self):
        return f'The command "{self.command}" was not found'

class OptionNotFound(Exception):
    def __init__(self, option):
        self.option = option

    def __str__(self):
        return f'The option "{self.option}" was not found'

class LEDverlichting():
    def __init__(self):
        self.api = TuyaApi()

        self.configFile = "./datafiles/LEDconfig.json"
        config = read_file(self.configFile)
        self.api.init(config["username"], config["password"], config["country_code"], config["application"])

        self.scenesData = []

        self.update()

    def update(self):
        self.api.poll_devices_update()
        self.device_ids = self.api.get_all_devices()
        self.lights = dict(sorted(dict((i.name(),i) for i in self.device_ids if i.obj_type == 'light').items()))
        self.scenes = dict(sorted(dict((i.name(),i) for i in self.device_ids if i.obj_type == 'scene').items()))

        self.makeScenesFile()

    def makeScenesFile(self):
        scenesData = []
        for i in self.scenes.keys():
            name = i.split()[0].lower()
            command = i.split()[1].lower()
            
            optionInList = False
            for j in scenesData:
                if j["name"] == name:
                    optionInList = True
                    newCommand = {
                        "name": command,
                        "action": i
                    }
                    j["commands"].append(newCommand)
                    break
            
            if not optionInList:
                lightname = False

                if name.capitalize() in self.lights.keys():
                    lightname = True

                newOption = {
                    "name": name,
                    "lightname": lightname,
                    "commands": [
                        {
                            "name": command,
                            "action": i
                        }
                    ]
                }

                scenesData.append(newOption)

        self.scenesData = scenesData

    # LIGHT COMMANDS
    def setBrightness(self, lightname, value):
        self.update()

        lightname = lightname.capitalize()
        try:
            value = int(value)
        except ValueError:
            return f"{value} is not a number."
        
        if value < 0:
            value = 0
        elif value > 100:
            value = 255
        else:
            value = round((255 / 100) * value)

        self.lights[lightname].set_brightness(int(value))

        return value

    def setColor(self, lightname, value):
        self.update()

        lightname = lightname.capitalize()

        try:
            value = [int(numeric_string) for numeric_string in value.split()]
            self.lights[lightname].set_color(value)
        except:
            return f"{value} is not a hsv color."

        return "not done yet"

    def state(self, lightname, command):
        self.update()

        lightname = lightname.capitalize()

        if self.lights[lightname].state():
            return f"{lightname} is on."
        else:
            return f"{lightname} is off."

    def activateScene(self, sceneName):
        self.scenes[sceneName].activate()

    def listAllLights(self):
        self.update()
        lightsList = []
        for i in self.lights.keys():
            lightsList.append(i)
        return lightsList

    def listAllScenes(self):
        self.update()
        scenesList = []
        for i in self.scenes.keys():
            scenesList.append(i)
        return scenesList

    def commandScene(self, txt):
        commandFound = False
        optionFound = False
        sceneName = ''

        try:
            for i in self.scenesData:
                if re.search(rf'(?i)\b{i["name"]}\b', txt):
                    optionFound = True
                    txt = re.sub(rf'(?i)\b *{i["name"]} *\b', '', txt)
                    for j in i["commands"]:
                        if re.search(rf'(?i)\b{j["name"]}\b', txt):
                            commandFound = True
                            txt = re.sub(rf'(?i)\b *{j["name"]} *\b', '', txt)
                            sceneName = f'{j["action"]}'
                            self.activateScene(sceneName)
                            break

                    if not commandFound and i["lightname"]:
                        lightCommands = [
                            {
                                "name": "set_brightness",
                                "action": self.setBrightness
                            },
                            {
                                "name": "set_color",
                                "action": self.setColor
                            },
                            {
                                "name": "state",
                                "action": self.state
                            }
                        ]

                        for j in lightCommands:
                            if re.search(rf'(?i)\b{j["name"]}\b', txt):
                                commandFound = True
                                print(j)
                                txt = re.sub(rf'(?i)\b *{j["name"]} *\b', '', txt)
                                output = j["action"](i["name"], txt)
                                print(output)
                                break

                    if not commandFound:
                        raise CommandNotFound(txt)

                    break
            
            if not optionFound:
                raise OptionNotFound(txt)
        
            return 

        except Exception as e:
            return e
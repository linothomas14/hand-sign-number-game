import json


class Media:

    def readHighestScore(mode):
        f = open('db.json')
        data = json.load(f)
        if mode == "basic":
            return data['basic_score']
        else:
            return data['float_score']

    def updateHighestScore(newScore, mode):
        with open('db.json') as f:
            data = json.load(f)

            if mode == "basic":
                data['basic_score'] = newScore
            else:
                data['float_score'] = newScore

        with open('db.json', 'w') as f:
            json.dump(data, f)

    def getSound(num):
        sound_list = {
            "1": "betulsekali.mp3",
            "2": "kamubelajardenganbaik.mp3",
            "3": "kamucerdas.mp3",
            "4": "kamuhebat.mp3",
            "5": "kamukeren.mp3",
            "6": "kamupintar.mp3",
            "7": "luarbiasa.mp3",
            "8": "menakjubkan.mp3",
            "9": "wahhebat.mp3",
            "10": "yapbetul.mp3",
        }
        return sound_list[num]

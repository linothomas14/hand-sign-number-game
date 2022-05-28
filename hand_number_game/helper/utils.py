import json

import hand_number_game.helper.HandTrackingModule as htm


class Utils:

    def __init__(self, detector: htm):

        self.detector = detector
        self.tip_ids = [4, 8, 12, 16, 20]
        self.fingers_list = {
            "1": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "2": [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
            "3": [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            "4": [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            "5": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            "6": [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            "7": [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
            "8": [1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            "9": [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            "10": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        }

    def check_hands_type(self, img, hands_type):
        if hands_type == ['Right', 'Left']:
            lmList_Left = self.detector.findPosition(img,
                                                     handNo=-1,
                                                     draw=False)
            lmList_Right = self.detector.findPosition(img,
                                                      handNo=0,
                                                      draw=False)
        else:
            lmList_Left = self.detector.findPosition(img, handNo=0, draw=False)
            lmList_Right = self.detector.findPosition(img,
                                                      handNo=-1,
                                                      draw=False)

        return lmList_Left, lmList_Right

    def get_shown_fingers(self, img, hands_type):
        lmList_Left, lmList_Right = self.check_hands_type(
            img=img, hands_type=hands_type)
        fingers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for hand, handType in zip(img, hands_type):
            # RightHand
            if handType == 'Right':
                # Thumb
                if lmList_Right[self.tip_ids[0]][1] < lmList_Right[
                        self.tip_ids[0] - 1][1]:
                    fingers[5] = 1
                else:
                    fingers[5] = 0

                for id in range(1, 5):
                    if lmList_Right[self.tip_ids[id]][2] < lmList_Right[
                            self.tip_ids[id] - 2][2]:
                        fingers[id + 5] = 1

            # LeftHand
            if handType == 'Left':
                # Thumb
                if lmList_Left[self.tip_ids[0]][1] > lmList_Left[
                        self.tip_ids[0] - 1][1]:
                    fingers[0] = 1
                else:
                    fingers[0] = 0

                for id in range(1, 5):
                    if lmList_Left[self.tip_ids[id]][2] < lmList_Left[
                            self.tip_ids[id] - 2][2]:
                        fingers[id] = 1
        return fingers

    def readHighestScore():
        f = open('db.json')
        data = json.load(f)
        return data['highest']

    def updateHighestScore(newScore):
        with open('db.json') as f:
            data = json.load(f)

            data['highest'] = newScore

        with open('db.json', 'w') as f:
            json.dump(data, f)

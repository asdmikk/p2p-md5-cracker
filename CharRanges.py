
class Ranges:

    def calc(self):
        ret = []

        charRange = ""
        firstChar = ""
        sendStringLen1 = 1
        sendStringLen2 = 0
        sendStringLen3 = 0
        sendStringLen4 = 0
        while sendStringLen1 == 1:
            charRange = "?"
            sendStringLen1 = 0
            sendStringLen2 = 1
            print(charRange)
        # sendToSlave(charRange)
        while sendStringLen2 == 1:
            charRange = "??"
            sendStringLen2 = 0
            sendStringLen3 = 1
            print(charRange)
        while sendStringLen3 == 1:
            for i in range(33, 126):  # 32?
                charRange = str(chr(i)) + "??"
                print(charRange)
            sendStringLen3 = 0
            sendStringLen4 = 1
        while sendStringLen4 == 1:
            for i in range(33, 126):  # 32?
                firstChar = str(chr(i))
                for i in range(33, 126):
                    charRange = firstChar + str(chr(i)) + "??"
                    print(charRange)
            sendStringLen4 = 0


        return ret



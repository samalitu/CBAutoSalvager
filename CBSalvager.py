import pyautogui # type: ignore
import pydirectinput
import time

def main():
    SalvageTacks()

def LocateTacks():
    #Locate Tacks

    oldX = 0
    oldY = 0

    for i in range(6):
        try:
            x, y = pyautogui.locateCenterOnScreen("Tack.png", grayscale=True, confidence=0.9)

        except:
            print("Couldnt locate tack")
            break
        
        if oldX == x and oldY == y:
            break

        print("found item at: ", x, y)

        pydirectinput.mouseDown(x=1, y=1)
        time.sleep(0.01)
        pydirectinput.mouseUp(x=1, y=1)

        pydirectinput.mouseDown(x=x, y=y, button='right')
        time.sleep(0.01)
        pydirectinput.mouseUp(x=x, y=y, button='right')

        oldX = x
        oldY = y

def SalvageButton():
        #Salvage
        try:
            x, y = pyautogui.locateCenterOnScreen("Salvage.png", grayscale=True, confidence=0.9)

        except:
            print("Couldnt locate salvage button")
            return False

        pydirectinput.mouseDown(x=x, y=y)
        time.sleep(0.01)
        pydirectinput.mouseUp(x=x, y=y)

        return True

def YesButton():
        #Say Yes
        time.sleep(0.5) #TODO Tweak me
        try:
            x, y = pyautogui.locateCenterOnScreen("Yes.png", grayscale=True, confidence=0.9)

        except:
            print("Couldnt locate yes button")
            return False

        pydirectinput.mouseDown(x=x, y=y)
        time.sleep(0.01)
        pydirectinput.mouseUp(x=x, y=y)

        return True

def WaitForOkButton(startTime):
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen("Ok.png", grayscale=True, confidence=0.9)
            break

        except:
            print("Couldnt locate ok button - Time passed: ", time.time() - startTime)

            if time.time() - startTime > 20:
                return False
            else:
                continue
        
    pydirectinput.mouseDown(x=x, y=y)
    time.sleep(0.01)
    pydirectinput.mouseUp(x=x, y=y)

    return True

def SalvageTacks():
    while True:

        #Find & Select Tacks
        LocateTacks()

        #Salvage
        if not SalvageButton():
            return False

        #Say Yes
        if not YesButton():
            return False

        #Wait for OK
        startTime = time.time()
        if not WaitForOkButton(startTime):
            return False


if __name__ == "__main__":
    main()
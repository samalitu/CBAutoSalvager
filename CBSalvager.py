import pyautogui
import pydirectinput
from pynput import keyboard
import time

class Flag:
    ended = False

def main():
    listener = keyboard.Listener(
        on_press=KeyWatcher_onPress,
        on_release=KeyWatcher_onRelease)
    listener.start()
    
    pydirectinput.mouseDown(x=1, y=1)
    time.sleep(0.01)
    pydirectinput.mouseUp(x=1, y=1)

    while not Flag.ended:
        WalkToSmith()
        WalkToHorseSeller()

    print("Ending my job")

def LocateTacks():
    oldX = 0
    oldY = 0

    for i in range(6):
        if not Flag.ended:
            try:
                x, y = pyautogui.locateCenterOnScreen("Images/Tack.png", grayscale=True, confidence=0.9)

            except:
                print("Couldnt locate tack")
                break
            
            if oldX == x and oldY == y:
                print("Old X: ", oldX, "Old Y:", oldY)
                break

            print("found item at: ", x, y)

            pydirectinput.mouseDown(x=x, y=y, button='right')
            time.sleep(0.01)
            pydirectinput.mouseUp(x=x, y=y, button='right')

            oldX = x
            oldY = y

def PressButton(button):
    time.sleep(0.3)
    try:
        x, y = pyautogui.locateCenterOnScreen("Images/" + button + ".png", grayscale=True, confidence=0.9)

    except:
        print("Couldnt locate " + button + " button")
        return False

    pydirectinput.mouseDown(x=x, y=y)
    time.sleep(0.01)
    pydirectinput.mouseUp(x=x, y=y)

    return True  

def WalkTo(Target):
    status = True

    pydirectinput.keyDown("tab")

    if not PressButton(Target):
        status =  False

    pydirectinput.keyUp("tab")

    return status

def WalkToSmith():
    if not WalkTo("Smith"):
        return False


    startTime = time.time()
    while not PressButton("SmithIntro"):
        if time.time() - startTime > 20 or Flag.ended:
            return False
        else:
            time.sleep(1)

    SalvageTacks()

    return True

def WalkToHorseSeller():
    if not WalkTo("HorseSeller"):
        return False


    startTime = time.time()
    while not PressButton("HorseSellerIntro"):
        if time.time() - startTime > 20 or Flag.ended:
            return False
        else:
            time.sleep(1)

    BuyTacks()

    return True

def WaitForOkButton():
    startTime = time.time()
    while True:
        try:
            x, y = pyautogui.locateCenterOnScreen("Images/Ok.png", grayscale=True, confidence=0.9)
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

    time.sleep(1)

    while not Flag.ended:

        #Find & Select Tacks
        LocateTacks()

        #Salvage
        if not PressButton("Salvage"):
            return False

        #Say Yes
        if not PressButton("Yes"):
            return False

        #Wait for OK
        if not WaitForOkButton():
            return False

def BuyTack(x, y):
    pydirectinput.mouseDown(x=x, y=y)
    time.sleep(0.1)
    pydirectinput.mouseUp(x=x, y=y)

    if not PressButton("Buy"):
        return False
    
    return True

def BuyTacks():
    CalibrationX = 500
    CalibrationY = 30

    time.sleep(1)

    try:
        x, y = pyautogui.locateCenterOnScreen("Images/Tack2.png", grayscale=True, confidence=0.9)
    except:
        print("Couldnt locate tack")

    x = x + CalibrationX
    y = y + CalibrationY

    while not Flag.ended:
        if not BuyTack(x, y):
            break

        try:
            x, y = pyautogui.locateCenterOnScreen("Images/BagFull.png", grayscale=True, confidence=0.9)
            print("Bag has been filled")
            break
        except:
            print("Bag is not full yet")

    if not PressButton("Ok"):
        return False
    
    return True

def KeyWatcher_onPress(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def KeyWatcher_onRelease(key):
    print('{0} released'.format(key))
    
    if key == keyboard.Key.f9:
        Flag.ended = True    
        return False

if __name__ == "__main__":
    main()
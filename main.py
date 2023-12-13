import time
import pyautogui
import keyboard
from MTM import matchTemplates
import numpy as np
import mss
import cv2


left=0
top=0
width=0
height=0
game_location = {'left': left, 'top': top, 'width': width, 'height': height}
coin_pos = []
offsetX=0
offsetY=0


print("Starting Program ...")


# Load the templates
try:
    # Load the main image in which you want to find template positions
   
    templates = [
        ('btc', cv2.imread('btc.png')),
        ('doge', cv2.imread('doge.png')),
        ('eth', cv2.imread('eth.png')),
        ('dash', cv2.imread('dash.png')),   
    
    ]
except Exception as e:
    print(f"Error loading templates: {e}")
    exit()


if pyautogui.locateOnScreen('coinmatch.png', confidence=0.9) is not None:
            print("Pressing Start Button")
            image = pyautogui.locateOnScreen('coinmatch.png', confidence=0.9)
            if image is not None:
                x, y = pyautogui.center(image)
                pyautogui.moveTo(x + 5, y+5)
                time.sleep(1)
                pyautogui.click()
                time.sleep(4)



            if pyautogui.locateOnScreen('GameScreenLocation.png', confidence=0.6) is not None:
                    print("Game button found")
                    template_position = pyautogui.locateOnScreen('GameScreenLocation.png', confidence=0.6)

                    #get game location window X and Y
                    offsetX = template_position[0]
                    offsetY = template_position[1]

                    # Extract position information
                    left, top, width, height = template_position
                    game_location = {'left': left, 'top': top, 'width': width, 'height': height}
                    if pyautogui.locateOnScreen('StartButton.png', confidence=0.9) is not None:
                        print("Pressing Start Button")
                        image = pyautogui.locateOnScreen('StartButton.png', confidence=0.9)
                        if image is not None:
                            x, y = pyautogui.center(image)
                            pyautogui.moveTo(x + 5, y+5)
                            time.sleep(1)
                            pyautogui.click()
                            time.sleep(1)
            
        
        


        

def template_matching():  

     # Create an mss instance for screen capture
    with mss.mss() as sct:
        frame = sct.grab(game_location)
         
        # Convert mss.grab() data to NumPy array
        image_np = np.array(frame, dtype=np.uint8)
        # Convert RGBA to BGR
        screen = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)   

        
       
        

        # Perform template matching
        matches = matchTemplates(
            templates,
            screen,
            N_object=64,
            score_threshold=0.7,
            maxOverlap=0.25,
            searchBox=None
        )
        for i in range(len(matches['BBox'])):
            if i in matches['BBox'].index:
                coin_pos.append(matches['BBox'][i])
                print(matches['TemplateName'][i])

        # Check if matches are found
        if not matches.empty:
            # Choose a random match
            random_match = matches.sample()

            # Extract information from the match
            template_name = random_match.iloc[0]['TemplateName']
            bbox = random_match.iloc[0]['BBox']

            # Click on the center of the bounding box
            x, y, w, h = bbox
            center_x = x + w // 2
            center_y = y + h // 2

            # Print information
            print(f"Clicked on {template_name} at position ({center_x}, {center_y})")

            # Click using pyautogui
            pyautogui.click(center_x+ offsetX, center_y+ offsetY)

# Continuously perform template matching every 0.5 seconds
while not keyboard.is_pressed('q'):
    template_matching()
    time.sleep(1)

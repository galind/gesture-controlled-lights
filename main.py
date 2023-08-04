import asyncio
import os

import cv2
from kasa import SmartBulb

from hand_tracking import HandTracker


async def bulb_connection():
    bulb = SmartBulb('192.168.1.52')
    await bulb.update()
    return bulb


def finger_count(lm_list: list):
    finger_coords = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_coords = (4, 2)

    count = 0
    if len(lm_list) > 0:
        for coord in finger_coords:
            if lm_list[coord[0]][2] < lm_list[coord[1]][2]:
                count += 1
        if lm_list[thumb_coords[0]][1] > lm_list[thumb_coords[1]][1]:
            count += 1
    return count


def history_check(history: list):
    if len(history) < 10:
        return False
    first_element = history[0]
    return all(result == first_element for result in history)


def send_notification(action: int):
    message = 'Sleeping for 5 seconds...'
    title = 'Gesture Controlled Lights'
    subtitle = f'Action {action} has been received!'
    content = 'display notification "{}" with title "{}" subtitle "{}"'.format(
        message, title, subtitle
    )
    os.system(f'osascript -e \'{content}\'')


async def task_one(bulb: SmartBulb):
    await bulb.update()

    status = bulb.is_on
    color = bulb.color_temp
    brightness = bulb.brightness

    if not status:
        await bulb.turn_on()

    if color != 6500:
        await bulb.set_color_temp(6500)

    if brightness != 80:
        await bulb.set_brightness(80)


async def task_two(bulb: SmartBulb):
    await bulb.update()

    status = bulb.is_on
    color = bulb.color_temp
    brightness = bulb.brightness

    if not status:
        await bulb.turn_on()

    if color != 5000:
        await bulb.set_color_temp(5000)

    if brightness != 50:
        await bulb.set_brightness(50)


async def task_three(bulb: SmartBulb):
    await bulb.update()
    status = bulb.is_on
    if status:
        await bulb.turn_off()


def main():
    bulb = asyncio.run(bulb_connection())
    print(bulb)

    cap = cv2.VideoCapture(0)
    tracker = HandTracker(max_hands=1, detection_conf=0.85, tracking_conf=0.85)
    history = []

    while True:
        success, image = cap.read()
        if not success:
            continue

        image = tracker.hands_finder(image)
        lm_list = tracker.position_finder(image)
        up_count = finger_count(lm_list)

        history.append(up_count)
        result = history_check(history)

        valid_actions = [1, 2, 3]
        if result and up_count in valid_actions:
            send_notification(up_count)

            if up_count == 1:
                asyncio.run(task_one(bulb))
            elif up_count == 2:
                asyncio.run(task_two(bulb))
            elif up_count == 3:
                asyncio.run(task_three(bulb))

            history = []

        if len(history) > 10:
            history.pop(0)

        font = cv2.FONT_HERSHEY_TRIPLEX
        color = (255, 255, 255)

        org = (15, 180)
        formatted_history = ', '.join([str(h) for h in history])
        text = f'History: {formatted_history}'
        cv2.putText(image, text, org, font, 3, color, 2)

        org = (15, 85)
        text = f'Fingers up: {str(up_count)}'
        cv2.putText(image, text, org, font, 3, color, 2)

        cv2.imshow('Output', image)
        cv2.waitKey(75)


if __name__ == '__main__':
    main()

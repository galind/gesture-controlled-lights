import os

import cv2

from hand_tracking import HandTracker


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
    message = 'Sleeping for 15 seconds...'
    title = 'Gesture Controlled Lights'
    subtitle = f'Action {action} has been received!'
    content = 'display notification "{}" with title "{}" subtitle "{}"'.format(
        message, title, subtitle
    )
    os.system(f'osascript -e \'{content}\'')


def main():
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
                pass
            elif up_count == 2:
                pass
            elif up_count == 3:
                pass
            elif up_count == 4:
                pass
            elif up_count == 5:
                pass

            cv2.waitKey(15000)

        if len(history) > 10:
            history.pop(0)

        text = f'Fingers up: {str(up_count)}'
        org = (15, 85)
        font = cv2.FONT_HERSHEY_TRIPLEX
        color = (255, 255, 255)
        cv2.putText(image, text, org, font, 3, color, 2)

        cv2.imshow('Output', image)
        cv2.waitKey(300)


if __name__ == '__main__':
    main()

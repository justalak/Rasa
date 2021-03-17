from common import emoji

class DisplayHelper:
    @staticmethod
    def numberToArrow(number):
        if number > 0:
            return emoji.UP_ARROW
        elif number < 0:
            return emoji.DOWN_ARROW
        else:
            return ''

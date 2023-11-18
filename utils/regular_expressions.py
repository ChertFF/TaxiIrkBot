import re


def correct_phone_number(number):
    if re.match(r'^((\+7|)+([0-9]){10})$', number):
        return number
    else:
        return "error"


def correct_FI(FI):
    if re.match(r'^[а-яА-ЯёЁa-zA-Z]+ [а-яА-ЯёЁa-zA-Z]+ ?[а-яА-ЯёЁa-zA-Z]+$', FI):
        return FI
    else:
        return "error"
# phone_number = re.match(r'^((\+7|7|8)+([0-9]){10})$', text)
# print(phone_number)

# def main():
#     detect_phone_number(text)
#
#
# if __name__ == '__main__':
#     main()

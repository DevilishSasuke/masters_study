import re





'''
def validate_phone_number(phone_str: str) -> bool:
    return re.fullmatch(r"^(\+7|8)\d{10}$", phone_str)

def beautify_phone_number(phone_str: str) -> str:
    return re.sub(
        r"^(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})$",
        r"+7-\2-\3-\4-\5",
        phone_str
    )


print("0 to exit")
print("enter russian phone number")
while True:
    phone_str = input()
    if phone_str == "0":
        break
    if not validate_phone_number(phone_str.strip()):
        print("you entered number in wrong format")
    print("here is beautified number: " + beautify_phone_number(phone_str))
'''

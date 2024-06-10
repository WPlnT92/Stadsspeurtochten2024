import random
from .models import CodeTocht

def trial_code_check(code):
    trial_codes_list = ["AMSCO73995647", "MAAS12345678", "GRUNN12345678", "AMSCO12345678", "MAAS87654321", "GRUNN87654321"]
    if code in trial_codes_list:
        return True
    else:
        return False    

def code_generator(name):
    names_dict = {
        "Maastricht": "MAAS", 
        "Groningen": "GRUNN",
        "Amsterdam-Centrum-Oost": "AMSCO",
        "Amsterdam-Binnenstad": "AMSB",
        "Willemstad": "WILL",
        "Haarlem": "HRLM",
        }
    letters = names_dict[name]
    nums = random.randint(1000000000, 9999999999)
    numbers = str(nums)
    new_code_tocht = letters+numbers
    all_codes = CodeTocht.objects.all()
    for code_tocht in all_codes:
        if new_code_tocht == code_tocht.code_tocht:
            new_code_tocht = new_code_tocht+'D'
    add_new_code = CodeTocht.objects.create(code_tocht=new_code_tocht)
    add_new_code.save()
    return new_code_tocht
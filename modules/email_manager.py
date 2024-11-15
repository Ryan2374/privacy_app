import random
import string

def generate_disposable_email():
    domain = "examplemail.com"
    local_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{local_part}@{domain}"

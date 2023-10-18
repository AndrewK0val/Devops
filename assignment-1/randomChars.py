import random
import string

lenght = 6

sixRandomChars = ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))

bucket_name = sixRandomChars + "-akoval"

print(bucket_name)
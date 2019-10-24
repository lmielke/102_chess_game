import re

host = "localhost:8000"


match = re.search(re.compile(r"\d{1,3}\.\d{1,3}"), host)

print(match)
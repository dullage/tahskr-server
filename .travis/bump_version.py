import json
import sys
from datetime import date

version_file_list = sys.argv[1:]

for version_file in version_file_list:
    with open(version_file, "r+") as f:
        content = json.load(f)

        prev_version = content["version"]
        prev_version_parts = prev_version.split(".")
        prev_date_part = ".".join(prev_version_parts[0:3])
        prev_increment_part = prev_version_parts[3]

        today = date.today()
        y = today.strftime("%y").lstrip("0")
        m = today.strftime("%m").lstrip("0")
        d = today.strftime("%d").lstrip("0")
        new_date_part = ".".join([y, m, d])

        if prev_date_part == new_date_part:
            new_increment_part = str(int(prev_increment_part) + 1)
        else:
            new_increment_part = "0"

        new_version = ".".join([new_date_part, new_increment_part])

        content["version"] = new_version
        f.seek(0)
        f.truncate()
        f.write(json.dumps(content))

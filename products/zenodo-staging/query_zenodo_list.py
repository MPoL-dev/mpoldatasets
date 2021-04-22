import requests
import os

base_id = os.getenv("ZENODO_BASE_ID")
base_url = os.getenv("ZENODO_BASE_URL")
token = os.getenv("ZENODO_API_TOKEN")

# do an initial query to the repository to learn what the latest
# version identifier is
r = requests.get(
    "{:}/api/deposit/depositions/{:}".format(base_url, base_id),
    params={"access_token": token},
)

latest_id = r.json()["links"]["latest"].split("/")[-1]

# now query the latest version for the md5 sums
r = requests.get(
    "{:}/api/deposit/depositions/{:}".format(base_url, latest_id),
    params={"access_token": token},
)

with open("zenodolist.chk", "w") as f:
    for file in r.json()["files"]:
        f.write("{:} {:}\n".format(file["checksum"], file["filename"]))

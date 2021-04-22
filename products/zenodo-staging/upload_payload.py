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

# create new version (unpublished) to upload files to
r = requests.post(
    "{:}/api/deposit/depositions/{:}/actions/newversion".format(base_url, latest_id),
    params={"access_token": token},
)

# get the "latest_draft" id
latest_draft_id = r.json()["links"]["latest_draft"].split("/")[-1]

# get the metadata for this new version
r = requests.get(
    "{:}/api/deposit/depositions/{:}".format(base_url, latest_draft_id),
    params={"access_token": token},
)
# primarily, we're interested in the upload bucket
bucket = r.json()["links"]["bucket"]

# upload all files in the payload
with open("payloadlist.txt", "r") as f:
    for line in f:
        fname = line.rstrip("\n")
        print("uploading", fname)
        # The target URL is a combination of the bucket link with the desired filename
        # seperated by a slash.
        with open(fname, "rb") as f:
            r = requests.put(
                "{:}/{:}".format(bucket, fname),
                data=f,
                params={"access_token": token},
            )
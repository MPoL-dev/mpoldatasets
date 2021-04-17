import requests
import os
import json

token = os.getenv("ZENODO_API_TOKEN")

# link to all versions
# 10.5281/zenodo.4498438
# but note that this is just for web reference,
# we need to use the versioned id for actions
# especially for new version creation
# https://developers.zenodo.org/#new-version


id = 4498439

# response = requests.get(
#     "https://zenodo.org/api/deposit/depositions", params={"access_token": token},
# )
# # print(response.url)
# print(json.dumps(response.json(), sort_keys=True, indent=4))

r = requests.get(
    "https://zenodo.org/api/deposit/depositions/{:}".format(id),
    params={"access_token": token},
)
print(r.url)

print(json.dumps(r.json(), sort_keys=True, indent=4))

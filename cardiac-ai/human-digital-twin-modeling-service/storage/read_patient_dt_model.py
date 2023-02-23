import requests

endpoint = "http://localhost:3000/"
webid = "http://localhost:3000/prodiptaPromit/card#me"

ps_hdt_output = ["/public/healthcare/ps_hdt/data",
                 "/public/healthcare/ps_hdt/simulation-code"]

webid_response = requests.get(webid)

if webid_response.status_code == 200:
    public_key = webid_response.json()["publicKey"]

    for folder in ps_hdt_output:
        ps_hdt_output_response = requests.get(
            endpoint + folder,
            headers={
                "Authorization": "Bearer " + public_key,
            }
        )

        if ps_hdt_output_response.status_code == 200:
            ps_hdt_output_contents = ps_hdt_output_response.json()

            for file in ps_hdt_output_contents:
                print(file["name"])
        else:
            print(f"PS-HDT output folder contents request failed for {folder}")
else:
    print("WebID request failed")

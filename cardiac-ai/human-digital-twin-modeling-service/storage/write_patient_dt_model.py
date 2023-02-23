import requests
import os

endpoint = "http://localhost:3000/"
webid = "http://localhost:3000/prodiptaPromit/card#me"

ps_hdt_output = ["patient-dt-modelling/data",
                 "patient-dt-modelling/simulation-code"]
ps_hdt_output_sp = ["/public/healthcare/dt/data",
                    "/public/healthcare/dt/simulation-code"]

webid_response = requests.get(webid)

if webid_response.status_code == 200:
    public_key = webid_response.json()["publicKey"]

    for i in range(len(ps_hdt_output)):
        folder = ps_hdt_output[i]
        pod_folder = ps_hdt_output_sp[i]

        files = [f for f in os.listdir(
            folder) if os.path.isfile(os.path.join(folder, f))]
        for file in files:
            file_path = folder + "/" + file
            pod_file_path = pod_folder + file

            with open(file_path, "rb") as f:
                upload_response = requests.put(
                    endpoint + pod_file_path,
                    headers={
                        "Authorization": "Bearer " + public_key,
                        "Content-Type": "text/plain"
                    },
                    data=f
                )

                if upload_response.status_code == 201:
                    print("File " + file + " uploaded successfully")
                else:
                    print("File " + file + " upload failed")
else:
    print("WebID request failed")

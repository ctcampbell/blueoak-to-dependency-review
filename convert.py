import requests


undesirable_ratings = ["Model", "Lead"]


if __name__ == '__main__':
  response = requests.get("https://blueoakcouncil.org/list.json")
  if response.ok:
    license_list = response.json()
    real_license_list = [x for x in license_list["ratings"] if x["name"] not in undesirable_ratings]

    with open("dist/blueoak-licenses.yml", "w") as f:
      f.write("allow_licenses:\n")
      for rating in real_license_list:
        f.write(f"  # {rating['name']}\n")
        f.write(f"  # {rating['notes']}\n")
        for license in rating["licenses"]:
          f.write(f"  - '{license['id']}'\n")
import requests
import logging
import os


# Constants
BLUEOAK_LIST_URL = "https://blueoakcouncil.org/list.json"
OUTPUT_FILE_PATH = "dist/blueoak-licenses.yml"
UNDESIRABLE_RATINGS = ["Model", "Lead"]


def fetch_license_list(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching license list: {e}")
        return None


def filter_licenses(license_list, undesirable_ratings):
    return [
        rating for rating in license_list["ratings"]
        if rating["name"] not in undesirable_ratings
    ]


def write_licenses_to_file(licenses, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write("allow_licenses:\n")
            for rating in licenses:
                f.write(f"  # {rating['name']}\n")
                f.write(f"  # {rating['notes']}\n")
                for license in rating["licenses"]:
                    f.write(f"  - '{license['id']}'\n")
    except IOError as e:
        logging.error(f"Error writing to file: {e}")


def main():
    logging.basicConfig(level=logging.INFO)

    license_list = fetch_license_list(BLUEOAK_LIST_URL)
    if license_list:
        real_license_list = filter_licenses(license_list, UNDESIRABLE_RATINGS)
        write_licenses_to_file(real_license_list, OUTPUT_FILE_PATH)
        logging.info("License file created successfully.")
    else:
        logging.error("Failed to create license file due to previous errors.")


if __name__ == '__main__':
    main()

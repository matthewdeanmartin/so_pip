import os

from so_pip.support_files.license import convert_html_to_text

if __name__ == "__main__":
    for license_name in ["CC BY-SA 2.0"]:  # ,"CC BY-SA 2.5.html"]:
        license_path = f"{license_name}.txt"
        if not os.path.exists(license_path) and (
            "2.0" in license_name or "2.5" in license_name
        ):
            # Can't find text versions of 2.5 or 2.0
            # ref https://wiki.creativecommons.org/wiki/License%20Versions
            license_path_txt = f"{license_name}.txt"
            convert_html_to_text(
                license_path.replace(".txt", ".html"), license_path_txt
            )

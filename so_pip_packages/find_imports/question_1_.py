"""
N/A Chip Calhoun
https://stackoverflow.com/questions/32531385/python-string-comparison-using-pymarc-marc8-to-unicode-no-longer-working
"""

# My code imports a MARC file using MARCReader and compares a string against a
# list of acceptable answers. If the string from MARC has no match in my list,
# it gets added to an error list. This has worked for years in Python 2.7.4
# installations on Windows 7 with no issue. I recently got a Windows 10 machine
# and installed Python 2.7.10, and now strings with non-standard characters fail
# that match. the issue is not Python 2.7.10 alone; I've installed every version
# from 2.7.4 through 2.7.10 on this new machine, and get the same problem. A new
# install of Python 2.7.10 on a Windows 7 machine also gets the problem.
#


import os
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
from time import strftime

# repository, but "Acadm̌ie des Sciences" now appears in our list of new
# repositories.
from aipmarc import get_bibno, get_catdb, parse_date

# I've trimmed out functions that aren't relevant, and I've dramatically trimmed
# the master list. In this example, "Académie des Sciences" is an existing
from phfawstemplate import browsepage  # , nutchpage, eadpage, titlespage
from pymarc import MARCReader, marc8_to_unicode
from umlautsort import alafiling


def make_newrepos_list(
    list, fn
):  # Create list of unexpected repositories found in the MArcout database dump
    output = (
        "These new repositories are not yet included in the master list in phfaws.py. Please add the repository code (in place of "
        "NEWCODE*"
        "), and the URL (in place of "
        "TEST"
        "), and then add these lines to phfaws.py. Please keep the list alphabetical. \nYou can find repository codes at http://www.loc.gov/marc/organizations/ \n \n"
    )
    for row in list:
        output = '{}    reposmasterlist.append([u"{}", "{}", "{}"])\n'.format(
            output, row[0], row[1], row[2]
        )

    fh = open(fn, "w")
    fh.write(output.encode("utf-8"))
    fh.close()


def main(marcfile):
    reader = MARCReader(file(marcfile))

    """
    Creating list of preset repository codes.
    """
    reposmasterlist = [
        [
            "American Institute of Physics",
            "MdCpAIP",
            "http://www.aip.org/history/nbl/index.html",
        ]
    ]
    reposmasterlist.append(
        [
            "Académie des Sciences",
            "FrACADEMIE",
            "http://www.academie-sciences.fr/fr/Transmettre-les-connaissances/inventaires-des-fonds-d-archives-personnelles.html",
        ]
    )
    reposmasterlist.append(
        [
            "American Association for the Advancement of Science",
            "daaas",
            "http://archives.aaas.org/",
        ]
    )

    newreposcounter = 0
    newrepos = ""
    newreposlist = []

    findingaidcounter = 0
    reposcounter = 0

    for record in reader:
        if record["903"]:  # Get only records where 903a="PHFAWS"
            phfawsfull = record.get_fields("903")
            for field in phfawsfull:
                phfawsnote = field["a"]
                if "PHFAWS" in phfawsnote:
                    if (
                        record["852"] is not None
                    ):  # Get only records where 852/repository is not blank
                        repository = record.get_fields("852")
                        for field in repository:
                            reposname = field["a"]
                        reposname = marc8_to_unicode(
                            reposname
                        )  # Convert repository name from MARC file to Unicode
                        reposname = reposname.rstrip(".,")
                        reposcode = None
                        reposurl = None
                        for (
                            row
                        ) in (
                            reposmasterlist
                        ):  # Match field 852 repository against the master list.
                            if (
                                row[0] == reposname
                            ):  # If it's in the master list, use the master list to populate our repository-related fields
                                reposcode = row[1]
                                reposurl = row[2]
                        if (
                            record["856"] is not None
                        ):  # Get only records where 856 is not blank and includes "online finding aid"
                            links = record.get_fields("856")
                            for field in links:
                                linksthree = field["3"]
                                if (
                                    linksthree is not None
                                    and "online finding aid" in linksthree
                                ):
                                    if (
                                        reposcode == None
                                    ):  # If this record's repository wasn't in the master list, add to list of new repositories
                                        newreposcounter += 1
                                        newrepos = f"{newrepos} {reposname} \n"
                                        reposcode = "NEWCODE" + str(newreposcounter)
                                        reposurl = "TEST"
                                        reposmasterlist.append(
                                            [reposname, reposcode, reposurl]
                                        )
                                        newreposlist.append(
                                            [reposname, reposcode, reposurl]
                                        )
                                    human_url = field["u"]
                                else:
                                    pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        else:
            pass

    # Output list of new repositories
    newreposlist.sort(key=lambda rep: rep[0])
    if newreposcounter != 0:
        status = (
            "%d new repositories found. you must add information on these repositories, then run phfaws.py again. Please see the newly updated rewrepos.txt for details."
            % (newreposcounter)
        )
        sys.stderr.write(status)
        make_newrepos_list(newreposlist, "newrepos.txt")


if __name__ == "__main__":
    try:
        mf = sys.argv[1]
        sys.exit(main(mf))
    except IndexError:
        sys.exit("Usage: %s <marcfile>" % sys.argv[0])

# Edit: I've found that simply commenting out the "reposname =
# marc8_to_unicode(reposname)" line gets me the results I want. I still don't
# understand why this is, since it was a necessary step before.

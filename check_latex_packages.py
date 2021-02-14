import os
import subprocess
import re

def check_latex_packages():
    test_template = r"""\documentclass[preview]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{test_package}
\begin{document}
Test
\end{document}
"""
    packages = [
        "babel",
        "amsmath",
        "amssymb",
        "dsfont",
        "setspace",
        "tipa",
        "relsize",
        "textcomp",
        "mathrsfs",
        "calligra",
        "wasysym",
        "ragged2e",
        "physics",
        "xcolor",
        "microtype",
        "pifont",
    ]

    for package in packages:
        with open("latex_package_test.tex", "w", encoding="utf8") as fout:
            test = test_template.replace("test_package", package)
            fout.write(test)
        print(f"Testing latex package {package:<15} ", end="")
        test_run = subprocess.run(
            ["latex", "-interaction=batchmode", "latex_package_test.tex"],
            capture_output=True
        )
        if test_run.returncode == 0:
            print("ok")
        else:
            print("failed")
            print("printing error log")
            with open("latex_package_test.log", "r") as logfile:
                log = logfile.read()
            error_regex = re.compile(r"!(.*\n){5}")
            m = error_regex.search(log)
            for line in m.group().split("\n"):
                print(line)

    print("Clean up testing artifacts...", end="")
    os.remove("latex_package_test.aux")
    os.remove("latex_package_test.xdv")
    os.remove("latex_package_test.log")
    os.remove("latex_package_test.tex")
    print("done")

if __name__ == "__main__":
    print("\n===Checking for latex package dependencies===\n")
    latex_package_fail = check_latex_packages()
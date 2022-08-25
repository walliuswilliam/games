find . -type d -name __pycache__ -exec rm -r {} \+

# import os, pkg_resources
# pkgs = sorted([str(i.key) for i in pkg_resources.working_set])
# if '__' not in pkgs: os.system("pip install __")
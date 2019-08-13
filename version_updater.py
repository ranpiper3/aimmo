import argparse

from semantic_release.history import set_new_version

from aimmo import __version__

parser = argparse.ArgumentParser(description="Update version based on branch.")
parser.add_argument("DEPLOY_TO_DEV", help="True if build to dev")
parser.add_argument("TRAVIS_BUILD_NUMBER", help="Travis build number")
parser.add_argument("TRAVIS_BRANCH", help="Name of the branch the build is on")

args = parser.parse_args()
version = __version__

if args.DEPLOY_TO_DEV:
    version = __version__ + "dev" + args.TRAVIS_BUILD_NUMBER
else:
    BRANCH = args.TRAVIS_BRANCH

    if BRANCH == "development":
        version = __version__ + ".b" + args.TRAVIS_BUILD_NUMBER

set_new_version(version)
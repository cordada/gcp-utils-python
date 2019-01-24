"""
GCP's or this library's-specific common constants.

"""

# GCP project ID
# > A project ID must start with a lowercase letter, and can contain only ASCII letters, digits,
# > and hyphens, and must be between 6 and 30 characters.
# https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project
PROJECT_ID_MAX_LENGTH = 30
# TODO: PROJECT_ID_REGEX = re.compile(r'^...$')

# GCP region ID
#   https://cloud.google.com/about/locations/
# note: as of 2018-10-22, we have not found anywhere official the value of this restriction.
# note: as of 2018-10-22, the longest region ID is 'northamerica-northeast1' (23 characters).
REGION_ID_MAX_LENGTH_ESTIMATION = 48
# TODO: REGION_ID_MAX_LENGTH

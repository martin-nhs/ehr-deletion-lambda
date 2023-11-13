import os

from utilities.aws_utilities import fetch_ssm_parameter
from models.database_connection import DatabaseConnection


def get_ehr_repository_database_parameters() -> DatabaseConnection:
    """ Gets the connection string for the EHR Repository database.
    :return: The connection string.
    """
    database_name = fetch_ssm_parameter(os.environ["EHR_REPO_DB_NAME_SSM_PARAMETER_NAME"])
    username = fetch_ssm_parameter(os.environ["EHR_REPO_DB_USER_SSM_PARAMETER_NAME"], True)
    password = fetch_ssm_parameter(os.environ["EHR_REPO_DB_PASS_SSM_PARAMETER_NAME"], True)
    hostname = fetch_ssm_parameter(os.environ["EHR_REPO_DB_HOST_SSM_PARAMETER_NAME"])
    port = int(os.environ["EHR_REPO_DB_PORT"])  # Default 5432

    return DatabaseConnection(
        database_name,
        hostname,
        username,
        password,
        port
    )

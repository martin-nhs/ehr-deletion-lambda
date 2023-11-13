import boto3


def fetch_ssm_parameter(parameter_name: str, should_decrypt: bool = False) -> str:
    """ A utility function which fetches a parameter from AWS SSM.
    :param str parameter_name: The name (or key) of the SSM parameter.
    :param bool should_decrypt: A boolean to indicate if the parameter should be decrypted or not.
    :return: The encrypted or decrypted value from SSM.
    """
    ssm_client = boto3.client('ssm')
    ssm_response = ssm_client.get_parameter(
        Name=parameter_name,
        WithDecryption=should_decrypt
    )

    return ssm_response["Parameter"]["Value"]

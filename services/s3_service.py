import os
import boto3

from loguru import logger
from boto3.exceptions import Boto3Error
from exceptions.unable_to_proceed_exception import UnableToProceedException


class S3Service:
    def __init__(self):
        self._ehr_repository_bucket_name = os.environ["EHR_REPOSITORY_BUCKET_NAME"]
        self._s3_client = boto3.client('s3')

    def delete_health_records_from_s3(self, conversation_ids: list[str]) -> list[str]:
        """ Delete health records from S3 given their corresponding Conversation IDs.
        :param list[str] conversation_ids: The list of Conversation IDs to be deleted.
        :return: A list of Conversation IDs which were deleted successfully.
        """
        if len(conversation_ids) == 0:
            return []

        failed_deletions = {}

        for conversation_id in conversation_ids:
            try:
                all_messages = self._s3_client.list_objects_v2(
                    Prefix=conversation_id,
                    Bucket=self._ehr_repository_bucket_name
                )

                if "Contents" in all_messages:
                    # This will capture all Message IDs for the EHR.
                    object_keys = [content["Key"] for content in all_messages["Contents"]]

                    logger.info(f"Processing the deletion of Conversation ID {conversation_id}, messages to be "
                                f"deleted: {len(object_keys)}.")

                    response = self._s3_client.delete_objects(
                        Bucket=self._ehr_repository_bucket_name,
                        Delete={
                            'Objects': [{"Key": key} for key in object_keys],
                            'Quiet': True  # Returns only the keys where an error occurred.
                        }
                    )

                    if 'Errors' in response:
                        failed_deletions[conversation_id] = response["Errors"]
                    else:
                        logger.info("All messages have been successfully deleted from S3 for "
                                    f"Conversation ID {conversation_id}.")
                else:
                    failed_deletions[conversation_id] = {
                        "Message": "No S3 records were found for this Conversation ID."
                    }

            except Boto3Error as error:
                failed_deletions[conversation_id] = {
                    "Message": "An error occurred while deleting the health record from S3 for this Conversation ID.",
                    "Details": error
                }

        if failed_deletions:
            logger.error(f"One or more errors occurred while deleting the records, details: {failed_deletions}.")

        successfully_deleted_conversation_ids = [successful_conversation_id
                                                 for successful_conversation_id
                                                 in conversation_ids
                                                 if successful_conversation_id
                                                 not in failed_deletions.keys()]

        if len(successfully_deleted_conversation_ids) > 0:
            return successfully_deleted_conversation_ids
        else:
            raise UnableToProceedException(
                f"Unable to proceed - no health records were successfully deleted, please investigate logs."
            )

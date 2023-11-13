from services.database_service import DatabaseService
from services.s3_service import S3Service
from loguru import logger


def lambda_handler(event, context):
    """ The entrypoint of the lambda function. """

    # Extract initial detail and context and produce starting log.
    invocation_request_id = context["aws_request_id"]
    event_time: str = event["time"]
    detail_type: str = event["detail-type"]
    logger.info(f"{detail_type} triggered EHR Deletion Lambda at {event_time}, "
                f"with Request ID {invocation_request_id} - checking if any health records require deletion.")

    # Instantiate required services.
    database_service = DatabaseService()
    s3_service = S3Service()

    eligible_conversation_ids = database_service.fetch_all_eligible_records()
    successfully_deleted_conversation_ids = s3_service.delete_health_records_from_s3(eligible_conversation_ids)
    database_service.delete_records_from_ehr_repo_database(successfully_deleted_conversation_ids)

    return {
        "statusCode": 200
    }

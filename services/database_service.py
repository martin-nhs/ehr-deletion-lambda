import os

import pg8000.native

from loguru import logger
from exceptions.deletion_verification_exception import DeletionVerificationException
from utilities.database_utilities import get_ehr_repository_database_parameters


class DatabaseService:
    def __init__(self):
        self._ehr_repository_database_parameters = get_ehr_repository_database_parameters()
        self._deletion_interval = os.environ["DELETION_INTERVAL"]

    def fetch_all_eligible_records(self) -> list[str]:
        found_records = []
        sql_query = ("SELECT hr.conversation_id "
                     "FROM health_records hr "
                     "WHERE hr.deleted_at IS NOT NULL "
                     f"AND hr.deleted_at <= (now() - interval '{self._deletion_interval}') "
                     "GROUP BY hr.conversation_id;")

        with pg8000.native.Connection(**self._ehr_repository_database_parameters.connection_dictionary) as connection:
            for row in connection.run(sql_query):
                found_records.append(str(row[0]))

        found_records_length = len(found_records)

        if found_records_length > 0:
            logger.info(f"Found {found_records_length} health records eligible for deletion.")
            return found_records
        else:
            logger.warning("No eligible records were found.")
            return []

    def delete_records_from_ehr_repo_database(self, conversation_ids: list[str]) -> None:
        if len(conversation_ids) == 0:
            return

        formatted_conversation_ids = self._format_conversation_ids(conversation_ids)

        delete_health_records_sql_query = ("DELETE FROM health_records hr "
                                           "WHERE hr.conversation_id "
                                           f"IN ({formatted_conversation_ids});")

        delete_messages_sql_query = ("DELETE FROM messages m "
                                     "WHERE m.conversation_id "
                                     f"IN ({formatted_conversation_ids});")

        with pg8000.native.Connection(**self._ehr_repository_database_parameters.connection_dictionary) as connection:
            connection.run(delete_health_records_sql_query)
            connection.run(delete_messages_sql_query)

        self._verify_ehr_repository_records_deleted(conversation_ids)

    def _verify_ehr_repository_records_deleted(self, conversation_ids: list[str]) -> None:
        formatted_conversation_ids = self._format_conversation_ids(conversation_ids)
        sql_query = ("SELECT m.conversation_id "
                     "FROM messages m "
                     "WHERE m.conversation_id "
                     f"IN ({formatted_conversation_ids});")

        with pg8000.native.Connection(**self._ehr_repository_database_parameters.connection_dictionary) as connection:
            unsuccessful_ids = connection.run(sql_query)

            if len(unsuccessful_ids) != 0:
                raise DeletionVerificationException(
                    "The following Conversation ID(s) still exist within the EHR Repository database: "
                    f"{unsuccessful_ids} - these likely will require a manual deletion."
                )

            else:
                logger.info(f"Successfully deleted all record(s) for Conversation ID(s) {conversation_ids}.")

    @classmethod
    def _format_conversation_ids(cls, conversation_ids: list[str]):
        formatted_conversation_ids = ', '.join([f"'{conversation_id}'" for conversation_id in conversation_ids])
        return formatted_conversation_ids

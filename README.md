### PRM ORC Deletion Lambda

🎯 **Objective**

The objective of this lambda is to implement a method for removing S3 objects (i.e. health records) and sensitive data from various data sources within the ORC system. This ensures compliance with data protection regulations.

⚡ **Trigger Mechanism**

The lambda will be triggered by a scheduled CRON-based event facilitated through AWS EventBridge.

💲 **Required Environment Variables**

All the below environment variables **MUST** be set unless the lambda will not function as intended. 

| Variable Name                       | Description                                                                                                |
|-------------------------------------|------------------------------------------------------------------------------------------------------------|
| EHR_REPOSITORY_BUCKET_NAME          | The name of the repository S3 bucket.                                                                      |
| DELETION_INTERVAL                   | The interval required to pass for a record to be eligible for deletion. The default interval is `8 weeks`. |
| SLACK_WEBHOOK_SSM_PARAMETER_NAME    | The SSM parameter name for the Slack Webhook URL.                                                          |
| EHR_REPO_DB_HOST_SSM_PARAMETER_NAME | The SSM parameter name for the EHR Repository database host value.                                         |
| EHR_REPO_DB_USER_SSM_PARAMETER_NAME | The SSM parameter name for the EHR Repository database username.                                           |
| EHR_REPO_DB_PASS_SSM_PARAMETER_NAME | The SSM parameter name for the EHR Repository database password.                                           |
| EHR_REPO_DB_NAME_SSM_PARAMETER_NAME | The SSM parameter name for the EHR Repository database name.                                               |
| EHR_REPO_DB_PORT                    | The port number for the EHR Repository database, usually 5432 for PostgreSQL.                              |
| NHS_ENVIRONMENT                     | The NHS environment.                                                                                       |

🔌 **Third-Party Integrations**

| Integration | Description                                                                                                                                                  |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Slack       | Utilised for receiving notifications of failed deletions. Relevant personnel with the necessary permissions can investigate and manually delete if required. |

📦 **Required Libraries**

| Integration | Description                                                                        |
|-------------|------------------------------------------------------------------------------------|
| Boto3       | **Not required in production**, this is only required for local development.       |
| pg8000      | Used to interact and execute queries against PostgreSQL databases.                 |
| loguru      | A minimum-configuration comprehensive logging library for Python.                  | 

🛡️ **Required IAM Permissions**

* s3:DeleteObject - required to delete S3 objects from the repository bucket.
* s3:ListBucket - required to list objects within the repository bucket.
* ssm:GetParameter - required to fetch parameters from SSM.

---

♻️ **Future Improvements**

* Remove Verify EHR Repository deletions query and find a way to verify the records.
* Once the EHR Repository database is set up correctly (with a FK) we can use delete cascade to and boil the deletion query down to 1 operation.
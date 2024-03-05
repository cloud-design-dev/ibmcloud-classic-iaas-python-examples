import os
from ibm_secrets_manager_sdk.secrets_manager_v2 import *
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import logging
from dotenv import load_dotenv

load_dotenv()

sm_instance_id = os.environ.get('SM_INSTANCE_ID')
if not sm_instance_id:
    raise ValueError("SM_INSTANCE_ID environment variable not found")

sm_instance_region = os.environ.get('SM_INSTANCE_REGION')
if not sm_instance_region:
    raise ValueError("SM_INSTANCE_REGION environment variable not found")

class SMClient:
    def __init__(self, IBMCLOUD_API_KEY):
        self.IBMCLOUD_API_KEY = IBMCLOUD_API_KEY

    def create_authenticator(self):
        try:
            return IAMAuthenticator(self.IBMCLOUD_API_KEY)
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()

    def create_secrets_manager_service(self):
        try:
            authenticator = self.create_authenticator()
            secrets_manager_service = SecretsManagerV2(authenticator=authenticator)
            secrets_manager_service.set_service_url(f'https://{sm_instance_id}.{sm_instance_region}.secrets-manager.appdomain.cloud')
            return secrets_manager_service
        except ApiException as e:
            logging.error("API exception {}.".format(str(e)))
            quit()


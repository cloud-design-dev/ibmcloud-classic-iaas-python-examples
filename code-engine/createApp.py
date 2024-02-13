#!/usr/bin/env python3
# Author: Ryan Tiffany
# Copyright (c) 2023
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = 'ryantiffany'
import os
from ibm_code_engine_sdk.code_engine_v2 import CodeEngineV2
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

code_engine_project = os.environ.get('CODE_ENGINE_PROJECT')
if not code_engine_project:
    raise ValueError("CODE_ENGINE_PROJECT environment variable not found")

code_engine_region = os.environ.get('CODE_ENGINE_REGION')
if not code_engine_region:
    raise ValueError("CODE_ENGINE_REGION environment variable not found")



authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

code_engine_service = CodeEngineV2(authenticator=authenticator)
code_engine_service.set_service_url('https://api.'+code_engine_region+'.codeengine.cloud.ibm.com/v2')

all_results = []
pager = ProjectsPager(
    client=code_engine_service,
    limit=100,
)
while pager.has_next():
    next_page = pager.get_next()
    assert next_page is not None
    all_results.extend(next_page)

print(json.dumps(all_results, indent=2))
#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "9c5de523-493f-493d-b803-40e4162f4bbc") # 9c5de523-493f-493d-b803-40e4162f4bbc
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "e.2D929g-pkq-et1_zLIbPn-JJzaY.P_bP") # BNG)DC^1{G%2sc>M8V0Lc?Yw9

    CONNECTION_NAME = os.environ.get("ConnectionName", "ad-connection")

    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "ebdc9aa4-c570-466b-b0e0-fb350c396179")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "57aa96ad-478c-4dee-8340-367c88fab324")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://rhr-qna.azurewebsites.net/qnamaker")

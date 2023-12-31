#!/usr/bin/env python
######################################################################################################################
#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.                                                #
#                                                                                                                    #
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance    #
#  with the License. A copy of the License is located at                                                             #
#                                                                                                                    #
#      http://www.apache.org/licenses/LICENSE-2.0                                                                    #
#                                                                                                                    #
#  or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES #
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
#  and limitations under the License.                                                                                #
######################################################################################################################

import pytest
from llm_models.models.bedrock_anthropic_params import BedrockAnthropicLLMParams
from utils.constants import DEFAULT_BEDROCK_TEMPERATURE_MAP
from utils.enum_types import BedrockModelProviders


@pytest.mark.parametrize(
    "params, expected_response",
    [
        (
            {"max_tokens_to_sample": 512, "top_p": 0.2, "top_k": 0.2, "stop_sequences": "", "temperature": 0.2},
            {
                "max_tokens_to_sample": 512,
                "top_p": 0.2,
                "top_k": 0.2,
                "stop_sequences": [],
                "temperature": 0.2,
            },
        ),
        (
            {
                "max_tokens_to_sample": 512,
                "top_p": 0.2,
                "top_k": 0.2,
                "stop_sequences": ["human:", "ai:"],
                "temperature": 0.2,
            },
            {
                "max_tokens_to_sample": 512,
                "top_p": 0.2,
                "top_k": 0.2,
                "stop_sequences": ["ai:", "human:"],
                "temperature": 0.2,
            },
        ),
        (
            {
                "max_tokens_to_sample": 512,
                "top_p": 0.2,
                "top_k": 0.2,
                "stop_sequences": "",
            },
            {
                "max_tokens_to_sample": 512,
                "top_p": 0.2,
                "top_k": 0.2,
                "stop_sequences": [],
                "temperature": DEFAULT_BEDROCK_TEMPERATURE_MAP[BedrockModelProviders.ANTHROPIC.value],
            },
        ),
        (
            {},
            {
                "temperature": DEFAULT_BEDROCK_TEMPERATURE_MAP[BedrockModelProviders.ANTHROPIC.value],
            },
        ),
    ],
)
def test_ai21_params_dataclass_success(params, expected_response):
    bedrock_params = BedrockAnthropicLLMParams(**params)
    assert bedrock_params.temperature == expected_response["temperature"]
    assert bedrock_params.max_tokens_to_sample is expected_response.get("max_tokens_to_sample", None)
    assert bedrock_params.top_p == expected_response.get("top_p", None)
    assert bedrock_params.top_k == expected_response.get("top_k", None)
    assert bedrock_params.stop_sequences == expected_response.get("stop_sequences", [])


@pytest.mark.parametrize(
    "pop_null, params, expected_response",
    [
        (
            True,
            {"top_p": 0.2},
            {
                "top_p": 0.2,
                "temperature": DEFAULT_BEDROCK_TEMPERATURE_MAP[BedrockModelProviders.ANTHROPIC.value],
            },
        ),
        (
            True,
            {},
            {
                "temperature": DEFAULT_BEDROCK_TEMPERATURE_MAP[BedrockModelProviders.ANTHROPIC.value],
            },
        ),
        (
            False,
            {},
            {
                "max_tokens_to_sample": None,
                "top_p": None,
                "top_k": None,
                "stop_sequences": [],
                "temperature": DEFAULT_BEDROCK_TEMPERATURE_MAP[BedrockModelProviders.ANTHROPIC.value],
            },
        ),
        (
            False,
            {"top_p": 0.2},
            {
                "max_tokens_to_sample": None,
                "top_p": 0.2,
                "top_k": None,
                "stop_sequences": [],
                "temperature": DEFAULT_BEDROCK_TEMPERATURE_MAP[BedrockModelProviders.ANTHROPIC.value],
            },
        ),
    ],
)
def test_ai21_get_params_as_dict(pop_null, params, expected_response):
    bedrock_params = BedrockAnthropicLLMParams(**params)
    assert bedrock_params.get_params_as_dict(pop_null=pop_null) == expected_response

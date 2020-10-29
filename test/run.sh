#!/bin/bash

export GITHUB_SHA=1d20217
export GITHUB_EVENT_PATH="$( dirname "${BASH_SOURCE[0]}" )"/files/event.json
export GITHUB_EVENT_NAME="pull_request"

export INPUT_TFLINT_DISABLED_RULES='terraform_unused_declarations'
export INPUT_TFLINT_CHANGED_ONLY=true
export INPUT_TFLINT_CONFIG_FILE=true
export INPUT_TFLINT_DEBUG=true
export INPUT_TFLINT_ENABLED_RULES='terraform_deprecated_interpolation terraform_deprecated_index terraform_comment_syntax terraform_documented_outputs terraform_documented_variables terraform_typed_variables terraform_module_pinned_source terraform_naming_convention terraform_required_version terraform_required_providers terraform_standard_module_structure terraform_workspace_remote'
export INPUT_TFLINT_EXTRA_OPTIONS='--no-color'
export INPUT_TFLINT_PATH="$( dirname "${BASH_SOURCE[0]}" )"/files
export INPUT_TFLINT_RECURSE=false
export INPUT_TFLINT_TAG_LINES=true

$( dirname "${BASH_SOURCE[0]}" )/../main.py
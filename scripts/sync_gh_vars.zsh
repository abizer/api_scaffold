#!/bin/zsh

set -euo pipefail

if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed or not in PATH"
    echo "Please install gh CLI and try again"
    exit 1
fi

echo "loading secrets"
typeset -A gh_secrets
gh_secrets=(
    FLY_API_TOKEN_APP_PROD "$(op read 'op://scaffold/FLY_API_TOKEN/exampleproject-api-prod')"
    FLY_API_TOKEN_APP_STAGING "$(op read 'op://scaffold/FLY_API_TOKEN/exampleproject-api-staging')"
)

echo "loading variables"
typeset -A gh_variables
gh_variables=(
    # nothing for now, only need the fly secrets 
)

gh_write_secrets() {
    echo "writing secrets"
    tmpfile=$(mktemp)
    for secret_name value in ${(kv)gh_secrets}; do
        echo "$secret_name=$value" >> "$tmpfile"
    done
    echo "setting secrets"
    gh secret set -f "$tmpfile"
    rm "$tmpfile"
}

gh_write_variables() {
    echo "writing variables"
    tmpfile=$(mktemp)
    for secret_name value in ${(kv)gh_variables}; do
        echo "$secret_name=$value" >> "$tmpfile"
    done
    echo "setting variables"
    gh secret set -f "$tmpfile"
    rm "$tmpfile"
}

gh_write_variables 

gh_write_secrets

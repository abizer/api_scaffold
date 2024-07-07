default:
    @just --list

project := "exampleproject-api"
app := "app"
env := "local"

test:
  poetry run pytest 

run:
  poetry run uvicorn app.main:app --port 8080 --reload --log-level debug

op-render-env:
  PROJECT_NAME={{project}} APP_ENV={{env}} op inject -i env.tmpl -o .env 

flyexec env cmd:
  fly -c fly.{{project}}-{{env}}.toml -a {{project}}-{{env}} {{cmd}}

fly-logs env="staging":
  just flyexec {{env}} logs
alias logs := fly-logs

fly-status env="staging":
  just flyexec {{env}} status
alias status := fly-status
alias st := fly-status

fly-sync-secrets env="staging":
  APP_ENV={{env}} op inject -i env.tmpl -o .fly.secrets
  cat .fly.secrets | just flyexec {{env}} "secrets import"
  rm .fly.secrets

fly-ls-secrets env="staging":
  just flyexec {{env}} "secrets list"

gh-sync-secrets:
  scripts/sync_gh_vars.zsh

gh-ls-secrets:
  gh secrets list 

gh-ls-variables:
  gh variables list

gh-deploy env:
  gh api \
    --method POST \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    /repos/abizer/api_scaffold/actions/workflows/deploy_{{project}}-{{env}}.yml/dispatches \
    -f "ref=master"
alias deploy := gh-deploy

gh-workflows env="staging":
  @gh run ls -w deploy_{{project}}-{{env}}.yml
alias workflows := gh-workflows
alias wf := gh-workflows

alembic-check:
  poetry run alembic check
alias check := alembic-check

alembic-migrate msg:
  poetry run alembic revision --autogenerate -m {{msg}}
alias migrate := alembic-migrate

alembic-upgrade:
  poetry run alembic upgrade head
alias upgrade := alembic-upgrade

poetry-update:
  poetry update
alias update := poetry-update
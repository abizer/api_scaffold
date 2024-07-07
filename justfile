default:
    @just --list

project := "scaffold"
app := "app"
env := "local"

op-render-env:
  PROJECT_NAME={{project}} APP_ENV={{env}} op inject -i env.tmpl -o .env 
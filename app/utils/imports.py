import importlib


def import_from_models(models):
    for name in models.__all__:
        importlib.import_module(getattr(models, name).__module__)


def import_from_crud(crud):
    models = []
    for name in crud.__all__:
        # e.g. CRUDApiKey
        crud_object = getattr(crud, name)
        # e.g. ApiKey
        model_class = crud_object.model
        # e.g. app.modules.api_key.models
        module_name = model_class.__module__
        # e.g. ApiKey
        class_name = model_class.__name__
        module = importlib.import_module(module_name)
        model = getattr(module, class_name)
        models.append(model)
    return models

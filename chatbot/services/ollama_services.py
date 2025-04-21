import ollama

def get_models():
    models=ollama.list()
    print(type(models.models))
    print(models.models)

    models=[{"name":model.model,"size":model.details.parameter_size} for model in models.models]
    print(models)
    return models
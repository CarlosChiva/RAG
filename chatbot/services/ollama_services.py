import ollama

def get_models():
    models=ollama.list()
    models=[{"name":model.model,"size":model.details.parameter_size} for model in models.models]
    return models
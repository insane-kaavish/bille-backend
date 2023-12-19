import pickle

# load the model from disk
def model_load():
    model_filename = 'model.sav'
    model = pickle.load(open(model_filename, 'rb'))


import pickle

# load the model from disk
model_filename = 'model.sav'
model = pickle.load(open(model_filename, 'rb'))


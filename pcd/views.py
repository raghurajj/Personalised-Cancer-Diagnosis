from django.shortcuts import render
import json
import pickle
import re
import numpy as np




GENE_FILE = 'geneFeatures.sav'
TEXT_FILE = 'textFeatures.sav'
MODEL_FILE = 'finalized_model.sav'
VARIATION_FILE = 'variationFeatures.sav'
BASE_FILES_PATH = '/home/jm1shra/PersonalizedCancerDiagnosis/Personalised-Cancer-Diagnosis/mysite/'

def loadVariationFeatures():
    print('loadVariationWasCalled')
    return pickle.load(open(BASE_FILES_PATH + VARIATION_FILE,'rb'))

def loadGeneFeatures():
    print('loadGeneWasCalled')
    return pickle.load(open(BASE_FILES_PATH + GENE_FILE, 'rb'))

def loadTextFeatures():
    print('load')
    return pickle.load(open(BASE_FILES_PATH + TEXT_FILE, 'rb'))

def loadModel():
    return pickle.load(open(BASE_FILES_PATH + MODEL_FILE, 'rb'))

variationFeatures = loadVariationFeatures()
geneFeatures = loadGeneFeatures()
textFeatures = loadTextFeatures()
logistic_model = loadModel()



# Create your views here.

# def createVariationVector(word, features):
#   variationvector = [0]*len(features)
#   i = 0
#   for feature in features:
#     if feature == word:
#       variationvector[i] = 1 
#       break
#   return variationvector

def createVariationVector(variation, features):
  variationvector = [0]*len(features)
  i = 0
  for feature in features:
    if feature == variation:
      variationvector[i] = 1 
      break
  return variationvector

def createGeneVector(gene, features):
  geneVector = [0]*len(features)
  i = 0
  for feature in features:
    if feature == gene:
      geneVector[i] = 1 
      break
  return geneVector


def getList(text, gene='',variation=''):
    print('----------------------------------------------------------------')
    if (text is None) or (len(text) == 0):
        text = gene + ' ' + variation 
        print(text)

    text = re.sub('[^a-zA-Z0-9\n]', ' ', text)
    text = re.sub('\s+',' ', text)
    text = text.lower()
    print(text)
    return text.split(' ')

def createTextVector(text, features, gene='', variation=''):
    textVector = [0]*len(features)
    textList = getList(text, gene, variation)
    i = 0
    for feature in features:
        if feature in textList:
            textVector[i] = 1
    return textVector




def home(request):
    gene = request.POST.get('gene')
    variation = request.POST.get('variation')
    text = request.POST.get('research')

    # print(variationFeatures)
    # print(type(geneFeatures))
    # print(variationFeatures)
    # print(variationFeatures)
    

    class_title=""
    interpretation= ""

    if request.method == 'POST':
        class_title=" this is title "
        interpretation= " this is somethingelse"   
        # print(getList(text, gene, variation))
        genevector = createGeneVector(gene, geneFeatures)
        variationvector = createVariationVector(variation, variationFeatures)
        textvector = createTextVector(text,textFeatures, gene, variation)
        print(len(genevector) , len(variationvector), len(textvector))

        inputdata = genevector + variationvector + textvector
        print(f'size of input data {len(inputdata)}')
        norm = [float(data) / (sum(inputdata)+1)  for data in inputdata]

        return render(request, 'pcd/index.html', {"class": logistic_model.predict_proba(np.array(norm).reshape(1,-1)) ,"interpretation":variation})
        
    return render(request, 'pcd/index.html', {"class":'',"interpretation":''})

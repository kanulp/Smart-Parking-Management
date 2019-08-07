import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('json path')
firebase_admin.initialize_app(cred)

db = firestore.client()
#doc_ref = db.collection(u'users').document(u'demouser')
#doc_ref.set({
#    u'first': u'Karan',
#    u'last': u'Gajjar',
#    u'born': 2018
#})

# Set the capital field
db.collection(u'spots').document(u'id').update({u'vacant': 'fasle'})

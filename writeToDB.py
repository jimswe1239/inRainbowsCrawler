


def writeRecord(therapist):
    doc_ref = db.collection('users').document(str(therapist.name))
    doc = doc_ref.get()
    if not doc.exists:
        doc_ref.set({
            'first': therapist.name.first,
            'last': therapist.name.last,
            'born': 2000
        })

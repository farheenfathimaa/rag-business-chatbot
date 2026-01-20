def ingest_docs(files, business_id, access):
    docs = []
    for file in files:
        loader = PyMuPDFLoader(file)
        loaded = loader.load()

        for d in loaded:
            d.metadata.update({
                "business_id": business_id,
                "access": access
            })
            docs.append(d)

    return docs

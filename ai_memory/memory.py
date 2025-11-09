import chromadb


class Memory:
    def __init__(self, name="ai_memory"):
        self.client = chromadb.PersistentClient(path="./data")
        self.collection = self.client.get_or_create_collection(name)

    def add_document(self, title, text):
        self.collection.add(documents=[text], metadatas=[
                            {"source": title}], ids=[title])

    def search(self, query, n=3):
        return self.collection.query(query_texts=[query], n_results=n)

    def persist(self):
        pass

import pandas as pd
import math
class Entropy:
    def __init__(self):
        self.collection = []
        self.freqs = {}
    def get_item_entropy(self, item_name: str) -> float:
        if not self.freqs:
            raise NameError("Frequencies not calculated.")
        return abs(-math.log10(self.freqs.get(item_name,1))) #abs to fix log10(1) = -0
    def calculate(self):
        if not self.freqs:
            collection = pd.Series(self.collection)
            counts = collection.value_counts()
            freqs = counts/self.n_collection
            self.freqs = freqs.to_dict()
        return self.freqs

    def accept(self, visitor):
        visitor.visit(self)

class EntropyVisitor:
    def __init__(self, collection: list) -> None:
        self.n_collection = len(collection)
        collection = [item for sublist in collection for item in sublist]
        self.collection = collection
    def visit(self, element):
        element.collection = self.collection
        element.n_collection = self.n_collection

__entropy = Entropy()

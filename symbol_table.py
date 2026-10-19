class SymbolTable:
    def __init__(self, buckets=17):
        self.bucket_count = buckets
        self.table = [[] for _ in range(self.bucket_count)]

    def insert(self, symbol):
        pos = self.search(symbol)
        if self.search(symbol) != -1:
            return pos

        index = self.get_hash_index(symbol)
        self.table[index].append(symbol)
        list_index = len(self.table[index]) - 1
        return (index, list_index)

    def search(self,symbol):
        index = self.get_hash_index(symbol)
        for list_index, existing_symbol in enumerate(self.table[index]):
            if existing_symbol == symbol:
                return (index, list_index)
        return -1

    def display(self):
        with open("outputs/ST.out", "w") as f:
            f.write(f"{'Bucket':<8} | {'Position':<8} | Symbol\n")
            f.write("-" * 35 + "\n")
            for bucket_idx, bucket in enumerate(self.table):
                for list_idx, symbol in enumerate(bucket):
                    f.write(f"{bucket_idx:<8} | {list_idx:<8} | {symbol}\n")

    def get_hash_index(self,symbol):
        return sum(ord(c) for c in str(symbol)) % self.bucket_count

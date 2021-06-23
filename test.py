class Animal():
    def __init__(self, nama, jenis):
        self.nama = nama
        self.jenis = jenis

    def ngocok(self):
        return self.nama


class Anjing(Animal):
    def __init__(self, nama, jenis):
        super().__init__(nama, jenis)

    def ngocok(self):
        return self.jenis


anjing = Anjing("meki", "bulldog")
print(anjing.ngocok())

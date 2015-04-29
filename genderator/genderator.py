class Genderator:

    names = {}
    ratios = {}
    surnames = []

    def __init__(self):
        self.load_data()

    def load_data(self):
        self.load_names()
        self.load_name_surname_ratios()
        self.load_surnames()

    def load_names(self):
        with open('data/names_ine') as file:
            for line in file:
                if not line.startswith('#'):
                    (name, prob_female, prob_male) = line.rstrip().split('\t')
                    self.names[name] = float(prob_male)

    def load_name_surname_ratios(self):
        with open('data/name_surname_ratio') as file:
            for line in file:
                if not line.startswith('#'):
                    (key, val) = line.rstrip().split('\t')
                    self.ratios[key] = float(val)

    def load_surnames(self):
        with open('data/surnames_ine') as file:
            for line in file:
                if not line.startswith('#'):
                    self.surnames.append(line.rstrip())

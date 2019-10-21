import json, levenshtein


class AAcidDictionary:
    def __init__(self, fp):
        with open(fp) as f:
            self.codon_data = json.load(f)

        self.search_space = set()

        self.inverse_codon_data = {}

        for amino_acid in self.codon_data:
            self.search_space.add(amino_acid.lower())
            for acid_info in self.codon_data[amino_acid]:
                data_entry = self.codon_data[amino_acid][acid_info]
                if type(data_entry) == list:
                    for info in data_entry:
                        self.search_space.add(info.lower())
                        if info in self.inverse_codon_data:
                            self.inverse_codon_data[info.lower()].append(amino_acid)
                        else:
                            self.inverse_codon_data[info.lower()] = [amino_acid]
                else:
                    self.search_space.add(data_entry.lower())
                    key = data_entry.lower()
                    if key in self.inverse_codon_data:
                        self.inverse_codon_data[key].append(amino_acid)
                    else:
                        self.inverse_codon_data[key] = [amino_acid]
        self.search_space = list(self.search_space)

        #print(len(self.search_space), str(self.search_space))

        self.levenshtein_engine = levenshtein.Levenshtein(u=(7, 1, 4), t=(7, 1, 4))

    def find_amino_acid(self, character):
        if character in self.codon_data:
            yield (character, self.codon_data[character])
        elif character in self.inverse_codon_data:
            for entry in self.inverse_codon_data[character]:
                yield (entry, self.codon_data[entry])

    def get_search_space(self):
        return self.search_space

    def query(self, word):
        searchWord = word.lower()
        results = []

        # find the distance from the query to each word in the search space
        for v in self.get_search_space():
            distance = self.levenshtein_engine.get_distance(searchWord, v.lower())
            results.append((distance, v))

        # sort results by levenshtein distance
        results.sort()

        # create a generator for the results so a separate lookup call is not needed
        # effectively returns an iterable of the closest results
        for result in results:
            search_space_term = result[1]
            yield (search_space_term, self.find_amino_acid(search_space_term))

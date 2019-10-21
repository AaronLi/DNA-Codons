class Levenshtein:
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    def __init__(self, **weight_dict):
        self.w = dict(((letter, (7, 1, 6)) for letter in Levenshtein.alphabet + Levenshtein.alphabet.upper()))

        if weight_dict:
            self.w.update(weight_dict)

    def get_distance(self, s, t):
        """
            Levenshtein.get_distance(s, t) -> ldist
            ldist is the Levenshtein distance between the strings
            s and t.
            For all i and j, dist[i,j] will contain the Levenshtein
            distance between the first i characters of s and the
            first j characters of t

            weight_dict: keyword parameters setting the costs for characters,
                         the default value for a character will be 1
        """
        rows = len(s) + 1
        cols = len(t) + 1

        dist = [[0 for i in range(cols)] for i in range(rows)]
        # source prefixes can be transformed into empty strings
        # by deletions:
        for row in range(1, rows):
            dist[row][0] = dist[row - 1][0] + self.w[s[row - 1]][0]
        # target prefixes can be created from an empty source string
        # by inserting the characters
        for col in range(1, cols):
            dist[0][col] = dist[0][col - 1] + self.w[t[col - 1]][1]

        for col in range(1, cols):
            for row in range(1, rows):
                deletes = self.w[s[row - 1]][0]
                inserts = self.w[t[col - 1]][1]
                subs = max((self.w[s[row - 1]][2], self.w[t[col - 1]][2]))
                if s[row - 1] == t[col - 1]:
                    subs = 0
                else:
                    subs = subs
                dist[row][col] = min(dist[row - 1][col] + deletes,
                                     dist[row][col - 1] + inserts,
                                     dist[row - 1][col - 1] + subs)  # substitution

        return dist[row][col]

if __name__ == "__main__":
    levenshtein_engine = Levenshtein()
    print(levenshtein_engine.get_distance("lycine", "lycane"))
    print(levenshtein_engine.get_distance("guan", "leycein"))
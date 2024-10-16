class Levenshtein:
     def distance(self, string1, string2):
        distance = [[c for c in range(len(string1)+1)] for r in range(len(string2)+1)]
        
        for r in range(1, len(string2)+1):
            distance[r][0] = distance[r-1][0] + 1
        
        for r in range(1, len(string2)+1):
            for c in range(1, len(string1)+1):
                if string1[c-1] == string2[r-1]:
                    distance[r][c] = distance[r-1][c-1]
                else:
                    distance[r][c] = 1 + min(distance[r][c-1], 
                                             distance[r-1][c-1], 
                                             distance[r-1][c])
        return distance[-1][-1]
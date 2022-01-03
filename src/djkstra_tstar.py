class Djkstra():
    def __init__(self):
        pass

    def run(self, Gr):
        counter = 0
        dic = {}
        for i in Gr:
            for j in i:
                if j[2][0] not in dic:
                    counter += 1
                    if j[0][0] in dic:
                        dic[j[2][0]] = {"cost": j[1]+ dic[j[0][0]]["cost"], "prev": j[0][0], "state":j[2][1]}
                    else:
                        dic[j[2][0]] = {"cost": j[1], "prev": j[0][0], "state":j[2][1]}
                else:
                    counter += 1
                    if j[0][0] in dic:
                        if dic[j[2][0]]["cost"] > (j[1]+ dic[j[0][0]]["cost"]):
                            dic[j[2][0]] = {"cost": j[1]+ dic[j[0][0]]["cost"], "prev": j[0][0], "state":j[2][1]}
                    else:
                        if dic[j[2][0]]["cost"] > j[1]:
                            dic[j[2][0]] = {"cost": j[1], "prev": j[0][0], "state":j[2][1]}
                    
        k = list(dic.keys())[-1]
        s = dic[k]["state"]
        liste = []
        while True:
            liste.append((k,s))
            k = dic[k]["prev"]
            s = dic[k]["state"]
            if k == liste[0][0]:
                liste.append((k,s))
                break
        liste.reverse()
        return liste, counter
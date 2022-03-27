class ModelLoader:
    def __init__(self, path):
        self.path = path
        self.v = []
        self.f = []
        self.vd = []
        
    def load_all(self):
        count = 0
        with open(self.path, 'r') as file:
            for line in file:
                if ("object" in line): 
                    self.vd.append(len(self.v))
                    continue
                l = line.split()
                if len(l) == 0: continue
                if l[0] == 'v':
                    self.v.extend(list(map(float, l[1:4])))
                elif l[0] == 'f':
                    self.f.extend([x - 1 for x in list(map(float, l[1:4]))]) 
                    
        self.vd.append(len(self.v))

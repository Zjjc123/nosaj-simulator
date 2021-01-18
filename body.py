class Body:
    def __init__(self, mass, p0, v0, f0=0):
        self.mass = mass
        self.position = p0 # 1x3 array
        self.velocity = v0 # 1x3 array
        self.force = f0 

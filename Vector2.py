import math
class Vector2:
    def __repr__(self):
        return str("X :"+str(self.x)+ " Y :"+str(self.y))

    def __init__(self,x,y):
            self.x = x
            self.y = y

    @classmethod
    def fromTuple(self,t):
        self.x = t[0]
        self.y = t[1]
    
    def cp(self):
        return Vector2(self.x,self.y)

    def __sub__(self,v):
        try:
            return Vector2(self.x-v.x,self.y-v.y)
        except:
            try:
                return Vector2(self.x-v[0],self.y-v[1])
            except:
                try:
                    return Vector2(self.x-v,self.y-v)
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")

    def __isub__(self,v):
        try:
            self.x-=v.x
            self.y-=v.y
        except:
            try:
                self.x-=v.x[0]
                self.y-=v.y[1]
            except:
                try:
                    self.x-=v
                    self.y-=v
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")
        return self

    def __add__(self,v):
        try:
            return Vector2(self.x+v.x,self.y+v.y)
        except:
            try:
                return Vector2(self.x+v[0],self.y+v[1])
            except:
                try:
                    return Vector2(self.x+v,self.y+v)
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")
        
    def __iadd__(self,v):
        try:
            self.x+=v.x
            self.y+=v.y
        except:
            try:
                self.x+=v.x[0]
                self.y+=v.y[1]
            except:
                try:
                    self.x+=v
                    self.y+=v
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")
        return self

    def __div__(self,v):
        try:
            return Vector2(self.x/v.x,self.y/v.y)
        except:
            try:
                return Vector2(self.x/v[0],self.y/v[1])
            except:
                try:
                    return Vector2(self.x/v,self.y/v)
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")

    def __idiv__(self,v):
        v= float(v)
        try:
            self.x/=v.x
            self.y/=v.y
        except:
            try:
                self.x/=v.x[0]
                self.y/=v.y[1]
            except:
                try:
                    self.x/=v
                    self.y/=v
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")
        return self

    def __mul__(self,v):
        try:
            return Vector2(self.x*v.x,self.y*v.y)
        except:
            try:
                return Vector2(self.x*v[0],self.y*v[1])
            except:
                try:
                    return Vector2(self.x*v,self.y*v)
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")

    def __imul__(self,v):
        try:
            self.x*=v.x
            self.y*=v.y
        except:
            try:
                self.x*=v.x[0]
                self.y*=v.y[1]
            except:
                try:
                    self.x*=v
                    self.y*=v
                except:
                    raise ValueError("informe um Vector2, uma tupla (x,y) ou um escalar")
        return self

    def get_int(self):
        return(int(self.x),int(self.y))

    def zero(self):
            self.x = 0.0
            self.y = 0.0


    def set(self,v):
        try:
            self.x = v[0]
            self.y = v[1]
        except:
            try:
                self.x=v.x
                self.y=v.y
            except:
                raise ValueError("informe uma Tupla (x,y) ou Vector2")


    def normal(self):
        t = self.tamanho()
        if t == 0:
            return Vector2(0.0,0.0)
        else:    
            return Vector2(self.x/float(t),self.y/float(t))

    def tamanho(self):
        return(math.sqrt((self.x*self.x)+(self.y*self.y)))

    def dot(self,v):
        return((self.x * v.x)+(self.y * v.y))


    def rot(self,graus):
        self.x = ((self.x*math.cos(graus)) - (self.y*math.sin(graus)))
        self.y = ((self.x*math.sin(graus)) + (self.y*math.cos(graus)))

    def truncate(self, max):
        t = self.tamanho() 
        if  t == 0:
            t = 1
        i = max / t
        if i > 1.0:
            i = 1.0
        self.x *= i
        self.y *= i
from collections import defaultdict

class Intcode:
    def __init__(self, xs, inputs=[], pos=0):
        self.xs = defaultdict(int)
        self.xs.update({(i,x) for i,x in enumerate(xs)})
        self.pos = pos
        self.rel_base = 0
        self.inputs = inputs
        self.res = []
        
    def display(self):
        return dict(enumerate(self.xs))
    
    @staticmethod
    def parse_op(x):
        params, op = divmod(x, 100)
        params, p1 = divmod(params, 10)
        params, p2 = divmod(params, 10)
        p3 = params % 10
        return op, p1, p2, p3
    
    def get_value(self,i,p):
        if p == 0:
            return self.xs[i]   
        elif p == 1:
            return i
        elif p == 2:
            i_ = i + self.rel_base
            return self.xs[i_]
        else:
            print("Something went wrong, mode", p, i)
    
    def set_value(self,i,p):
        if p == 0:
            return i
        elif p == 2:
            i_ = i + self.rel_base
            return i_
        else:
            print("Something went wrong, mode", p, i)
    
    def op1(self,i1,i2,out,ps):
        p1, p2, pout = ps
        i1_ = self.get_value(i1, p1)
        i2_ = self.get_value(i2, p2)
        out_ = self.set_value(out, pout)
        self.xs[out_] = i1_ + i2_
        return 4
    
    def op2(self,i1,i2,out,ps):
        p1, p2, pout = ps
        i1_ = self.get_value(i1, p1)
        i2_ = self.get_value(i2, p2)
        out_ = self.set_value(out, pout)
        self.xs[out_] = i1_ * i2_
        return 4

    def op3(self,x,i,ps):
        p, *_ = ps
        i_ = self.set_value(i, p)
        self.xs[i_] = x
        return 2

    def op4(self,i,ps):
        p, *_ = ps
        i_ = self.get_value(i, p)
        self.res.append(i_)
        if i_ == -1:
            pass
        return 2
    
    def op5(self,i,out,ps):
        pi, pout, _ = ps
        i_ = self.get_value(i, pi)
        out_ = self.get_value(out, pout)
        if i_ != 0:
            self.pos = out_
            return 0
        return 3
    
    def op6(self,i,out,ps):
        pi, pout, _ = ps
        i_ = self.get_value(i, pi)
        out_ = self.get_value(out, pout)
        if i_ == 0:
            self.pos = out_
            return 0
        return 3
    
    def op7(self,i1,i2,out,ps):
        p1, p2, pout = ps
        i1_ = self.get_value(i1, p1)
        i2_ = self.get_value(i2, p2)
        out_ = self.set_value(out, pout)
        self.xs[out_] = 1 if i1_ < i2_ else 0
        return 4
    
    def op8(self,i1,i2,out,ps):
        p1, p2, pout = ps
        i1_ = self.get_value(i1, p1)
        i2_ = self.get_value(i2, p2)
        out_ = self.set_value(out, pout)
        self.xs[out_] = 1 if i1_ == i2_ else 0
        return 4
    
    def op9(self,i,ps):
        p, *_ = ps
        i_ = self.get_value(i, p)
        self.rel_base += i_
        return 2

    def input(self, x=None):
        if x is not None:
            self.inputs.append(x)
        return self

    def run(self):
        list(self)
        return self.res[-1]

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            op, *params = self.parse_op(self.xs[self.pos])
            if op == 1:
                i1, i2, out = [self.xs[x] for x in range(self.pos+1,self.pos+4)]
                self.pos += self.op1(i1, i2, out, params)
            elif op == 2:
                i1, i2, out = [self.xs[x] for x in range(self.pos+1,self.pos+4)]
                self.pos += self.op2(i1, i2, out, params)
            elif op == 3:
                x = self.inputs.pop(0)
                i_ = self.xs[self.pos+1]
                self.pos += self.op3(x, i_, params)
            elif op == 4:
                i = self.xs[self.pos+1]
                self.pos += self.op4(i, params)
                return self.res[-1]
            elif op == 5:
                i, out = [self.xs[x] for x in range(self.pos+1,self.pos+3)]
                p = self.op5(i, out, params)
                self.pos += p
            elif op == 6:
                i, out = [self.xs[x] for x in range(self.pos+1,self.pos+3)]
                p = self.op6(i, out, params)
                self.pos += p
            elif op == 7:
                i1, i2, out = [self.xs[x] for x in range(self.pos+1,self.pos+4)]
                self.pos += self.op7(i1, i2, out, params)
            elif op == 8:
                i1, i2, out = [self.xs[x] for x in range(self.pos+1,self.pos+4)]
                self.pos += self.op8(i1, i2, out, params)
            elif op == 9:
                i1 = self.xs[self.pos+1]
                self.pos += self.op9(i1, params)
            elif op == 99:
                raise StopIteration
            else:
                print("invalid instruction!", op)
                raise StopIteration
                break
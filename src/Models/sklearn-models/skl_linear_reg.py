from sklmodel import sklModel
class sklLinearReg(sklModel):
    
    def __init__(self, **params):
        self.model = LinearRegression()
        if len(params) > 0:
            self.set_params(**params)

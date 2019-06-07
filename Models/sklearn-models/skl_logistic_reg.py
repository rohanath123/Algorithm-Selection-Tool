from sklmodel import sklModel
class sklLogisticReg(sklModel):
    
    def __init__(self, **params):
        self.model = LogisticRegression()
        if len(params) > 0:
            self.set_params(**params)
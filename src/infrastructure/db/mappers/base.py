class BaseMapper:

    @staticmethod
    def to_domain(model):
        raise NotImplementedError
    
    @staticmethod
    def to_model(domain):
        raise NotImplementedError

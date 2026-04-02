class BaseMapper:

    @staticmethod
    def to_domain(model):
        raise NotImplementedError
    
    @staticmethod
    def to_model(domain):
        raise NotImplementedError

    @staticmethod
    def update_model(model, domain) -> None:
        raise NotImplementedError

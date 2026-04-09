class ImageNotFoundException(Exception):
    def __init__(self, image_id: str):
        self.image_id = image_id
        self.message = f"Image with id {image_id} not found in storage"
        super().__init__(self.message)

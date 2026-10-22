class UserProfile:
    def __init__(self, user, avatar, bio):
        self.user = user
        self.avatar = avatar
        self.bio = bio

    def update_bio(self, new_bio):
        if len(new_bio) > 500:
            raise ValueError("Тайлбар хэт урт байна")
        self.bio = new_bio
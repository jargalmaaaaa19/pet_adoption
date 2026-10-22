def test_user_profile_creation():
    user = User("Бат", "бат@example.com")
    profile = UserProfile(user, "Зураг", "Би веб хөгжүүлэгч")
    assert profile.user.name == "Бат"
    assert profile.avatar == "Зураг"
    assert profile.bio == "Би веб хөгжүүлэгч"
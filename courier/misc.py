
def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()
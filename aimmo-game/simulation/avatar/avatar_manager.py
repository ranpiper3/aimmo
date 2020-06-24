from simulation.avatar.avatar_wrapper import avatar_wrapper_factory
from simulation.avatar.avatar_appearance import AvatarAppearance


class AvatarManager(object):
    """
    Stores all game avatars.
    """

    def __init__(self):
        self.avatars_by_id = {}

    def add_avatar(self, player_id, location):
        worksheet_id = 2

        avatar = avatar_wrapper_factory(
            worksheet_id,
            player_id,
            location,
            AvatarAppearance("#000", "#ddd", "#777", "#fff"),
        )
        self.avatars_by_id[player_id] = avatar
        return avatar

    def get_avatar(self, user_id):
        return self.avatars_by_id[user_id]

    def remove_avatar(self, user_id):
        del self.avatars_by_id[user_id]

    def clear_all_avatar_logs(self):
        for avatar in self.avatars:
            avatar.clear_logs()

    @property
    def avatars(self):
        return list(self.avatars_by_id.values())

    @property
    def active_avatars(self):
        return self.avatars[:]

    def serialize_players(self):
        """
        To be called on a required update of players in the front-end of the game.
        """

        return [player.serialize() for player in self.avatars]

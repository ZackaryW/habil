from habil_base.habiToken import token_required


class HabiCharacter:
    @classmethod
    @token_required()
    def get(cls, token=None):
        pass
from django.db.models import ForeignKey


class UidForeignKey(ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('to_field', 'uid')
        super().__init__(*args, **kwargs)

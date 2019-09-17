from db import db


class Base(object):
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_id_for_user(cls, user_id, id):
        return cls.query.filter_by(user_id=user_id, id=id).first()

    @classmethod
    def get_all_for_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit is True:
            db.session.commit()
        return self.id

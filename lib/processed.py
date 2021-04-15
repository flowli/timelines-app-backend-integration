import pickledb


class Processed:
    entity_name = None
    db = None

    def __init__(self, entity_name, db_path):
        self.entity_name = entity_name
        db_file = db_path + "/" + entity_name + ".db"
        self.db = pickledb.load(db_file, True)

    def now(self, entity):
        self.db.set(self.entity_name + "=" + str(entity.id()), True)

    def has_been(self, entity):
        return not self.not_yet(entity)

    def not_yet(self, entity):
        return self.db.get(self.entity_name + "=" + str(entity.id())) is False

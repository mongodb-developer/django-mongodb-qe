class EncryptedRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == "riskapp":
            return db == "encrypted"

        if db == "encrypted":
            return False
        return None

    def db_for_read(self, model, **hints):

        if model._meta.app_label == "riskapp":
            return "encrypted"
        return None

    db_for_write = db_for_read

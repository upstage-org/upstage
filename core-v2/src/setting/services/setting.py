import os
from config.database import DBSession, ScopedSession
from config.env import NGINX_CONFIG_FILE
from core.helpers.object import convert_keys_to_camel_case
from mails.helpers.mail import send
from setting.entities.config import ConfigEntity
from setting.http.validation import ConfigInput, EmailInput

TERMS_OF_SERVICE = "TERMS_OF_SERVICE"
MANUAL = "MANUAL"
EMAIL_SUBJECT_PREFIX = "EMAIL_SUBJECT_PREFIX"
ENABLE_DONATE = "ENABLE_DONATE"
FOYER_TITLE = "FOYER_TITLE"
FOYER_DESCRIPTION = "FOYER_DESCRIPTION"
FOYER_MENU = "FOYER_MENU"
SHOW_REGISTRATION = "SHOW_REGISTRATION"

app_dir = os.path.abspath(os.path.dirname(__file__))
prodder = os.path.abspath(os.path.join(app_dir, "../.."))


class SettingService:
    def get_config(self, name: str):
        return DBSession.query(ConfigEntity).filter_by(name=name).first()

    def upload_limit(self):
        limit = 0
        with open(NGINX_CONFIG_FILE) as file:
            for line in file:
                line = line.strip().lower()
                if line.startswith("client_max_body_size"):
                    limit = line.split(" ")[1]
                    if limit.endswith(";"):
                        limit = limit[0:-1]
                    if limit.endswith("k"):
                        limit = int(limit[0:-1]) * 1024
                    if limit.endswith("m"):
                        limit = int(limit[0:-1]) * 1024 * 1024

        return {"limit": limit}

    def system_info(self):
        return convert_keys_to_camel_case(
            {
                "termsOfService": self.get_config(TERMS_OF_SERVICE),
                "manual": self.get_config(MANUAL),
                "esp": self.get_config(EMAIL_SUBJECT_PREFIX),
                "enableDonate": self.get_config(ENABLE_DONATE),
            }
        )

    def foyer_info(self):
        return convert_keys_to_camel_case(
            {
                "title": self.get_config(FOYER_TITLE),
                "description": self.get_config(FOYER_DESCRIPTION),
                "menu": self.get_config(FOYER_MENU),
                "showRegistration": self.get_config(SHOW_REGISTRATION),
            }
        )

    def update_terms_of_service(self, url: str):
        with ScopedSession() as local_db_session:
            config = self.get_config(TERMS_OF_SERVICE)
            if not config:
                config = ConfigEntity(name=TERMS_OF_SERVICE, value=url)
                local_db_session.add(config)
            else:
                config.value = url
            local_db_session.commit()
            local_db_session.flush()
            return convert_keys_to_camel_case(config)

    def save_config(self, input: ConfigInput):
        with ScopedSession() as local_db_session:
            config = self.get_config(input.name)
            if not config:
                config = ConfigEntity(name=input.name, value=input.value)
                local_db_session.add(config)
            else:
                config.value = input.value
            local_db_session.commit()
            local_db_session.flush()
            return convert_keys_to_camel_case(config)

    async def send_email(self, input: EmailInput):
        await send(
            input.recipients.split(","),
            input.subject,
            input.body,
            input.bcc.split(",") if input.bcc else [],
        )
        return {"success": True}

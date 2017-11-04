from settings import config


class FacebookWebHook(object):
    HUB_MODE = config.HUB_MODE
    VERIFY_TOKEN = config.VERIFY_TOKEN

    def __init__(self, hub_mode, hub_verify_token, hub_challenge):
        self.hub_mode = hub_mode
        self.hub_verify_token = hub_verify_token
        self.hub_challenge = hub_challenge

    def response(self):
        if self.hub_mode == self.HUB_MODE and (self.hub_challenge is not None):
            if not self.hub_verify_token == self.VERIFY_TOKEN:
                return "Verification token mismatch", 403
            return self.hub_challenge, 200
        return """
        SIGMA BOT your financial assistant.
        """
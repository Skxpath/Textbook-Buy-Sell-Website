# Used for generating an account activation token used to confirm that a user's email address is valid
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()

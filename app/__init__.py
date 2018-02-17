from django.contrib.auth.models import User


def get_name(self):
    return '{} - {}'.format(self.first_name,self.email)

User.add_to_class("__str__", get_name)
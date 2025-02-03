from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    """
    Todo Model to store tasks for users.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todostasks"
    )
    name = models.CharField(_("Name Of Task"), max_length=1000)
    done = models.BooleanField(_("Completed"), default=False)
    date_created = models.DateTimeField(
        _("Date Of Task Created"), default=now, null=True)
    date_completed = models.DateTimeField(_("Date Of Completion"), null=True)

    def save(self, *args, **kwargs):
        if len(self.name) == 0:
            return ValueError("Task Name Not Specified")
        if self.done and not self.date_completed:
            self.date_completed = now()
        elif not self.done:
            self.date_completed = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {'Completed' if self.done else 'Pending'}"

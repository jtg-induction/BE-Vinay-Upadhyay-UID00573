
from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint
class Project(models.Model):
    """
        Needed fields
        - members (m2m field to CustomUser; create through table and enforce unique constraint for user and project)
        - name (max_length=100)
        - max_members (positive int)
        - status (choice field integer type :- 0(To be started)/1(In progress)/2(Completed), with default value been 0)

        Add string representation for this model with project name.
    """
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectMember",
        related_name="allprojects"
    )

    STATUS_CHOICES = (
        (0, "To be started"),
        (1, "In progress"),
        (2, "Completed"),
    )

    name = models.CharField(max_length=100)
    max_members = models.PositiveIntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

   
    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """
    Needed fields
    - project (fk to Project model)
    - member (fk to User model - use AUTH_USER_MODEL from settings)
    - Add unique constraints

    Add string representation for this model with project name and user email/first name.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="membersofproject")
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projectsofmembers")

    class Meta:
        constraints = [
            UniqueConstraint (fields = ['project','member'],name='uniqueconstraints')
        ]

    def __str__(self):
        return f"{self.project.name} - {self.member.email if self.member.email else self.member.first_name}"




from django.db import models
from django.contrib.auth.models import User
from core import models as coreModels


class Pyme(coreModels.BaseModel):
    name = models.CharField(max_length=70, blank=False)
    code = models.CharField(max_length=70, blank=False, db_index=True)

    class Meta:
        verbose_name = "Pyme"
        verbose_name_plural = "Pymes"

    def _get_new_code(self):
        return self.name.lower().replace(' ', '_')

    def save(self, *args, **kwargs):
        new_code = self._get_new_code()
        if self.code != new_code:
            self.code = new_code
        return super(Pyme, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


# class PymeRole(models.Model):
#     name = models.CharField(max_length=70, blank=False, db_index=True)
#     pyme = models.ForeignKey(
#         Pyme,
#         related_name="roles",
#         on_delete=models.CASCADE)


class PymeUser(coreModels.BaseModel):
    pyme = models.ForeignKey(
        Pyme,
        related_name="users",
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        related_name="pyme_users",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Pyme User"
        verbose_name_plural = "Pyme Users"
        unique_together = ("pyme", "user")

    def __str__(self):
        return f"{self.user.email} ({self.pyme.name})"


# class PymeUserRole(models.Model):
#     user = models.ForeignKey(
#         PymeUser,
#         related_name="roles",
#         on_delete=models.CASCADE)

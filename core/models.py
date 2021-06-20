from django.db import models
from django.utils import timezone


class BaseModelManager(models.Manager):
    def active(self):
        return self.exclude(deleted_date__isnull=False)

    def inactive(self):
        return self.filter(deleted_date__isnull=False)


class BaseModel(models.Model):
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    deleted_date = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if (not self.id):
            self.created_date = timezone.now()

        self.updated_date = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def delete(self):
        self.deleted_date = timezone.now()
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()

    @property
    def is_deleted(self):
        return self.deleted_date is not None

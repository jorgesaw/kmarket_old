from django.db import models

class StatusCreatedUpdatedModelMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        abstract = True

    def soft_delete(self):
        self.active = False
        self.save()

    def delete(self, *args, **kwargs):
        self.soft_delete()
        super(StatusCreatedUpdatedModelMixin, self).delete(*args, **kwargs)
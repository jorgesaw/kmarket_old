import os
import sys

from django.db import models
from django.core.management import call_command
from django.db import transaction
from django.conf import settings
from django.db.models.signals import post_init
from django.dispatch import receiver

from sales.models import Sale
from overheads.models import Overhead

# Create your models here.
MSG_RESTORE_DATA_DONE = "Datos restaurados con éxito."
MSG_RESTORE_DATA_ERROR = "Error al intentar cargar los datos. Imposible cargarlos."

class ProviderBck(object):
    PRE_NAME = '_DB_'
    POS_NAME = '_BCK'
    FORMAT_FILE = 'json'

    def __init__(self, filename):
        self.file = self._make_path_bck(filename)
    
    def _make_path_bck(self, filename):
        filename_full = '{}{}{}.{}'.format(ProviderBck.PRE_NAME, filename, 
                            ProviderBck.POS_NAME, ProviderBck.FORMAT_FILE)

        return os.path.join(settings.PATH_BCK, filename_full)

class SQLiteProviderBck(ProviderBck):
    
    def create_bck(self):
        is_operation_done = False
        sysout = sys.stdout
        try:
            sys.stdout = open(self.file, 'w')
            call_command('dumpdata', 
                        '--exclude', 'auth.permission', 
                        '--exclude', 'admin.LogEntry', 
                        '--exclude', 'contenttypes',
                        '--exclude', 'sessions',
                        '--exclude', 'backups',  
                        '--indent', '4')
            is_operation_done = True
        except IOError:
            pass
        except:
            pass
        finally:
            sys.stdout.close()

        sys.stdout = sysout
        return is_operation_done

    def restore_bck(self):
        is_operation_done = False
        try:
            call_command('loaddata', self.file)
            is_operation_done = True
        except IOError:
            pass
        except:
            pass
        finally:
            pass
        return is_operation_done

class ProviderMariaDbBck(ProviderBck):
    pass        

class BackUp(models.Model):
    """Model representing a many to many relationship of backup."""

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    desc = models.CharField(max_length=255, verbose_name="Descripción")

    provider_bck = None

    class Meta:
        ordering = ['id',]
        verbose_name = "backup"
        verbose_name_plural = "backups"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(BackUp, self).save(*args, **kwargs)

        #self.provider_bck = SQLiteProviderBck(filename=str(self.created))
        if not self.provider_bck.create_bck():
            return

        month = self.created.month
        year = self.created.year
        if month <=1: # Si es el primer mes del año tenemos que tomar la fecha del año anterior
            month = 12 
            year -= 1

        Sale.objects.filter(date_sale__year__lte=year, 
                                    date_sale__month__lt=month).delete()
        Overhead.objects.filter(date_overhead__year__lte=year, 
                                    date_overhead__month__lt=month).delete()

    def __str__(self):
        return str(self.created)

@receiver(post_init, sender=BackUp)
def update_provider_bck(sender, instance, **kwargs):
    instance.provider_bck = SQLiteProviderBck(filename=str(instance.created))
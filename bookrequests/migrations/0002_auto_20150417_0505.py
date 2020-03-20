# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookrequests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrequest',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'request pending'), (1, b'request accepted'), (2, b'request rejected'), (3, b'being delivered to borrower'), (4, b'with borrower'), (5, b'done reading'), (6, b'being delivered to owner'), (7, b'returned')]),
            preserve_default=True,
        ),
    ]

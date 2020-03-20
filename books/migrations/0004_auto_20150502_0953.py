# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]

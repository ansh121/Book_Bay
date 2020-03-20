# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bookrequests', '0002_auto_20150417_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrequest',
            name='book',
            field=models.ForeignKey(to='books.Book'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bookrequest',
            name='borrower',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

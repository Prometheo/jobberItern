# Generated by Django 3.0.2 on 2020-02-10 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('websocket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='connection_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='websocket.ConnectionModel'),
            preserve_default=False,
        ),
    ]

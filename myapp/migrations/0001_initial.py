# Generated by Django 3.2.19 on 2023-08-22 20:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=320)),
                ('json', models.TextField(null=True)),
            ],
        ),
    ]
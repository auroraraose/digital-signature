# Generated by Django 5.1.6 on 2025-02-19 11:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_pdf', models.FileField(upload_to='documents/original_pdfs/')),
                ('signed_pdf', models.FileField(blank=True, null=True, upload_to='documents/signed_pdfs/')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('signed_at', models.DateTimeField(blank=True, null=True)),
                ('signature_status', models.CharField(choices=[('pending', 'Pending'), ('signed', 'Signed')], default='pending', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

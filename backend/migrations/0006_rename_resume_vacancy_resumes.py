# Generated by Django 4.0.5 on 2022-06-28 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_contact_candidate_contacts_contact_candidate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacancy',
            old_name='resume',
            new_name='resumes',
        ),
    ]

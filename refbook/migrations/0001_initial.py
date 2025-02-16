# Generated by Django 5.1.6 on 2025-02-12 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceBook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='код справочника')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.CreateModel(
            name='ReferenceBookVersion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('version', models.CharField(max_length=50)),
                ('start_date', models.DateField(help_text='Дата начала действия версии', verbose_name='Дата начала действия версии')),
                ('reference_book', models.ForeignKey(help_text='Справочник, к которому относится версия', on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='refbook.referencebook', verbose_name='Идентификатор справочника')),
            ],
            options={
                'verbose_name': 'Версия справочника',
                'verbose_name_plural': 'Версии справочников',
            },
        ),
        migrations.CreateModel(
            name='ReferenceBookElement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('code', models.CharField(help_text='Код элемента справочника (макс. 100 символов)', max_length=100, verbose_name='Код элемента')),
                ('value', models.CharField(help_text='Значение элемента справочника (макс. 300 символов)', max_length=300, verbose_name='Значение элемента')),
                ('version', models.ForeignKey(help_text='Версия справочника, к которой относится элемент', on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='refbook.referencebookversion', verbose_name='Идентификатор версии справочника')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
            },
        ),
        migrations.AddConstraint(
            model_name='referencebookversion',
            constraint=models.UniqueConstraint(fields=('reference_book', 'version'), name='unique_reference_book_version'),
        ),
        migrations.AddConstraint(
            model_name='referencebookversion',
            constraint=models.UniqueConstraint(fields=('reference_book', 'start_date'), name='unique_reference_book_start_date'),
        ),
        migrations.AddConstraint(
            model_name='referencebookelement',
            constraint=models.UniqueConstraint(fields=('version', 'code'), name='unique_version_element_code'),
        ),
    ]

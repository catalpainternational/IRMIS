# Generated by Django 2.2.4 on 2020-03-11 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0024_add_tender_to_contract'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractMilestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_of_work', models.IntegerField()),
                ('progress', models.IntegerField(verbose_name='Physical progress')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Contract')),
            ],
        ),
    ]

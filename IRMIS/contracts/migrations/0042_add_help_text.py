# Generated by Django 2.2.4 on 2020-03-31 07:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0041_update_contract_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='TIN',
            field=models.IntegerField(blank=True, help_text='Enter company TIN number', null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.TextField(blank=True, help_text='Enter company address', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, help_text='Enter company email', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='iban',
            field=models.CharField(blank=True, help_text='Enter company bank account number', max_length=256, null=True, verbose_name='Bank Account Number'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(help_text='Enter company name', max_length=256, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, help_text='Enter company phone number', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='rep_email',
            field=models.EmailField(blank=True, help_text='Enter company representative email', max_length=254, null=True, verbose_name='Representative email'),
        ),
        migrations.AlterField(
            model_name='company',
            name='rep_name',
            field=models.CharField(blank=True, help_text='Enter company representative name', max_length=256, null=True, verbose_name='Representative name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='rep_phone',
            field=models.CharField(blank=True, help_text='Enter company representative phone number', max_length=256, null=True, verbose_name='Representative phone'),
        ),
        migrations.AlterField(
            model_name='company',
            name='woman_led',
            field=models.NullBooleanField(choices=[(None, 'Unknown'), (True, 'Yes'), (False, 'No')], help_text='Is the company director/owner a woman?', verbose_name='Woman-Led Company'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='amendment_description',
            field=models.TextField(blank=True, help_text='Enter a reason for variations to the contract', null=True, verbose_name='Description (Reasons for Variations)'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='amendment_duration',
            field=models.IntegerField(blank=True, help_text='Enter new duration in days', null=True, verbose_name='Contract duration'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='amendment_start_date',
            field=models.DateField(blank=True, help_text='Enter new start date', null=True, verbose_name='Contract start date'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contract_code',
            field=models.SlugField(help_text='Enter contract code'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contractor',
            field=models.ForeignKey(blank=True, help_text='Select a company from the list', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='contractor_for', to='contracts.Company'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='defect_liability_days',
            field=models.IntegerField(blank=True, help_text='Duration of DLP in days', null=True, verbose_name='Defect liability period (days)'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='description',
            field=models.TextField(blank=True, help_text='Enter a description of the contract', null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='duration',
            field=models.IntegerField(blank=True, help_text='Duration in days', null=True, verbose_name='Duration (days)'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(blank=True, help_text='Enter contract end date', null=True, verbose_name='Contract end date'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateField(blank=True, help_text='Enter contract start date', null=True, verbose_name='Contract start date'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.ForeignKey(blank=True, default=1, help_text='Choose status', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contracts.ContractStatus'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='subcontractor',
            field=models.ForeignKey(blank=True, help_text='Select a company from the list', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sub_contractor_for', to='contracts.Company'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='tender',
            field=models.ForeignKey(blank=True, help_text='Choose a tender to create a contract', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contracts.Tender', verbose_name='Associated tender'),
        ),
        migrations.AlterField(
            model_name='contractamendment',
            name='value',
            field=models.DecimalField(decimal_places=4, help_text='Budget per year in USD', max_digits=14),
        ),
        migrations.AlterField(
            model_name='contractamendment',
            name='year',
            field=models.IntegerField(blank=True, choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], help_text='Select year', null=True),
        ),
        migrations.AlterField(
            model_name='contractbudget',
            name='value',
            field=models.DecimalField(decimal_places=4, help_text='Budget per year in USD', max_digits=14),
        ),
        migrations.AlterField(
            model_name='contractbudget',
            name='year',
            field=models.IntegerField(blank=True, choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020)], help_text='Select year', null=True),
        ),
        migrations.AlterField(
            model_name='contractmilestone',
            name='days_of_work',
            field=models.IntegerField(help_text='Days of work for the milestone'),
        ),
        migrations.AlterField(
            model_name='contractmilestone',
            name='progress',
            field=models.IntegerField(help_text='Milestone physical progress', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Physical progress (%)'),
        ),
        migrations.AlterField(
            model_name='contractsupervisor',
            name='name',
            field=models.CharField(help_text="Enter supervisor's name", max_length=40),
        ),
        migrations.AlterField(
            model_name='contractsupervisor',
            name='phone',
            field=models.CharField(help_text="Supervisor's phone number", max_length=40),
        ),
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.SlugField(help_text='Enter project’s code', max_length=128, unique=True, verbose_name='Project Code'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(help_text='Enter a description of the project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='donor',
            field=models.ForeignKey(blank=True, help_text='Choose the donor', null=True, on_delete=django.db.models.deletion.PROTECT, to='contracts.ProjectDonor'),
        ),
        migrations.AlterField(
            model_name='project',
            name='duration',
            field=models.IntegerField(blank=True, help_text='Estimated duration of the work', null=True, verbose_name='Duration (days)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='funding_source',
            field=models.ForeignKey(blank=True, help_text='Choose the funding source', null=True, on_delete=django.db.models.deletion.PROTECT, to='contracts.FundingSource'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(help_text='Enter project’s name', max_length=128, verbose_name='Project Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='program',
            field=models.ForeignKey(help_text='Choose the program for the project', on_delete=django.db.models.deletion.PROTECT, to='contracts.Program', verbose_name='Program Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(blank=True, help_text='????????', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.ForeignKey(default=1, help_text='Choose status', on_delete=django.db.models.deletion.PROTECT, to='contracts.ProjectStatus', verbose_name='Project Status'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='contracts.Tender'),
        ),
        migrations.AlterField(
            model_name='project',
            name='type_of_work',
            field=models.ForeignKey(help_text='Choose from the list', on_delete=django.db.models.deletion.PROTECT, to='contracts.TypeOfWork', verbose_name='Type of Work'),
        ),
        migrations.AlterField(
            model_name='projectasset',
            name='asset_code',
            field=models.CharField(help_text='Select project’s asset', max_length=128, verbose_name='Asset'),
        ),
        migrations.AlterField(
            model_name='projectasset',
            name='asset_end_chainage',
            field=models.IntegerField(blank=True, help_text='In meters', null=True, verbose_name='End Chainage'),
        ),
        migrations.AlterField(
            model_name='projectasset',
            name='asset_start_chainage',
            field=models.IntegerField(blank=True, help_text='In meters', null=True, verbose_name='Start Chainage'),
        ),
        migrations.AlterField(
            model_name='projectbudget',
            name='approved_value',
            field=models.DecimalField(blank=True, decimal_places=4, help_text='In USD', max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='projectbudget',
            name='year',
            field=models.IntegerField(blank=True, choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030)], help_text='Enter year', null=True),
        ),
        migrations.AlterField(
            model_name='projectmilestone',
            name='days_of_work',
            field=models.IntegerField(help_text='Estimated days of work'),
        ),
        migrations.AlterField(
            model_name='projectmilestone',
            name='progress',
            field=models.IntegerField(default=0, help_text='Estimated physical progress', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Physical progress (%)'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='announcement_date',
            field=models.DateField(blank=True, help_text='Tender announcement date', null=True, verbose_name='Announcement Date'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='code',
            field=models.SlugField(help_text='Enter tender code', primary_key=True, serialize=False, verbose_name='Tender Code'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='evaluation_date',
            field=models.DateField(blank=True, help_text='Bids evaluation date', null=True, verbose_name='Evaluation Date'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='status',
            field=models.ForeignKey(default=1, help_text='Choose status', on_delete=django.db.models.deletion.PROTECT, to='contracts.TenderStatus', verbose_name='Tender Status'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='submission_date',
            field=models.DateField(blank=True, help_text='Date of fid submission deadline', null=True, verbose_name='Bid Submission Deadline'),
        ),
        migrations.AlterField(
            model_name='tender',
            name='tendering_companies',
            field=models.IntegerField(blank=True, help_text='Enter the number of companies tendering', null=True, verbose_name='Number of Companies Tendering'),
        ),
    ]

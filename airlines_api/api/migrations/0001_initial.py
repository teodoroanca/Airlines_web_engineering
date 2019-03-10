# Generated by Django 2.1.7 on 2019-03-10 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Airport')),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Carrier')),
            ],
        ),
        migrations.CreateModel(
            name='Flights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancelled', models.IntegerField()),
                ('delayed', models.IntegerField()),
                ('diverted', models.IntegerField()),
                ('on_time', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MinutesDelayed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrier', models.IntegerField()),
                ('late_aircraft', models.IntegerField()),
                ('national_aviation_system', models.IntegerField()),
                ('security', models.IntegerField()),
                ('total', models.IntegerField()),
                ('weather', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NumberOfDelays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrier', models.IntegerField()),
                ('late_aircraft', models.IntegerField()),
                ('national_aviation_system', models.IntegerField()),
                ('security', models.IntegerField()),
                ('weather', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flights', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Flights')),
                ('minutes_delayed', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.MinutesDelayed')),
                ('number_of_delays', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.NumberOfDelays')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('label', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='statistics',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Statistics'),
        ),
        migrations.AddField(
            model_name='entry',
            name='time',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Time'),
        ),
    ]

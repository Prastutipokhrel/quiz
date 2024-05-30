# Generated by Django 5.0.6 on 2024-05-30 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0008_alter_question_correct_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquationQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter1', models.IntegerField()),
                ('parameter2', models.IntegerField()),
                ('parameter3', models.IntegerField()),
                ('correct_answer', models.FloatField()),
                ('question_text', models.CharField(max_length=500)),
            ],
        ),
    ]

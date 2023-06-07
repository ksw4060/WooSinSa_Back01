# Generated by Django 4.2.1 on 2023-06-07 10:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='이메일')),
                ('account', models.CharField(max_length=50, unique=True, verbose_name='계정이름')),
                ('age', models.PositiveIntegerField(null=True, verbose_name='나이')),
                ('username', models.CharField(max_length=50, verbose_name='유저이름')),
                ('gender', models.CharField(choices=[('Men', 'Men'), ('Women', 'Women')], max_length=10, verbose_name='성별')),
                ('introduction', models.TextField(blank=True, null=True, verbose_name='자기소개')),
                ('profile_img', models.ImageField(blank=True, upload_to='users/%Y%m%d', verbose_name='프로필 이미지')),
                ('joined_at', models.DateField(auto_now_add=True, verbose_name='계정 생성일')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화 여부')),
                ('is_admin', models.BooleanField(default=False, verbose_name='관리자 여부')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]

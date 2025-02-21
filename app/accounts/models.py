from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


class Account(User):
    slug = models.SlugField(unique=True, verbose_name='Slug')
    avatar = models.ImageField(
        upload_to='images/avatars/default.png',
        verbose_name='Avatar',
    )
    bio = models.TextField(verbose_name='Bio', blank=True, null=True)
    birth_date = models.DateField(
        verbose_name='Birth Day',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('account:profile', args=(self.slug,))

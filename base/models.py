from django.db import models
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    text = models.CharField(max_length=500)
    accepted = models.BooleanField(default=False)
    web_url = models.CharField(max_length=100, blank=True)
    linkedin_url = models.CharField(max_length=100, blank=True)
    github_url = models.CharField(max_length=100, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='responses', null=True, blank=True)

    def __str__(self):
        username = "Anonymous" if self.user is None else self.user.username
        return f"{username}: {self.text}"


class TechnicalSkillCategory(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TechnicalSkill(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='tech_skill_logos/', null=True, blank=True)
    category = models.ForeignKey(
        TechnicalSkillCategory,
        on_delete=models.CASCADE,
        related_name='skills',
        null=True,
        blank=True
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        MAX_IMAGE_SIZE = 200

        if self.pk:
            try:
                old_logo = TechnicalSkill.objects.get(pk=self.pk).logo
                if old_logo.name and old_logo.name != self.logo.name and old_logo.name != 'default.jpg':
                    old_logo.delete(save=False)
            except TechnicalSkill.DoesNotExist:
                pass

        if self.logo and hasattr(self.logo, 'file'):
            img = Image.open(self.logo)
            if img.height > MAX_IMAGE_SIZE or img.width > MAX_IMAGE_SIZE:
                img.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.Resampling.LANCZOS)

                thumb_io = BytesIO()
                img.save(thumb_io, format=img.format, quality=85)
                in_memory_file = InMemoryUploadedFile(thumb_io, None, self.logo.name, 'image/jpeg', thumb_io.tell(), None)
                self.logo.save(self.logo.name, in_memory_file, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    company = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    current_work = models.BooleanField(default=False)
    position = models.CharField(max_length=100)
    job_tasks = models.JSONField()
    skills = models.ManyToManyField(TechnicalSkill, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position} at {self.company}"


class Study(models.Model):
    center = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    tittle = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    skills = models.ManyToManyField(TechnicalSkill, blank=True)

    def __str__(self):
        return f"{self.tittle} at {self.center}"

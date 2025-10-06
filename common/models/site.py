from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=56)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    is_menu = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}  |  {self.slug}  |  {self.is_menu}"

    class Meta:
        verbose_name = '1. Toifa'
        verbose_name_plural = '1. Toifalar'


class New(models.Model):
    title = models.CharField(max_length=256)
    short_desc = models.TextField()
    description = models.TextField()
    image1 = models.ImageField(upload_to='news/')
    image2 = models.ImageField(upload_to='news/', null=True, blank=True)
    ctg = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100)
    create = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, editable=False)

    def get_desc(self):
        return self.description.split("\n")

    def save(self, *args, **kwargs):
        if "#" not in self.tags:
            self.tags = "#" + "#".join(self.tags.lower().strip().split())

        return super(New, self).save(*args, **kwargs)

    def get_tags(self):
        return self.tags.strip('#').replace(" ", "").split("#")

    def get_date(self):
        import datetime
        now = datetime.datetime.now()
        calc = int((now - self.create).total_seconds() // 60)
        if calc == 0:
            return "Hozirgina!"

        if 0 < calc < 60:
            return f"{calc} minut oldin"

        if 60 <= calc < 60 * 24:
            return f"{int(calc // 60)} soat oldin!"

        return self.create.strftime("%H:%M / %d-%B %Y")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '2. Yangi'
        verbose_name_plural = '2. Yangiliklar'


class Contact(models.Model):
    ism = models.CharField(max_length=56)
    phone = models.CharField(max_length=56)
    xabar = models.TextField()
    is_trash = models.BooleanField(default=False)

    def __str__(self):
        return self.xabar

    class Meta:
        verbose_name = '5. Aloqa'
        verbose_name_plural = '5. Aloqalar'


class Subscribe(models.Model):
    email = models.EmailField()
    is_trash = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '4. Obuna'
        verbose_name_plural = '4. Obunalar'


class Comment(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name='comments')
    user = models.CharField(max_length=50)
    message = models.TextField()
    post = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', models.SET_NULL, null=True, blank=True, related_name='subs')
    is_sub = models.BooleanField(default=False)

    def get_date(self):
        import datetime
        now = datetime.datetime.now()
        calc = int((now - self.post).total_seconds() // 60)
        if calc == 0:
            return "Hozirgina!"

        if 0 < calc < 60:
            return f"{calc} minut oldin"

        if 60 <= calc < 60 * 24:
            return f"{int(calc // 60)} soat oldin!"

        return self.post.strftime("%H:%M / %d-%B %Y")

    def __str__(self):
        return f"{self.user} -> {self.message}"

    class Meta:
        verbose_name = '3. Izoh'
        verbose_name_plural = '3. Izohlar'

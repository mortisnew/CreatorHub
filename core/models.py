
from django.db import models
from accounts.models import CreatorUser

class Tag(models.Model):
    name = models.CharField(max_length=100,unique=True)

class MemberStatus(models.TextChoices):
    MEMBER = 'member', 'Member'
    MANAGER = 'manager', 'Manager'
    ADMIN = 'admin', 'Admin'


class Community(models.Model):
    owner = models.ForeignKey(CreatorUser, on_delete=models.CASCADE,
                              related_name='owned_communities')
    name = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.ManyToManyField('Tag', related_name='communities_tag')
    active = models.BooleanField(default=True)
    required_post_approval = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(CreatorUser, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE,related_name='memberships')
    role = models.CharField(choices=MemberStatus.choices,
                                  default=MemberStatus.MEMBER,max_length=10)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['community', 'user'],
                name='unique_membership',
            )
        ]


class CreatePost(models.Model):
    user = models.ForeignKey(CreatorUser, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    file = models.FileField(upload_to='posts/',blank=True)

    is_allowed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(CreatorUser, on_delete=models.CASCADE)
    post = models.ForeignKey(CreatePost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               blank=True, null=True,related_name='replies')
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[0:15]

class ReportStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    REVIEWED = 'reviewed', 'Reviewed'
    DISMISSED = 'dismissed', 'Dismissed'

class ReportPost(models.Model):
    user = models.ForeignKey(CreatorUser, on_delete=models.CASCADE)
    post = models.ForeignKey(CreatePost, on_delete=models.CASCADE)
    problem = models.TextField()
    image = models.ImageField(upload_to='reports/',blank=True)
    rep_status = models.CharField(max_length=10,
                                  choices=ReportStatus.choices,
                                  default=ReportStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.problem[0:15]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_report_post',
            )
        ]

class ReportComment(models.Model):
    user = models.ForeignKey(CreatorUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    problem = models.TextField()
    image = models.ImageField(upload_to='reports/',blank=True)
    rep_status = models.CharField(max_length=10,
                                  choices=ReportStatus.choices,
                                  default=ReportStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_report_comment',
            )
        ]

    def __str__(self):
        return self.problem[0:15]

class Like(models.Model):
    user = models.ForeignKey(CreatorUser, on_delete=models.CASCADE)
    post = models.ForeignKey(CreatePost, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_like',
            )
        ]



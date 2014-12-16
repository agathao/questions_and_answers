from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings

TEXT_LENGTH = 10000
TITLE_LENGTH = 500

class Question(models.Model):
    question_text = models.CharField(max_length=TEXT_LENGTH)
    question_title = models.CharField(max_length=TITLE_LENGTH)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now_add=True) 
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    votes = models.IntegerField(default=0)
    tags_list = models.CharField(max_length=TEXT_LENGTH, default="")
        
    def __unicode__(self):              # __unicode__ on Python 2
        return self.question_text + " - " + unicode(self.creator)

    def num_replies(self):
        return self.post_set.count() - 1
    num_replies.short_description = 'Number of answers'
    
    def get_sorted_answers(self):
        return self.answer_set.order_by('-votes')
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=TEXT_LENGTH)
    answer_title = models.CharField(max_length=TITLE_LENGTH)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    votes = models.IntegerField(default=0)
     
    def __unicode__(self):              # __unicode__ on Python 2
        return self.answer_text

        
class Tags(models.Model):
    question = models.ForeignKey(Question)
    tag_text = models.CharField(max_length=10000)
     
    def __unicode__(self):              # __unicode__ on Python 2
        return self.tag_text

        
class UploadedImage(models.Model):
    imagefile=models.ImageField(upload_to='documents/%Y/%m/%d') #"user_images/uploaded_images")
    owner=models.ForeignKey(settings.AUTH_USER_MODEL)
    
class QuestionVotesRegistry(models.Model):
    question = models.ForeignKey(Question)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    vote = models.IntegerField()
    
class AnswerVotesRegistry(models.Model):
    answer = models.ForeignKey(Answer)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    vote = models.IntegerField()
    
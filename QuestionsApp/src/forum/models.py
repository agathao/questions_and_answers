from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings


class Question(models.Model):
    question_text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now_add=True) 
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    votes = models.IntegerField(default=0)
    tags_list = models.CharField(max_length=10000, default="")
        
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
    answer_text = models.CharField(max_length=10000)
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

        

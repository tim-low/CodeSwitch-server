from django.db import models
from skills.models import Skill

# Create your models here.

class Course(models.Model):
    """Course entity. Data pulled from SkillsFuture API.

    Fields pulled from SkillsFuture API:
        title
        trainingProviderAlias
        content
        objective
        totalCostOfTrainingPerTrainee
        totalTrainingDurationHour
        meta['createDate']
        modeOfTrainings[0]['description']
        referenceNumber
        displayImageName
    
    Attributes:
        id              -- (auto-generated)
        title           -- title
        organizer       -- trainingProviderAlias
        price           -- totalCostOfTrainingPerTrainee
        course_src      -- referenceNumber
            https://www.myskillsfuture.sg/content/portal/en/training-exchange/course-directory/course-detail.html?courseReferenceNumber={referenceNumber}
        picture_src     -- displayImageName
            https://www.myskillsfuture.sg/content/dam/portal/tex/aot/thumbnails/{displayImageName}.jpg 
        description     -- content
        objective       -- objective
        create_date     -- meta['createDate']
        training_type   -- modeOfTrainings[0]['description']
    """

    # Cannot be blank
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    course_src = models.URLField(max_length=200)
    picture_src = models.URLField(blank=True, null=True, max_length=200)

    # Can be blank
    description = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    create_date = models.DateField(blank=True, default=None)
    training_type = models.CharField(max_length=100, blank=True)

    skills_taught = models.ManyToManyField(Skill)
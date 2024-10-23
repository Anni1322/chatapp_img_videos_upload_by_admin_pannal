from django.db import models

class ChatModel(models.Model):
    user_message = models.TextField(verbose_name="User Message")
    answers = models.TextField(verbose_name="Answers")
    # image_path = models.URLField(blank=True, null=True, verbose_name="Image Path")  # Using URLField
    image_path = models.ImageField(upload_to="Images/images",max_length=200,null=True,blank=True)
    video_path = models.FileField(upload_to="Videos/videos", max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.user_message} -> {self.answers}"

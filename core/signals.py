# from datetime import date
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .models import User
 
# @receiver(post_save, sender=User)
# def update_user(sender, instance, created, **kwargs):
#     user = instance
#     now = date.today()
                            
#     if created:
#         user.day = now.day
#         if now.month == 1:
#            month = "January"
#         elif now.month == 2: 
#            month = "February"
#         elif now.month == 3: 
#            month = "March"
#         elif now.month == 4: 
#            month = "April"   
#         elif now.month == 5: 
#            month = "May"
#         elif now.month == 6: 
#            month = "June" 
#         elif now.month == 7: 
#            month = "July"
#         elif now.month == 8:
#            month = "August"   
#         elif now.month == 9:
#            month = "September" 
#         elif now.month == 10: 
#            month = "October"
#         elif now.month == 11: 
#            month = "November" 
#         else:
#            month = "December"
#         user.month = month
#         user.year = now.year
#         user.created = date(day=now.day, month=now.month, year=now.year)
#         user.save()

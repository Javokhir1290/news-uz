from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
import requests
from django.core.mail import send_mail
from django.conf import settings



@receiver(post_save, sender=New)
def news_signal(sender, instance, created, **kwargs):

    if created:
        messages = f"Saytda Yangi Xabar\n" \
                   f"Title :{instance.title}\n" \
                   f"Qisqacha :{instance.short_desc}\n" \
                   f"Sana :{instance.create.strftime('%D')}\n"

        email_royxat = [
            "ergashevazamera8@gmail.com",
            "maxmudbobomurodov151@gmail.com"
            #email kiritiladi
        ]
        send_mail(
            subject="News saytiga yangi xabar qushildi",
            message=messages,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_royxat,
        )
        print("\n\n" "Barchaning emailiga Xabar yuborib bo'lindi !" "\n\n")

        tg_id = [
            6909856076,
            6717501063,
            6063204874,
            5894214924
        ]
        import requests

        for i in tg_id:
            url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage"
            payload = {
                "chat_id": i,
                "text": messages
            }
            r = requests.post(url, data=payload)

        print("\n", "Telegramga ham Xabar yuborildi", "\n\n")

        message = "Telegram Botdan hammaga habar yuborildi"
        url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={6717501063}&text={message}"
        requests.get(url)



# @receiver(post_save, )
# def create_signal(sender, instance=None, created=None, *args, **kwargs):
#     print("\nBu Universal signal", sender)
#     print("\nObjects", instance)
#     print("\nYaraldimi", created)
#     print("\n", args, kwargs, "\n\n")
#
#
# @receiver(post_delete, sender=None)
# def delete_signal(sender, instance=None, *args, **kwargs):
#     print("\nYangi Signal\nYuboruvchi", sender)
#     print("\nObjects", instance)
#     print("\n", args, kwargs, "\n\n")


@receiver(post_save, sender=Comment)
def comment_signal(sender, instance, created, **kwargs):
    if created:
        messagee = f"Saytda Yangi Izoh qo'shildi\n" \
                  f"Yangilik : <b>{instance.new.title}</b>\n" \
                  f"User : <b>{instance.user}</b>\n" \
                  f"Message : <b>{instance.message}</b>\n" \
                  f"Sana : <b>{instance.post.strftime('%H:%M / %d-%B %Y')}</b>"
        url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={6717501063}&text={messagee}&parse_mode=HTMl"
        requests.get(url)


# @receiver(post_delete, sender=Comment)
# def comment_delete_signal(sender, instance, **kwargs):
#     message = f"Saytdan Comment o'chirildi\n" \
#               f"Comment : {instance.__str__()}\n" \
#
#     url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={6717501063}&text={message}&parse_mode=HTMl"
#     requests.get(url)



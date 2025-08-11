from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from News_paper.settings import DEFAULT_FROM_EMAIL



def new_post(instance):
    template='new_post.html' 
    for cat in instance.category.all():
        email_subject=f'New post in category "{cat}"' 
        us_emails=get_sub(cat) 
        html = render_to_string(template_name=template,context={
        'category':'category',
        'post': 'post'
            },
        )
        msg=EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=us_emails
                                   )
        msg.attach_alternative(html,'text/html')
        msg.send()

def get_sub(category):
    user_email=[]
    for user in category.sub.all():
        user_email.append(user.email)
    return user_email 
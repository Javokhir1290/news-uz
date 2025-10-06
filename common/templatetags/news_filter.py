from django.template import Library
from django.db.models import Q
register = Library()



@register.filter
def nfilter(query_set, atrs, *args, **kwargs):
    atrs = atrs.split('=')
    dec = {
        atrs[0]: atrs[1]
    }
    natija = query_set.filter(**dec)[:int(atrs[2])]

    return natija




@register.filter
def srch_filter(query_set, atrs):
    natija = query_set.filter(Q(title__contains=atrs))
    return natija




@register.filter
def order_filter(query_set, atrs):

    return query_set.order_by(atrs)




@register.filter
def random_filter(queryset, atrs, *args, **kwargs):
        atrs = atrs.split('=')
        dec = {
            atrs[0]: atrs[1]
        }
        natija = query_set.filter(**dec)[:int(atrs[2])]

        return natija

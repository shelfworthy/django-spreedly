# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import list_detail

@login_required
def plan_list(request):
    from subscription.models import Plan, Subscription

    return list_detail.object_list(
        request,
        queryset=Plan.objects.all(),
        template_name='plan_list.html',
        extra_context={'subscription': Subscription.objects.get_for_user(request.user)}
    )
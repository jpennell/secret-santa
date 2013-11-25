import logging
import copy
import random
import itertools

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from annoying.decorators import render_to

from webapp.apps.exchange.forms import ExchangeForm, UserExchangeForm, UserExchangeExclusionForm
from webapp.apps.exchange.models import Exchange, UserExchangeExclusion

logger = logging.getLogger(__name__)

@render_to('exchange/list.html')
@login_required
def exchange_list(request):
    user_exchanges = request.user.userexchange_set.all()
    return {'user_exchanges': user_exchanges}


@render_to('exchange/create.html')
@login_required
def create(request):

    if request.method == 'POST':
        form = ExchangeForm(request.POST)

        if form.is_valid():
            exchange = form.save(user=request.user)
            return redirect('exchange-list')
    else :
        form = ExchangeForm()

    return {'form': form}


@render_to('exchange/edit.html')
@login_required
def edit(request, exchange_id):

    exchange = get_object_or_404(Exchange, pk=exchange_id)

    if request.method == 'POST':
        form = ExchangeForm(request.POST, instance=exchange)

        if form.is_valid():
            exchange = form.save(user=request.user)
            return redirect('exchange-list')
    else :
        form = ExchangeForm(instance=exchange)

    user_exchanges = exchange.userexchange_set.all()
    user_exchange_exclusions = UserExchangeExclusion.objects.filter(exchange=exchange)

    return {
        'form': form,
        'exchange': exchange,
        'user_exchanges': user_exchanges,
        'user_exchange_exclusions': user_exchange_exclusions
    }


@login_required
def start(request, exchange_id):

    exchange = get_object_or_404(Exchange, pk=exchange_id)

    if request.method == 'POST':

        user_exchanges = exchange.userexchange_set.all()
        user_exchange_exclusions = UserExchangeExclusion.objects.filter(exchange=exchange)

        all = copy.deepcopy(list(user_exchanges))
        targets = copy.deepcopy(all)
        random.shuffle(targets)

        target_permutations = itertools.permutations(targets)
        found = False
        i = 0
        for permutation in target_permutations:
            i = i + 1
            if validate(all, permutation, user_exchange_exclusions):
                for person, target in zip(all, permutation):
                    logger.info("%s -> %s" % (person, target));
                    person.target = target.user
                    person.save()

                    subject = exchange.name

                    if exchange.state == Exchange.STARTED:
                        subject = subject + " - Re-generated"

                    if target.user.first_name and target.user.last_name:
                        body = "Get a gift for: %s %s (%s)" % (target.user.first_name, target.user.last_name, target.user.email)
                    else:
                        body = "Get a gift for: %s" % target.user.email

                    email_from = settings.EMAIL_FROM
                    email_to = person.user.email
                    send_mail(subject, body, email_from, [email_to], fail_silently=False)

                found = True
                break

        logger.info("Checked %d permutations" % i)

        if not found:
            raise Exception("Can't start exchange, could not compute cycle")

        exchange.state = Exchange.STARTED
        exchange.save()

        return redirect('exchange-list')

    else :
        return redirect('exchange-list')


def validate(all, targets, user_exchange_exclusions):
    for person, target in zip(all, targets):
        if person == target:
            return False
        for exclusion in user_exchange_exclusions:
            if person == exclusion.user_exchange1 and target == exclusion.user_exchange2:
                return False
    return True


@login_required
def delete(request, exchange_id):

    exchange = get_object_or_404(Exchange, pk=exchange_id)
    exchange.delete()

    return redirect('exchange-list')


@render_to('exchange/user/create.html')
@login_required
def create_user_exchange(request, exchange_id):

    exchange = get_object_or_404(Exchange, pk=exchange_id)

    if request.method == 'POST':
        form = UserExchangeForm(request.POST)

        if form.is_valid():
            user_exchange = form.save(exchange=exchange)
            return redirect('exchange-edit', exchange.id)
    else :
        form = UserExchangeForm()

    return {'form': form, 'exchange': exchange}


@render_to('exchange/user/exclusion/create.html')
@login_required
def create_user_exchange_exclusion(request, exchange_id):

    exchange = get_object_or_404(Exchange, pk=exchange_id)
    user_exchanges = exchange.userexchange_set.all()

    if request.method == 'POST':
        form = UserExchangeExclusionForm(user_exchanges, request.POST)

        if form.is_valid():
            user_exchange_exclusion = form.save(exchange=exchange)
            return redirect('exchange-edit', exchange.id)
    else :
        form = UserExchangeExclusionForm(user_exchanges)

    return {'form': form, 'exchange': exchange}

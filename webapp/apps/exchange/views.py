import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from annoying.decorators import render_to

from webapp.apps.exchange.forms import ExchangeForm, UserExchangeForm
from webapp.apps.exchange.models import Exchange

logger = logging.getLogger(__name__)

@render_to('exchange/list.html')
@login_required
def list(request):
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

    return {'form': form, 'exchange': exchange, 'user_exchanges': user_exchanges}


@login_required
def delete(request, exchange_id):

    exchange = get_object_or_404(Exchange, pk=exchange_id)
    exchange.delete()

    return redirect('exchange-list')


@render_to('exchange/user/create.html')
@login_required
def create_user_exchange(request, exchange_id):

    logger.info('create_user_exchange')

    exchange = get_object_or_404(Exchange, pk=exchange_id)

    if request.method == 'POST':
        form = UserExchangeForm(request.POST)

        if form.is_valid():
            user_exchange = form.save(exchange=exchange)
            return redirect('exchange-edit', exchange.id)
    else :
        form = UserExchangeForm()

    return {'form': form, 'exchange': exchange}

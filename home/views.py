from django.shortcuts import render, redirect

from .models import User, Attainment, Memorandum, SpecialOrder, CommLetter, Moau, MoauParties, MoauSignatories, Event, EventAgencies

from .forms import UserPForm, UserIForm, MoauForm, EventForm, MemoForm, LetterForm, OrderForm

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from datetime import date, timedelta, datetime
from django.utils import timezone
# Create your views here.

def home(request):
    moas = Moau.objects.all()
    events = Event.objects.all()
    memos = Memorandum.objects.all()
    letters = CommLetter.objects.all()
    orders = SpecialOrder.objects.all()

    today = datetime.now()
    datetoday = date.today()
    start_week = datetoday - timedelta(datetoday.weekday())
    end_week = start_week + timedelta(7)

    moa_today = Moau.objects.filter(created_at__year=datetoday.year, created_at__month=datetoday.month, created_at__day=datetoday.day).count()
    moa_week = Moau.objects.filter(created_at__range=[start_week, end_week]).count()
    moa_month = Moau.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    event_today = Event.objects.filter(created_at__year=datetoday.year, created_at__month=datetoday.month, created_at__day=datetoday.day).count()
    event_week = Event.objects.filter(created_at__range=[start_week, end_week]).count()
    event_month = Event.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    memo_today = Memorandum.objects.filter(created_at__year=datetoday.year, created_at__month=datetoday.month, created_at__day=datetoday.day).count()
    memo_week = Memorandum.objects.filter(created_at__range=[start_week, end_week]).count()
    memo_month = Memorandum.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    letter_today = CommLetter.objects.filter(created_at__year=datetoday.year, created_at__month=datetoday.month, created_at__day=datetoday.day).count()
    letter_week = CommLetter.objects.filter(created_at__range=[start_week, end_week]).count()
    letter_month = CommLetter.objects.filter(created_at__year=today.year, created_at__month=today.month).count()
    order_today = SpecialOrder.objects.filter(created_at__year=datetoday.year, created_at__month=datetoday.month, created_at__day=datetoday.day).count()
    order_week = SpecialOrder.objects.filter(created_at__range=[start_week, end_week]).count()
    order_month = SpecialOrder.objects.filter(created_at__year=today.year, created_at__month=today.month).count()

    context = {
        'navbar': 'home',
        'moas': moas,
        'events': events,
        'memos': memos,
        'letters': letters,
        'orders': orders,
        'moa_today': moa_today,
        'moa_week': moa_week,
        'moa_month': moa_month,
        'event_today': event_today,
        'event_week': event_week,
        'event_month': event_month,
        'memo_today': memo_today,
        'memo_week': memo_week,
        'memo_month': memo_month,
        'letter_today': letter_today,
        'letter_week': letter_week,
        'letter_month': letter_month,
        'order_today': order_today,
        'order_week': order_week,
        'order_month': order_month,
    }

    return render(request, 'home/home.html', context)

def about_us(request):
    context = {
        'navbar': 'about'
    }
    return render(request, 'home/about_us.html', context)



def moas(request):
    moaus = Moau.objects.all()

    context = {
        'navbar': 'moa',
        'moaus': moaus
    }
    return render(request, 'home/moas.html', context)

def moa(request, pk):
    moa = Moau.objects.get(moau_no=pk)

    context = {
        'navbar': 'moa',
        'moa': moa
    }
    return render(request, 'home/moa.html', context)

def add_moa(request):
    form = MoauForm()
    user = request.user
    data = request.POST

    context = {
        'navbar': 'moa',
        'form': form,
        'data': data
    }

    if request.method == 'POST':
        form = MoauForm(request.POST, request.FILES)

        if form.is_valid():
            moa = form.save(commit=False)

            if data['moau_no'] == '':
                messages.error(request, 'Please enter a moau no')
                return render(request, 'home/add_moa.html', context)
            if Moau.objects.filter(moau_no=data['moau_no']).exists():
                messages.error(request, 'MOA No already exsists')
                return render(request, 'home/add_moa.html', context)

            moa.moau_no = data['moau_no']
            moa.moau_title = data['moau_title']
            moa.moau_objective = data['moau_objective']
            moa.moau_notarized_by = data['moau_notarized_by']
            moa.created_by = user.username
            moa.save()
            return redirect('moa', moa.moau_no)
            
    return render(request, 'home/add_moa.html', context)

def edit_moa(request, pk):
    moa = Moau.objects.get(moau_no=pk)
    form = MoauForm(instance=moa)
    user = request.user
    data = request.POST

    context = {
        'navbar': 'moa',
        'form': form,
        'data': data,
        'moa': moa
    }

    if request.method == 'POST':
        form = MoauForm(request.POST, request.FILES, instance=moa)


        if form.is_valid():
            moa = form.save(commit=False)

            if data['moau_no'] == '':
                messages.error(request, 'Please enter a moau no')
                return render(request, 'home/edit_moa.html', context)
            if Moau.objects.filter(moau_no=data['moau_no']).exists():
                if str(moa.moau_no) == str(data['moau_no']):
                    pass
                else:
                    messages.error(request, 'MOA No already exsists')
                    return render(request, 'home/edit_moa.html', context)

            moa.moau_no = data['moau_no']
            moa.moau_title = data['moau_title']
            moa.moau_objective = data['moau_objective']
            moa.moau_notarized_by = data['moau_notarized_by']
            moa.modified_by = user.username
            moa.save()
            return redirect('moa', moa.moau_no)
            
    return render(request, 'home/edit_moa.html', context)

def delete_moa(request, pk):
    moa = Moau.objects.get(moau_no=pk)
    moa.delete()
    return redirect('moas')

def add_party(request, pk):
    moa = Moau.objects.get(moau_no=pk)
    data = request.POST
    user = request.user

    context = {
        'navbar': 'moa',
        'data': data,
        'moa': moa
    }

    if request.method == 'POST':
        MoauParties.objects.create(
            moau=moa,
            agency=data['agency'],
            represented_by=data['represented_by'],
            position=data['position'],
            address=data['address'],
            referred_to_as=data['referred_to_as'],
            created_by=user.username
        )
        return redirect('moa', moa.moau_no)
    
    return render(request, 'home/add_party.html', context)

def edit_party(request, pk):
    party = MoauParties.objects.get(id=pk)
    data = request.POST
    user = request.user

    context = {
        'navbar': 'moa',
        'data': data,
        'party': party
    }

    if request.method == 'POST':
        party.agency = data['agency']
        party.represented_by = data['represented_by']
        party.position = data['position']
        party.address = data['address']
        party.referred_to_as = data['referred_to_as']
        party.modified_by = user.username
        party.save()
        return redirect('moa', party.moa.moau_no)
    
    return render(request, 'home/edit_party.html', context)

def delete_party(request, pk):
    party = MoauParties.objects.get(id=pk)
    party.delete()
    return redirect('moa', party.moau.moau_no)


def add_signatory(request, pk):
    moa = Moau.objects.get(moau_no=pk)
    data = request.POST
    user = request.user

    context = {
        'navbar': 'moa',
        'data': data,
        'moa': moa
    }

    if request.method == 'POST':
        MoauSignatories.objects.create(
            moau=moa,
            signed_by=data['signed_by'],
            position=data['position'],
            agency=data['agency'],
            created_by=user.username
        )
        return redirect('moa', moa.moau_no)
    
    return render(request, 'home/add_signatory.html', context)

def edit_signatory(request, pk):
    signatory = MoauSignatories.objects.get(id=pk)
    data = request.POST
    user = request.user

    context = {
        'navbar': 'moa',
        'data': data,
        'signatory': signatory
    }

    if request.method == 'POST':
        signatory.signed_by = data['signed_by']
        signatory.position = data['position']
        signatory.agency = data['agency']
        signatory.modified_by = user.username
        signatory.save()
        return redirect('moa', signatory.moa.moau_no)
    
    return render(request, 'home/edit_signatory.html', context)

def delete_signatory(request, pk):
    signatory = MoauSignatories.objects.get(id=pk)
    signatory.delete()
    return redirect('moa', signatory.moau.moau_no)



def events(request):
    events = Event.objects.all()
    context = {
        'navbar': 'events',
        'events': events
    }
    return render(request, 'home/events.html', context)

def event(request, pk):
    event = Event.objects.get(event_id=pk)
    context = {
        'navbar': 'events',
        'event': event
    }
    return render(request, 'home/event.html', context)

def add_event(request):
    form = EventForm()
    user = request.user
    data = request.POST

    context = {
        'navbar': 'events',
        'form': form,
        'data': data
    }

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)

            if data['event_id'] == '':
                messages.error(request, 'Please enter the event id')
                return render(request, 'home/add_event.html', context)
            if Event.objects.filter(event_id=data['event_id']).exists():
                messages.error(request, 'Event ID already exists')
                return render(request, 'home/add_event.html', context)

            event.event_id = data['event_id']
            event.event_name = data['event_name']
            event.event_agenda = data['event_agenda']
            event.event_venue = data['event_venue']
            event.no_participants = data['no_participants']
            event.impl_agency = data['impl_agency']
            event.created_by = user.username
            event.save()
            return redirect('events')
            
    return render(request, 'home/add_event.html', context)

def edit_event(request, pk):
    event = Event.objects.get(event_id=pk)
    form = EventForm(instance=event)
    user = request.user
    data = request.POST

    context = {
        'navbar': 'events',
        'form': form,
        'data': data,
        'event': event
    }

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            event = form.save(commit=False)

            if data['event_id'] == '':
                messages.error(request, 'Please enter the event id')
                return render(request, 'home/edit_event.html', context)
            if Event.objects.filter(event_id=data['event_id']).exists():
                if str(event.event_id) == str(data['event_id']):
                    pass
                else:
                    messages.error(request, 'Event ID already exists')
                    return render(request, 'home/edit_event.html', context)

            event.event_id = data['event_id']
            event.event_name = data['event_name']
            event.event_agenda = data['event_agenda']
            event.event_venue = data['event_venue']
            event.no_participants = data['no_participants']
            event.impl_agency = data['impl_agency']
            event.modified_by = user.username
            event.save()
            return redirect('event', event.event_id)
            
    return render(request, 'home/edit_event.html', context)

def delete_event(request, pk):
    event = Event.objects.get(event_id=pk)
    event.delete()
    return redirect('events')

def add_event_agency(request, pk):
    event = Event.objects.get(event_id=pk)
    data = request.POST
    user = request.user

    context = {
        'navbar': 'events',
        'data': data,
        'event': event
    }

    if request.method == 'POST':
        EventAgencies.objects.create(
            event=event,
            agency_id=data['agency_id'],
            agency_role=data['agency_role'],
            created_by=user.username
        )
        return redirect('event', event.event_id)
    return render(request, 'home/add_event_agency.html', context)

def edit_event_agency(request, pk):
    event_agency = EventAgencies.objects.get(id=pk)
    data = request.POST
    user = request.user

    context = {
        'navbar': 'events',
        'data': data,
        'event_agency': event_agency
    }

    if request.method == 'POST':
        event_agency.agency_id = data['agency_id']
        event_agency.agency_role = data['agency_role']
        event_agency.modified_by = user.username
        event_agency.save()
        return redirect('event', event_agency.event.event_id)
    
    return render(request, 'home/edit_event_agency.html', context)

def delete_event_agency(request, pk):
    event_agency = EventAgencies.objects.get(id=pk)
    event_agency.delete()
    return redirect('event', event_agency.event.event_id)



def memorandums(request):
    memorandums = Memorandum.objects.all()

    context = {
        'navbar': 'memorandum',
        'memorandums': memorandums
    }
    return render(request, 'home/memorandums.html', context)

def add_memo(request):
    form = MemoForm()
    user = request.user
    data = request.POST

    context = {
        'navbar': 'memorandum',
        'form': form,
        'data': data
    }

    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES)

        if form.is_valid():
            memo = form.save(commit=False)

            if data['memo_no'] == '':
                messages.error(request, 'Please enter a memo no')
                return render(request, 'home/add_memo.html', context)
            if Memorandum.objects.filter(memo_no=data['memo_no']).exists():
                messages.error(request, 'Memo No already exsists')
                return render(request, 'home/add_memo.html', context)

            memo.memo_no = data['memo_no']
            memo.memo_subject = data['memo_subject']
            memo.memo_content = data['memo_content']
            memo.memo_to = data['memo_to']
            memo.memo_to_pos = data['memo_to_pos']
            memo.memo_thru = data['memo_thru']
            memo.memo_thru_pos = data['memo_thru_pos']
            memo.memo_from = data['memo_from']
            memo.memo_from_pos = data['memo_from_pos']
            memo.memo_recomm_by = data['memo_recomm_by']
            memo.memo_approved_by = data['memo_approved_by']
            memo.created_by = user.username
            memo.save()
            return redirect('memorandums')
            
    return render(request, 'home/add_memo.html', context)

def edit_memo(request, pk):
    memo = Memorandum.objects.get(memo_no=pk)
    form = MemoForm(instance=memo)
    user = request.user
    data = request.POST

    context = {
        'navbar': 'memorandum',
        'form': form,
        'data': data,
        'memo': memo
    }

    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES, instance=memo)

        if form.is_valid():
            memo = form.save(commit=False)

            if data['memo_no'] == '':
                messages.error(request, 'Please enter a memo no')
                return render(request, 'home/edit_memo.html', context)
            if Memorandum.objects.filter(memo_no=data['memo_no']).exists():
                if str(memo.memo_no) == str(data['memo_no']):
                    pass
                else:
                    messages.error(request, 'Memo No already exsists')
                    return render(request, 'home/edit_memo.html', context)

            memo.memo_no = data['memo_no']
            memo.memo_subject = data['memo_subject']
            memo.memo_content = data['memo_content']
            memo.memo_to = data['memo_to']
            memo.memo_to_pos = data['memo_to_pos']
            memo.memo_thru = data['memo_thru']
            memo.memo_thru_pos = data['memo_thru_pos']
            memo.memo_from = data['memo_from']
            memo.memo_from_pos = data['memo_from_pos']
            memo.memo_recomm_by = data['memo_recomm_by']
            memo.memo_approved_by = data['memo_approved_by']
            memo.modified_by = user.username
            memo.save()
            return redirect('memorandums')
            
    return render(request, 'home/edit_memo.html', context)

def delete_memo(request, pk):
    memo = Memorandum.objects.get(memo_no=pk)
    memo.delete()
    return redirect('memorandums')



def comm_letters(request):
    letters = CommLetter.objects.all()

    context = {
        'navbar': 'letters',
        'letters': letters
    }
    return render(request, 'home/comm_letters.html', context)

def add_letter(request):
    form = LetterForm()
    user = request.user
    data = request.POST

    context = {
        'navbar': 'letters',
        'form': form,
        'data': data
    }

    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES)

        if form.is_valid():
            letter = form.save(commit=False)

            if data['letter_no'] == '':
                messages.error(request, 'Please enter the letter no')
                return render(request, 'home/add_letter.html', context)
            if CommLetter.objects.filter(letter_no=data['letter_no']).exists():
                messages.error(request, 'Letter No already exsists')
                return render(request, 'home/add_letter.html', context)

            letter.letter_no = data['letter_no']
            letter.letter_subject = data['letter_subject']
            letter.letter_to = data['letter_to']
            letter.letter_from = data['letter_from']
            letter.letter_received_by = data['letter_received_by']
            letter.letter_noted_by = data['letter_noted_by']
            letter.letter_recom_approval = data['letter_recom_approval']
            letter.letter_approved_by = data['letter_approved_by']
            letter.created_by = user.username
            letter.save()
            return redirect('comm-letters')
            
    return render(request, 'home/add_letter.html', context)

def edit_letter(request, pk):
    letter = CommLetter.objects.get(letter_no=pk)
    form = LetterForm(instance=letter)
    user = request.user
    data = request.POST

    context = {
        'navbar': 'letters',
        'form': form,
        'data': data,
        'letter': letter
    }

    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES, instance=letter)

        if form.is_valid():
            letter = form.save(commit=False)

            if data['letter_no'] == '':
                messages.error(request, 'Please enter the letter no')
                return render(request, 'home/edit_letter.html', context)
            if CommLetter.objects.filter(letter_no=data['letter_no']).exists():
                if str(letter.letter_no) == str(data['letter_no']):
                    pass
                else:
                    messages.error(request, 'Letter No already exsists')
                    return render(request, 'home/edit_letter.html', context)

            letter.letter_no = data['letter_no']
            letter.letter_subject = data['letter_subject']
            letter.letter_to = data['letter_to']
            letter.letter_from = data['letter_from']
            letter.letter_received_by = data['letter_received_by']
            letter.letter_noted_by = data['letter_noted_by']
            letter.letter_recom_approval = data['letter_recom_approval']
            letter.letter_approved_by = data['letter_approved_by']
            letter.modified_by = user.username
            letter.save()
            return redirect('comm-letters')
            
    return render(request, 'home/edit_letter.html', context)

def delete_letter(request, pk):
    letter = CommLetter.objects.get(letter_no=pk)
    letter.delete()
    return redirect('comm-letters')



def special_orders(request):
    orders = SpecialOrder.objects.all()

    context = {
        'navbar': 'orders',
        'orders': orders
    }
    return render(request, 'home/special_orders.html', context)

def add_order(request):
    form = OrderForm()
    user = request.user
    data = request.POST

    context = {
        'navbar': 'orders',
        'form': form,
        'data': data
    }

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)

        if form.is_valid():
            order = form.save(commit=False)

            if data['so_no'] == '':
                messages.error(request, 'Please enter the order no')
                return render(request, 'home/add_order.html', context)
            if SpecialOrder.objects.filter(so_no=data['so_no']).exists():
                messages.error(request, 'Order No already exsists')
                return render(request, 'home/add_order.html', context)

            order.so_no = data['so_no']
            order.so_subject = data['so_subject']
            order.so_content = data['so_content']
            order.so_signedby = data['so_signedby']
            order.created_by = user.username
            order.save()
            return redirect('special-orders')
    return render(request, 'home/add_order.html', context)

def edit_order(request, pk):
    order = SpecialOrder.objects.get(so_no=pk)
    form = OrderForm(instance=order)
    user = request.user
    data = request.POST

    context = {
        'navbar': 'orders',
        'form': form,
        'data': data,
        'order': order
    }

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)

        if form.is_valid():
            order = form.save(commit=False)

            if data['so_no'] == '':
                messages.error(request, 'Please enter the order no')
                return render(request, 'home/edit_order.html', context)
            if SpecialOrder.objects.filter(so_no=data['so_no']).exists():
                if str(order.so_no) == str(data['so_no']):
                    pass
                else:
                    messages.error(request, 'Order No already exsists')
                    return render(request, 'home/edit_order.html', context)

            order.so_no = data['so_no']
            order.so_subject = data['so_subject']
            order.so_content = data['so_content']
            order.so_signedby = data['so_signedby']
            order.modified_by = user.username
            order.save()
            return redirect('special-orders')
    return render(request, 'home/edit_order.html', context)

def delete_order(request, pk):
    order = SpecialOrder.objects.get(so_no=pk)
    order.delete()
    return redirect('special-orders')



def user_login(request):
    data = request.POST

    context = {
        'data': data
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if len(username) == 0 & len(password) == 0:
            messages.error(request, 'Please enter the credentials')
            return render(request, 'login_page.html', context)

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, f'Username "{username}" doesnt exists')
            return render(request, 'login_page.html', context)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password doesnt match')
    return render(request, 'login_page.html', context)

def user_logout(request):
    logout(request)
    messages.info(request, 'User successfully logout')
    return redirect('login')



def profile(request):
    user = request.user

    context = {
        'navbar': 'profile',
        'user': user
    }
    return render(request, 'home/profile.html', context)

def edit_profile(request):
    user = request.user
    form = UserPForm(instance=user)
    data = request.POST

    context = {
        'navbar': 'profile',
        'form': form
    }

    if request.method == 'POST':
        form = UserPForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            profile = form.save(commit=False)

            if data['username'] == '':
                messages.error(request, 'Please enter a username')
                return render(request, 'home/edit_profile.html', context)

            profile.name = data['name']
            profile.username = data['username']
            profile.email = data['email']
            profile.save()
            return redirect('profile')

    return render(request, 'home/edit_profile.html', context)

def edit_info(request):
    user = request.user
    form = UserIForm(instance=user)
    data = request.POST

    context = {
        'navbar': 'profile',
        'form': form
    }

    if request.method == 'POST':
        form = UserIForm(request.POST, instance=user)

        if form.is_valid():
            profile = form.save(commit=False)

            if any(c.isalpha() for c in data['employee_num']):
                messages.error(request, 'Employee # should only contain numbers')
                return render(request, 'home/edit_info.html', context)
            if any(c.isalpha() for c in data['phone_num']):
                messages.error(request, 'Phone number should only contain numbers')
                return render(request, 'home/edit_info.html', context)

            profile.employee_num = data['employee_num']
            profile.phone_num = data['phone_num']
            profile.nationality = data['nationality']
            profile.occupation = data['occupation']
            profile.address = data['address']
            profile.save()
            return redirect('profile')
            
    return render(request, 'home/edit_info.html', context)
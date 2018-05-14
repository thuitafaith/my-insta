from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import login
from gram.forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from gram.tokens import account_activation_token
from .models import Image,Profile,Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import EditForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


# Create your views here.
def signup(request):
    current_user = request.user
    if current_user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Gram Account'
            message = render_to_string('registration/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('registration/account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form':form})

def account_activation_sent(request):
    current_user = request.user
    if current_user.is_authenticated():
        return HttpResponseRedirect('intro')
    return render(request, 'registration/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('signup')
    else:
        return render(request, 'registration/account_activation_invalid.html')
def intro(request):

    return render(request,'intro.html')

@login_required(login_url='/login')
def profile(request):
    current_user = request.user
    profile_info = User.objects.get(id=current_user.id)

    edit_form = EditForm(instance=current_user)

    ProfileInlineFormset = inlineformset_factory(User, Profile, fields=('profile_photo', 'Bio'))
    formset = ProfileInlineFormset(instance=current_user)

    if current_user.is_authenticated() and request.user.id == current_user.id:
        if request.method == "POST":
            edit_form = EditForm(request.POST,request.FILES,instance=current_user)
            formset = ProfileInlineFormset(request.POST,request.FILES,instance=current_user)

            if edit_form.is_valid():
                created_user = edit_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST,request.FILES,instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect(current_user)
        return render(request, 'profile.html', {'profile_data': profile_info, "formset": formset, 'created_user': edit_form})
    else:
        raise PermissionDenied

@login_required(login_url='/login')
def post(request):
    current_user = request.user
    timeline_owner = Profile.objects.get(owner_profile=current_user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.image_link = timeline_owner
            post.save()
        return redirect(intro)
    else:
        form = PostForm()

    return render(request, 'newpost.html', {"form": form})

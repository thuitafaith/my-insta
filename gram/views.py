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
from .forms import EditForm,PostForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt


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

@csrf_exempt
@login_required(login_url='/login')
def intro(request):
    current_user = request.user
    images = Image.objects.all()
    image_list=[]
    for image in images:
        image_list.append((image, image.likes.filter(owner_profile=request.user)))

    return render(request, 'intro.html', {'images': image_list})

@csrf_exempt
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
@csrf_exempt
@login_required(login_url='/login')
def post(request):
    current_user = request.user
    timeline_owner = Profile.objects.get(owner_profile=current_user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner_profile = timeline_owner
            post.save()
        return redirect(intro)
    else:
        form = PostForm()

    return render(request, 'newpost.html', {"form": form})

@csrf_exempt
@login_required(login_url='/login')
def likes(request, image_id):
    current_user =request.user
    img = Image.objects.get(id=image_id)
    timeline_owner = Profile.objects.get(owner_profile=current_user)

    if request.method == 'POST' and request.is_ajax():
        like_status = request.POST['like']
        if like_status == 'true':
            img.likes.remove(timeline_owner)
            status = 'unliked'

        if like_status == 'false':
            img.likes.add(timeline_owner)
            status = 'liked'

        status = json.dumps(status)
        return HttpResponse(status, content_type='application/json')

    return redirect(intro)

@csrf_exempt
@login_required(login_url='/login')
def comments(request, image_id):
    current_user = request.user
    imge = Image.objects.get(id=image_id)
    timeline_owner = Profile.objects.get(owner_profile=current_user)

    if request.method == 'POST' and 'comment' in request.POST:
        comment = request.POST['comment']
        comment_item = Comment(image=imge,
                               profile=timeline_owner, comment_post=comment)
        comment_item.save()
        comments = Comment.objects.all()

        print(comment)

        # return render_to_response('comment.html', {'comments': comments})

    return redirect(intro)


@login_required(login_url='/login')
def profile_dis(request,username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('intro')
    profile = Profile.objects.get(user=user)

    name = f"{user.username}"
    return render(request, profile_display.html, {"name":name,"user":user,"profile":profile})

login_required(login_url='/login')
def profile_info(request):
    current_user = request.user
    profile_info = Profile.objects.filter(owner_profile=current_user.id).all()

    return render(request, 'profile-display.html', {'profile_data': profile_info})

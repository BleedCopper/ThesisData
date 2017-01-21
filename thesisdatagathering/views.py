from django.conf import settings
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twython import Twython
from thesisdatagathering.DataCleaner import DataCleaner
from dateutil.parser import parse
# Create your views here.
from thesisdatagathering.models import User, Post

CONSUMER_KEY = "6Ou9SSfowTYRYDsQJDX2g6pcV"
CONSUMER_SECRET = "6OT7ybjNe6HL2kKa7SM3hXnW4dwtziWfFroiFHoSwVPV49nRnR"


@csrf_exempt
def auth(request):
    # oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # oauth.set_access_token("2374233954-7qXgGv8iNwm1OHfYDsSNCjFnkE16hLJagKhC4D8", "UFOwbDsong5QuzMflfiTykn6y4mf7ZXf0Bbt5DLf5xxCt")
    # api = tweepy.API(oauth, proxy = "proxy.dlsu.edu.ph:80")
    # public_tweets = api.user_timeline()
    # for tweet in public_tweets:
    #     print (tweet.text)
    # twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET, client_args = {'proxies': {'https': 'http://proxy.dlsu.edu.ph:80'}})
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET)

    # Request an authorization url to send the user to...
    callback_url = request.build_absolute_uri(reverse('thesisdatagathering:twitter_callback'))
    auth_props = twitter.get_authentication_tokens(callback_url)

    # Then send them over there, durh.

    print(request.POST)
    request.session['request_token'] = auth_props
    request.session['date'] = (request.POST['bdmonth']+" "+request.POST['bdday']+","+request.POST['bdyear'])
    request.session['gender'] = request.POST['gender']
    return HttpResponseRedirect(auth_props['auth_url'])

@csrf_exempt
def facebookhandler(request):
    dc = DataCleaner()
    print(request.method)
    if request.method == 'POST':
        if 'posts[]' in request.POST:
            uid=request.POST['uid']
            posts = request.POST.getlist('posts[]')
            times = request.POST.getlist('time[]')
            print(request.POST)
            print(request.POST['month']+" "+request.POST['day']+","+request.POST['year'])

            date_object = parse(request.POST['month']+" "+request.POST['day']+","+request.POST['year'])

            stat= True
            try:
                user = User.objects.get(username=uid, source="Facebook")
                if not user.birthdate:
                    user.birthdate = date_object
                    user.gender=request.POST['gender']
                    user.save()
                else:
                    stat=False
            except User.DoesNotExist:
                user = User.objects.create(username=uid, gender=request.POST['gender'], birthdate=date_object ,source="Facebook")

            if(stat):
                for post,time in zip(posts,times):
                    date_object = parse(time)
                    # posFeature = POSFeature(dc.clean_data_facebook(post))
                    # test = [posFeature.nVerbs, posFeature.nAdjectives]

                    Post.objects.create(user=user, text=post, time=date_object.time())


                    # print('Message: ' + post)
            # doSomething with pieFact here...
            return HttpResponse('success') # if everything is OK
    # nothing went well
    return HttpResponse('FAIL!!!!!')

@csrf_exempt
def thanks(request, redirect_url='/thesisdatagathering?sent=true'):
    oauth_token = request.session['request_token']['oauth_token']
    oauth_token_secret = request.session['request_token']['oauth_token_secret']


    # twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
    #                   oauth_token, oauth_token_secret, client_args = {'proxies': {'https': 'http://proxy.dlsu.edu.ph:80'}})
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
                      oauth_token, oauth_token_secret)


    authorized_tokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'])

    tuser = authenticate(
        username=authorized_tokens['screen_name'],
        password=authorized_tokens['oauth_token_secret']
    )
    # login(request, user)

    # twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
    #                   authorized_tokens['oauth_token'], authorized_tokens['oauth_token_secret'], client_args = {'proxies': {'https': 'http://proxy.dlsu.edu.ph:80'}})

    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
                      authorized_tokens['oauth_token'], authorized_tokens['oauth_token_secret'])

    user_tweets = twitter.get_user_timeline()
    tuser = twitter.verify_credentials()
    uname = tuser['screen_name']
    print(uname)

    stat= True
    date_object = parse(request.session['date'])
    try:
        user = User.objects.get(username=uname, source="Twitter")
        if not user.birthdate:
            user.birthdate = date_object
            user.gender=request.session['gender']
            user.save()
        else:
            stat=False
    except User.DoesNotExist:
        user = User.objects.create(username=uname, gender=request.session['gender'], birthdate=date_object, source="Twitter")

    dc = DataCleaner()
    # print(dc.clean_data_twitter("hello @BleedCopper how are you? -Ohmie"))
    if(stat):
        for tweet in user_tweets:

            text = tweet['text']
            date = tweet['created_at']

            date_object = parse(date)

            # posFeature = POSFeature(dc.clean_data_twitter(text))
            # test = [posFeature.nVerbs, posFeature.nAdjectives]

            Post.objects.create(user=user, text=dc.clean_data_twitter(text), time=date_object.time())
    return HttpResponseRedirect(redirect_url)
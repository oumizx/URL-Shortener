from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import KirrURL
from .forms import SubmitUrlForm
from analytics.models import ClickEvent


# Create your views here
# def test_view(request):
# 	return HttpResponse("some stuff")

# def kirr_redirect_view(request, shortcode=None, *args, **kwargs): #function based view
# 	obj = get_object_or_404(KirrURL, shortcode=shortcode)
# 	#return HttpResponse("hello {sc}".format(sc=obj.url))
# 	return HttpResponseRedirect(obj.url)
def home_view_fbv(request, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
    return render(request, "shortener/home.html", {})


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        bg_image = 'http://orig05.deviantart.net/4129/f/2008/285/4/f/red_morning_i_by_serapstock.jpg'
        context = {
            "title": "Haonanzhu.com",
            "form": the_form,
            "bg_image": bg_image
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        # some_dict = {}
        # #some_dict['url']
        # some_dict.get('url', "http://www.google.com")
        # print(request.POST)
        # print(request.POST["url"])
        # print(request.POST.get("url"))
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Kirr.co",
            "form": form
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            if not 'http' in new_url:
                new_url = 'http://' + new_url
            obj, created = KirrURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"
            # print(form.cleaned_data)
        return render(request, template, context)


class URLRedirectView(View):  # class based view
    def get(self, request, shortcode=None, *args, **kwargs):
        # obj = get_object_or_404(KirrURL, shortcode=shortcode)
        # return HttpResponse("hello again {sc}".format(sc=shortcode))
        # save item
        qs = KirrURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exsits():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)

        # def post(self, request, *args, **kwargs):
        # 	return HttpResponse()

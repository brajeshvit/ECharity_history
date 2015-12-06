from django.db.models import Q
from django.db import models
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import Context
from products.models import ProductManager, ProductImage
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
# Custom Imports
from .forms import PostForm, ImageForm
#from .forms import VariationInventoryForm
from .models import Product, Variation
from .models import Slider
from .models import Product
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User



# Create your views here.
#################################################################################
#Product list view

def home(request):
	sliders = Slider.objects.all()
	products = Product.objects.filter(title__contains='E').order_by('-title')
	template = 'home.html'	
	context = {
		"products": products,
		"sliders": sliders,
		}
	return render(request, template, context)


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()


    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        # print context
        context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")
        return context


#Basic search function
#using q import from django.db.models import Q
# 
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
                )
            try:
                qs2 = self.model.objects.filter(
                Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs

##################################################################################
#Variation List view
class VariationListView(ListView):
    model = Variation
    queryset = Variation.objects.all()


    # def get_context_data(self, *args, **kwargs):
    #     context = super(VariationListView, self).get_context_data(*args, **kwargs)
    #     # print context
    #     context["now"] = timezone.now()
    #     context["query"] = self.request.GET.get("q")
    #     return context

    def get_queryset(self, *args, **kwargs):
        # qs = super(VariationListView, self).get_queryset(*args, **kwargs)
        # query = self.request.GET.get("q")
        product_pk= self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset


    def post (self, request, *args, **kwargs):
        raise Http404


##################################################################################
#Product Detail view
class ProductDetailView(DetailView):
    model = Product
    # template_name = "product.html"

    def product_detail_view_func(request, id):
        # product_instance = Product.objects.get(id=id)
        product_instance =  get_object_or_404(Product, id=id)
        try:
            product_instance = Product.object.get(id=id)
        except Product.DoesNotExist:
            raise Http404
        except:
            raise Http404

        template = "products/product_detail.html"
        context = {
        "object": product_instance
        }

        return render(request, template, context)

########################################################################################

def post_detail(request, pk):   
    post = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail1.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            #return redirect('products.views.ProductDetailView', pk=post.pk)
            #return render(request, 'products/product_list.html')   
            return redirect('products.views.post_detail', pk=post.pk) 
    else:
        form = PostForm()
    return render(request, 'products/post_edit.html', {'form': form})

#####################################################################################


def add_img(request, pk):
    if request.method == "POST":
        form = PostImgForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            #return redirect('products.views.ProductDetailView', pk=post.pk)
            #return render(request, 'products/product_list.html')   
            return redirect('products.views.post_detail', pk=post.pk) 
    else:
        form = PostForm()
    return render(request, 'products/post_edit.html', {'form': form})   
    
#####################################################################################


def post_edit(request, pk):
    post = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('products.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'products/post_img.html', {'form': form})


##########################################################################################

def post_list(request):
    model = Product, User
    posts = Product.objects.filter(user_id = request.user.id)
    return render(request, 'products/post_list.html', {'posts': posts})


##########################################################################################




def image_list(request):
   # model = Product, User  
    #images = ProductImage.objects.filter(id = request.user.id)
    images = ProductImage.objects.all()
    return render(request, "post_detail.html", {'images': images})
    


def image_upload(request, image_id=None):
    instance = None
    if image_id:
        instance = ProductImage.objects.get(pk=productimage_id)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            new_instance = form.save(commit=True)  # let's save the instance to get create its primary key

            if form.cleaned_data['delete_image'] and new_instance.image:
                new_instance.image.delete()

            if form.cleaned_data['image_path']:
                tmp_path = form.cleaned_data['image_path']
                abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

                fname, fext = os.path.splitext(os.path.basename(tmp_path))
                filename = slugify(fname) + fext

                new_instance.image.save(filename, File(open(abs_tmp_path, "rb")), False)
                os.remove(abs_tmp_path)
            new_instance.save()
            return redirect("image_list")
    else:
        form = ImageForm(instance=instance)

    return render(request, "products/image_upload.html", {'instance': instance, 'form': form})
    



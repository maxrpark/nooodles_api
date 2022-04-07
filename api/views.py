from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Brand, Tags, Ingredient, Noodle
# helper functions
from .utils import noodleList, noodleDescription


class Home(View):
    def get(self, request):
        return render(request, 'index.html')


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


# NOODLES


class NoodlesView(View):
    def get(self, request):
        all_noodles = Noodle.objects.all()
        if(all_noodles.count() > 0):
            return noodleList(all_noodles)
        else:
            return JsonResponse({'error': 'No found'}, safe=False)


class NoodleView(View):
    def get(self, request, slug):
        try:
            selectedNoodle = get_object_or_404(Noodle, slug=slug)
            noodle = noodleDescription(selectedNoodle)
            return JsonResponse(noodle, safe=False)
        except:
            return JsonResponse({'message': 'Noodle not found'}, status=404)
# CATEGORIES
# List of categories


class CategoriesList(View):
    def get(self, request):
        all_categories = Category.objects.all()
        categories_list = []
        for category in all_categories:
            data = {
                'id': category.id,
                'name': category.name,
                # 'slug': category.slug,
                'description': category.description,
            }
            categories_list.append(data)
        return JsonResponse(categories_list, safe=False)

# All noodles same category


class SingleCategory(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_category = all_noodles.filter(category__name=slug)
        if(single_category.count() > 0):
            return noodleList(single_category)
        else:
            return JsonResponse({'error': 'No such category'}, safe=False)

# INGREDIENTS
# Ingredients list


class IngredientsList(View):
    def get(self, request):
        all_ingredients = Ingredient.objects.all()
        ingredients_list = []
        for ingredient in all_ingredients:
            data = {
                'id': ingredient.id,
                'name': ingredient.name,
            }
            ingredients_list.append(data)
        return JsonResponse(ingredients_list, safe=False)

# All noodles by Ingredient


class SingleIngredient(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_ingredient = all_noodles.filter(ingredients__name=slug)
        if(single_ingredient.count() > 0):
            return noodleList(single_ingredient)
        else:
            return JsonResponse({'error': 'No such ingredient'}, safe=False)

# BRANDS
# list of brands


class BrandsList(View):
    def get(self, request):
        all_brands = Brand.objects.all()
        brand_list = []
        for brand in all_brands:
            data = {
                'id': brand.id,
                'name': brand.name,
                'slug': brand.slug,
            }
            brand_list.append(data)
        return JsonResponse(brand_list, safe=False)

# all noodles same brand


class Singlebrand(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_brand = all_noodles.filter(brand__slug=slug)
        if(single_brand.count() > 0):
            return noodleList(single_brand)
        else:
            return JsonResponse({'error': 'No such brand'}, safe=False)


# TAGS
#  list of tags
class TagsList(View):
    def get(self, request):
        all_tags = Tags.objects.all()
        tags_list = []
        for tag in all_tags:
            data = {
                'id': tag.id,
                'name': tag.name,
            }
            tags_list.append(data)
        return JsonResponse(tags_list, safe=False)

# All noodles by tags


class SingleTag(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_tag = all_noodles.filter(tags__name=slug)
        if(single_tag.count() > 0):
            return noodleList(single_tag)
        else:
            return JsonResponse({'error': 'No such tag'}, safe=False)


# search noodle by name
class SearchNoodle(View):
    def get(self, request):
        query = request.GET.get('query', '')
        print(query)
        all_noodles = Noodle.objects.all()
        noodle = all_noodles.filter(
            Q(name__icontains=query))
        if(noodle.count() > 0):
            print(query, 'found')
            print(noodle)
            return noodleList(noodle)
        else:
            return JsonResponse({'response': 'No noodle found'}, safe=False)

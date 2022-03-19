from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Category, Brand, Tags, Ingredient, Noodle, NoodleImage

from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

# List of things


class NoodlesView(View):
    def get(self, request):
        all_noodles = Noodle.objects.all()
        noodles_list = []
        for noodle in all_noodles:
            noodle_img = NoodleImage.objects.filter(noodle=noodle)

            data = {
                'id': noodle.id,
                'name': noodle.name,
                'description': noodle.summary,
                'spicy_level': noodle.spicy_level.level,
                'category': noodle.category.name,
                'brand': noodle.brand.name,
                'tags': [tag.name for tag in noodle.tags.all()],
                'ingredients': [ingredient.name for ingredient in noodle.ingredients.all()],
                'instructions': noodle.instructions,
                'images': [image.image.url for image in noodle_img],
                'amount_per_package': noodle.amount_per_package,
                'price_per_package': noodle.price_per_package,
                'price_per_unite': noodle.price_per_unite,
                'slug': noodle.slug,
            }
            print(noodle)
            noodles_list.append(data)
        return JsonResponse(noodles_list, safe=False)


# all list of categories
class CategoriesList(View):
    def get(self, request):
        all_categories = Category.objects.all()
        categories_list = []
        for category in all_categories:
            data = {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
            }
            categories_list.append(data)
        return JsonResponse(categories_list, safe=False)

# Ingredients list


class IngredientsList(View):
    def get(self, request):
        all_ingredients = Ingredient.objects.all()
        print(all_ingredients)
        ingredients_list = []
        for ingredient in all_ingredients:
            data = {
                'id': ingredient.id,
                'name': ingredient.name,
            }
            ingredients_list.append(data)
        return JsonResponse(ingredients_list, safe=False)

# list of brands


class BrandsList(View):
    def get(self, request):
        all_brands = Brand.objects.all()
        brand_list = []
        for brand in all_brands:
            data = {
                'id': brand.id,
                'name': brand.name,
            }
            brand_list.append(data)
        return JsonResponse(brand_list, safe=False)

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

# noodles by thing

# all noodles same category


class SingleCategory(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_category = all_noodles.filter(category__name=slug)
        if(single_category.count() > 0):
            single_category_list = []
            for noodle in single_category:
                noodle_img = NoodleImage.objects.filter(noodle=noodle)

                data = {
                    'id': noodle.id,
                    'name': noodle.name,
                    'description': noodle.summary,
                    'spicy_level': noodle.spicy_level.level,
                    'category': noodle.category.name,
                    'brand': noodle.brand.name,
                    'tags': [tag.name for tag in noodle.tags.all()],
                    'ingredients': [ingredient.name for ingredient in noodle.ingredients.all()],
                    'instructions': noodle.instructions,
                    'images': [image.image.url for image in noodle_img],
                    'amount_per_package': noodle.amount_per_package,
                    'price_per_package': noodle.price_per_package,
                    'price_per_unite': noodle.price_per_unite,
                    'slug': noodle.slug,
                }
                print(noodle)
                single_category_list.append(data)
            return JsonResponse(single_category_list, safe=False)
        else:
            return JsonResponse({'error': 'No such category'}, safe=False)

# all noodles same brand


class Singlebrand(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_brand = all_noodles.filter(brand__slug=slug)
        single_brand_list = []
        if(single_brand.count() > 0):
            for noodle in single_brand:
                noodle_img = NoodleImage.objects.filter(noodle=noodle)

                data = {
                    'id': noodle.id,
                    'name': noodle.name,
                    'description': noodle.summary,
                    'spicy_level': noodle.spicy_level.level,
                    'category': noodle.category.name,
                    'brand': noodle.brand.name,
                    'tags': [tag.name for tag in noodle.tags.all()],
                    'ingredients': [ingredient.name for ingredient in noodle.ingredients.all()],
                    'instructions': noodle.instructions,
                    'images': [image.image.url for image in noodle_img],
                    'amount_per_package': noodle.amount_per_package,
                    'price_per_package': noodle.price_per_package,
                    'price_per_unite': noodle.price_per_unite,
                    'slug': noodle.slug,
                }
                single_brand_list.append(data)
            return JsonResponse(single_brand_list, safe=False)
        else:
            return JsonResponse({'error': 'No such brand'}, safe=False)


# All noodles by tags
class SingleTag(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_tag = all_noodles.filter(tags__name=slug)
        single_tag_list = []
        if(single_tag.count() > 0):
            for noodle in single_tag:
                noodle_img = NoodleImage.objects.filter(noodle=noodle)

                data = {
                    'id': noodle.id,
                    'name': noodle.name,
                    'description': noodle.summary,
                    'spicy_level': noodle.spicy_level.level,
                    'category': noodle.category.name,
                    'brand': noodle.brand.name,
                    'tags': [tag.name for tag in noodle.tags.all()],
                    'ingredients': [ingredient.name for ingredient in noodle.ingredients.all()],
                    'instructions': noodle.instructions,
                    'images': [image.image.url for image in noodle_img],
                    'amount_per_package': noodle.amount_per_package,
                    'price_per_package': noodle.price_per_package,
                    'price_per_unite': noodle.price_per_unite,
                    'slug': noodle.slug,
                }
                single_tag_list.append(data)
            return JsonResponse(single_tag_list, safe=False)
        else:
            return JsonResponse({'error': 'No such tag'}, safe=False)


# All noodles by tags
class SingleIngredient(View):
    def get(self, request, slug):
        all_noodles = Noodle.objects.all()
        single_ingredient = all_noodles.filter(ingredients__name=slug)
        if(single_ingredient.count() > 0):
            print(single_ingredient)
            single_ingredient_list = []
            for noodle in single_ingredient:
                noodle_img = NoodleImage.objects.filter(noodle=noodle)

                data = {
                    'id': noodle.id,
                    'name': noodle.name,
                    'description': noodle.summary,
                    'spicy_level': noodle.spicy_level.level,
                    'category': noodle.category.name,
                    'brand': noodle.brand.name,
                    'tags': [tag.name for tag in noodle.tags.all()],
                    'ingredients': [ingredient.name for ingredient in noodle.ingredients.all()],
                    'instructions': noodle.instructions,
                    'images': [image.image.url for image in noodle_img],
                    'amount_per_package': noodle.amount_per_package,
                    'price_per_package': noodle.price_per_package,
                    'price_per_unite': noodle.price_per_unite,
                    'slug': noodle.slug,
                }
                single_ingredient_list.append(data)
            return JsonResponse(single_ingredient_list, safe=False)
        else:
            return JsonResponse({'error': 'No such ingredient'}, safe=False)

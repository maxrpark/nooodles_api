from django.http import JsonResponse, request, response
from django.views import View

from .models import Category, Brand, Tags, Ingredient, Noodle, SpicyLevel, NoodleImage


class NoodlesView(View):
    def get(self, request):
        all_noodles = Noodle.objects.all()
        noodles_list = []
        for noodle in all_noodles:
            noodle_img = NoodleImage.objects.filter(noodle=noodle)
            print([image.image.url for image in noodle_img])
            data = {
                'id': noodle.id,
                'name': noodle.name,
                # 'price': noodle.price,
                'description': noodle.summary,
                'spicy_level': noodle.spicy_level.level,
                'category': noodle.category.name,
                'brand': noodle.brand.name,
                'tags': [tag.name for tag in noodle.tags.all()],
                'ingredients': [ingredient.name for ingredient in noodle.ingredients.all()],
                'images': [image.image.url for image in noodle_img]
            }
            print(noodle)
            noodles_list.append(data)
        return JsonResponse(noodles_list, safe=False)

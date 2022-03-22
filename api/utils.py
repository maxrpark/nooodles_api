from django.http import JsonResponse
from .models import NoodleImage


def noodleDescription(noodle):
    noodle_img = NoodleImage.objects.filter(noodle=noodle)
    noodle_img = NoodleImage.objects.filter(noodle=noodle)
    UUII = str(noodle.created_at)[12:26].replace(
        ':', '').replace('.', '')
    data = {
        'id': UUII,
        'name': noodle.name,
        'description': noodle.summary,
        'spicy_level': noodle.spicy_level.level,
        'category': noodle.category.name,
        'brand': {
            "name": noodle.brand.name,
            "slug": noodle.brand.slug},
        'tags': [tag.name for tag in noodle.tags.all()],
        'ingredients': [ingredient.name for ingredient in noodle.ingredients.all()],
        'instructions': noodle.instructions,
        'images': [image.image.url for image in noodle_img],
        'amount_per_package': noodle.amount_per_package,
        'price_per_package': noodle.price_per_package,
        'price_per_unite': noodle.price_per_unite,
        'rating': noodle.rating,
        'slug': noodle.slug,
    }
    return data


def noodleList(result):
    noodle_list = []
    for noodle in result:
        data = noodleDescription(noodle)
        noodle_list.append(data)
    return JsonResponse(noodle_list, safe=False)

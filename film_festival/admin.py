from django.contrib import admin

from film_festival.models import Film, Rating, Upvote, Provider

class FilmAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'watched', 'watched_date', 'total_upvotes')
    ordering = ('-watched', 'watched_date', '-total_upvotes', 'created')
admin.site.register(Film, FilmAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('film', 'stars', 'user')
admin.site.register(Rating, RatingAdmin)

class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('film', 'user')
admin.site.register(Upvote, UpvoteAdmin)

admin.site.register(Provider)

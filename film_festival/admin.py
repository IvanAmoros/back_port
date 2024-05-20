from django.contrib import admin

from film_festival.models import Film, Rating, Upvote

class FilmAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'watched', 'watched_date', 'total_upvotes')
    ordering = ('-watched', 'watched_date', '-total_upvotes')

admin.site.register(Film, FilmAdmin)

admin.site.register(Rating)
admin.site.register(Upvote)

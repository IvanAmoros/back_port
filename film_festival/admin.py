from django.contrib import admin

from film_festival.models import Film, Rating

class FilmAdmin(admin.ModelAdmin):
    list_display = ('tittle', 'watched', 'watched_date', 'up_votes')
    ordering = ('-watched', 'watched_date', '-up_votes')

admin.site.register(Film, FilmAdmin)

admin.site.register(Rating)

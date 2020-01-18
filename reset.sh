

# 4 lines below resets all
#find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
#find . -path "*/migrations/*.pyc"  -delete
#python3 manage.py makemigrations
#python3 manage.py migrate
python3 manage.py delete_all_data
python3 manage.py importcsv --mappings='' --model='activities.MealActivity'  data/db.meals.csv
python3 manage.py importcsv --mappings='' --model='activities.EventActivity'  data/db.events.csv
python3 manage.py convert_coords


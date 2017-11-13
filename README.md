# P5_OpenFoodFacts
Projet n°5 : Utilisez les données publiques de l'OpenFoodFacts

How to install : 

1. Use theese command to authorize the access to the BDD :
  
  "GRANT ALL PRIVILEGES ON openfoodfacts.* TO 'your_name'@'localhost' IDENTIFIED BY 'your_password';"
  
2. Create a file named "config.py" containing the following code : 

  mysql = {'host': 'localhost',
'user': 'your_name',
'passwd': 'your_password'}

3. Install the 'requirements.txt' file. 

4. Run 'database_create.py'

Then you can run : 'open_food_find.py'

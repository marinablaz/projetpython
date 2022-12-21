<h1> Projet Python pour le Data Scientist </h1>

<h2> Eléa Bordais, Marina Blazevic, Côme Nadler et Clothilde Voisin </h2>

Voici le Github réalisé dans le cadre de notre projet "Python pour le Data Scientist" de 2ème année à l'ENSAE Paris.

Nous avons décidé de nous intéresser aux prix des Airbnb parisiens. AirBnb est une plateforme créée en 2008, qui avait à l'origine pour but de permettre à des particuliers de mettre en location leur bien pour des courtes durées (par exemple pendant des périodes de vacances où le bien est inoccupé). Cependant, la plateforme a connu un énorme succès, et depuis, certains utilisateurs en ont fait leur activité principale et louent leurs biens de façon permanente. Nous avons donc voulu comprendre le marché d'AirBnb et comment les prix se comportaient sur ce marché, afin de pouvoir les comparer aux prix de loyers parisiens de biens loués à des fins de résidence permanente (par exemple par des agences). 


La base de données utilisée provient du site Open Data soft, qui scrappe les données d'Airbnb dans plusieurs grandes villes à travers le monde et donne accès à plus de 50 000 données sur les AirBnb Parisiens. Nous avons également scrappé des données du site SuperImmo pour obtenir les prix de différents loyers parisiens.  

Notre projet s'articule en plusieurs parties. Dans un premier temps, nous avons nettoyé la base et effectué plusieurs statistiques descriptives pour comprendre quelles variables semblaient influencer le prix, puis nous avons réalisé des cartes interactives pour mieux visualiser l'impact de l'arrondissement dans le prix des Airbnb. Ensuite, nous avons analysé de manière plus approfondie l'impact des reviews sur Airbnb sur le prix.  
Dans une seconde partie, nous avons créé un modèle afin de prédire au mieux le prix des AirBnb, en utilisant au fur et à mesure des méthodes de plus en plus sophistiquées. Pour finir, dans une troisième partie, nous nous sommes intéressés aux équipements des appartements afin d'améliorer le modèle de prédiction.

Les fichiers sont : 
- notebook--final, qui contient le corps principal du projet
- scraping.py, qui contient tout le code lié au scrapping de SuperImmo

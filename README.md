# edulib2PDF
Télécharger et convertir un manuel edulib en PDF

# Prérequis importants :
Vous devez installer l'outil système [wkhtmltopdf](https://wkhtmltopdf.org/) sur votre machine pour que la conversion fonctionne.

- Windows : Télécharger l'installateur sur le site officiel de wkhtmltopdf et l'installer.
- Linux : `sudo apt-get install wkhtmltopdf`
- macOS : `brew install wkhtmltopdf`

Ensuite, installez les librairies Python nécessaires :

```
pip install requests pdfkit pypdf beautifulsoup4
```

# Récupérer l'ID 
1. Allez sur [https://www.edulib.fr/demo/bibliotheque](https://www.edulib.fr/demo/bibliotheque) et sélectionnez votre manuel préféré
2. Cliquez sur "Voir la démo" (⚠️ça doit vous rediriger vers un lien ***libmanuel.fr*** sinon ça ne fonctionne pas)
3. L'identifiant se trouve désormais dans l'URL :

```
https://www.libmanuels.fr/demo/9782210120969/specimen/0/?title=EMC%20Lyc%C3%A9e%20(2025)%20%E2%80%93%20Nouveaux%20programmes%202de,%201re,%20Tle&editor=Magnard
```
Ici, l'identifiant est **9782210120969**

→ Finalement, il suffit d'utiliser cet identifiant [ici](https://github.com/XenocodeRCE/edulib2PDF/blob/main/main.py#L10) et [là](https://github.com/XenocodeRCE/edulib2PDF/blob/main/main.py#L11) et de lancer le script python 

```
python main.py
```

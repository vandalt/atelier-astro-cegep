# %% [markdown]
# # Atelier pour le cours d'astronomie
#
# ## Format de l'atelier
#
# L'atelier a été créé sous forme de cahier [Jupyter Notebook](https://jupyter.org/) car ce dernier permet d'afficher des figures et du texte formatté via GitHub. Le cahier mélange des cellules de texte (comme celle que vous lisez présementement) et des cellules de code (comme la prochaine). Le code est un code Python normal. Vous pouvez donc copier des bouts de code dans un éditeur. J'ai également inclut une version `.py` de l'atelier. Cependant, la version "blank" aura beaucoup de commentaires et sera peut-être difficile à lire.
#
# Si vous utilisez autre chose qu'un cahier Jupyter, je suggère donc de créer un nouveau fichier dans votre éditeur, de lire les instructions dans ce fichier-ci et de copier le code dans votre fichier à mesure que l'atelier progresse.
#
# ## Contexte
#
# Dans cet atelier, nous allons explorer l'analyse de données du télescope spatial James Webb (JWST).
# Nous allons calculer la photométrie de naines Y en utilisant les données du programme [GO 2473](https://www.stsci.edu/jwst-program-info/program/?program=2473), mené par mon collègue [Loïc Albert](https://exoplanetes.umontreal.ca/en/team-member/loic-albert/).
#
# Les naines Y sont les [naines brunes](https://fr.wikipedia.org/wiki/Naine_brune) les plus froides et les moins brillantes.
# Les naines brunes sont des objets astrophysiques qui se forment comme les étoiles, mais qui n'atteignent pas une masse suffisamment élevée pour la fusion nucléaire.
# Ainsi, elles se refroidissent continuellement avec le temps et ont des masses entre 13 et 75 fois celle de Jupiter.
# Leur faible masse et leur basse température font qu'elles ressemblent en plusieurs points aux exoplanètes géantes.
# Or, elles sont souvent isolées (elles n'orbitent pas une étoile), ce qui les rend plus faciles à observer.
# Elles sont donc, en plus d'être intéressantes en elles-même, d'excellent « proxy » pour mieux comprendre les planètes géantes.
#
# Vu leur basse température, les naines Y émettent la majorité de leur lumière dans l'infrarouge.
# Ceci les rend très difficile à observer à partir du sol, ou bien à partir de l'espace avec un télescope opérant dans le visible comme Hubble.
# Le télescope Webb est donc l'observatoire parfait pour les étudier plus en détails.
# Plus spécifiquement, nous avons obtenu des données d'imagerie avec l'instrument [NIRCam](https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-observing-modes/nircam-imaging#gsc.tab=0).
#
# L'objectif principal de ce programme d'observation est la recherche de compagnons.
# Par compagnon, on désigne d'autres naines Y encore plus froides qui seraient en orbite autour des cibles de notres programmes.
# Elles ne sont techniquement pas des planètes car les naines brunes ne sont pas des étoiles.
# Nous avons pour l'instant trouvé [un seul compagnon](https://ui.adsabs.harvard.edu/abs/2023ApJ...947L..30C/abstract), et je suis en train de compléter l'analyse du programme dans un article qui devrait paraître plus tard cette année.
#
# Vu la qualité des données Webb, il est également intéressant de contraindre la luminosité des cibles dans le programme via une analyse photométrique.
# Mon collègue Loïc a récemment publié [un article](https://ui.adsabs.harvard.edu/abs/2025AJ....169..163A/abstract) à ce sujet.
# Aujourd'hui, nous allons reproduire certaines parties de cette analyse.
# Plus spécifiquement, nous allons:
#
# - Accéder aux données en ligne via Python
# - Visualiser les données
# - Calculer la somme du flux dans les images pour calculer la photométrie
#
# ## Importation et visualisation d'une image
#
# ### Accès aux données via MAST
#
# Les données JWST sont disponibles sur le portail [MAST](https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html).
# Ce portail en ligne peut-être utilisé manuellement ou bien avec Python.
# Pour l'utiliser avec Python, nous allons recourir à [astroquery](https://astroquery.readthedocs.io/en/latest/).
# Si on connait l'URL des données qu'on souhaite télécharger, l'interface est assez simple.
#
# Les observations ont été effectuées avec deux filtres photométriques (couleurs): F150W et F480M.
# Le premier est un filtrer large (W pour _wide_) observant à 1.5 $\mu$m et le second est un filtre moyen (M pour _medium_) observant à 4.8 $\mu$m.
# Observer avec deux filtres différents nous permet de calculer la couleur de l'objet pour la comparer avec des modèles théoriques, et NIRCam peut observer deux couleurs en parallèle, donc aucun temps additionnel n'est requis!
#
# Ici, j'ai pré-sélectionné les observations de WISE-0366, l'une des cibles observée par notre programme.
# Le code ci-dessous télécharge ces données si elles ne sont pas déjà sur votre ordinateur.
#
# Pour cet atelier, toutes les données sont également sur la page GitHub si jamais le téléchargement par Python ne fonctionne pas.
#
# **Exercice: Avec l'interface MAST, téléchargez les données, mais seulement si elles ne sont pas sur votre ordinateur.**

# %%
from pathlib import Path
from astroquery.mast import Observations

# Les objets "Path" sont plus pratique à manipuler que des strings
data_dir = Path("./data")

# Dictionnaire donnant le nom des fichiers pour chaque filtre (couleur).
files = {
    "f150w": "jw02473-o053_t053_nircam_clear-f150w_i2d.fits",
    "f480m": "jw02473-o053_t053_nircam_clear-f480m_i2d.fits",
}
base_uri = "mast:JWST/product/"
# TODO: Download

# %% [markdown]
# Voilà! Les données devraient maintenant apparaître sous `data`.
#
# **Exercice: Vérifiez que les données sont sous `data` en listant son contenu**

# %%
# TODO: Check

# %% [markdown]
# ### Ouverture des fichiers et méta-données
#
# Maintenant que les fichiers sont sur notre disque dur, on peut utiliser [Astropy](https://docs.astropy.org/en/latest/io/fits/index.html) pour les ouvrir.
# Commençons par explorer le contenu du fichier en F480M.

# %%
filename = files["f480m"]
filepath = data_dir / filename

# %% [markdown]
# **Exercice: ouvrez le fichier dans une variable `hdul` et affichez ses informations**

# %%
# TODO: Fits file

# %% [markdown]
# Comme on peut voir ici, le fichier contient plusieurs extensions.
# Chaque extension peut inclure une en-tête avec des méta-données, ainsi que des données (image, tableau, etc.).
# Par convention, l'extension 0 (`PRIMARY`) ne contient pas de données et seulement une en-tête avec des informations sur le programme.
# Les observations qui nous intéressent sont dans l'extension `1`, ou `"SCI"`.

# %%
import pprint  # pretty print

# hdr = hdul[0].header
# TODO: sci_hdr et data
# hdul.close()  # On ferme le fichier maintenant que tout est extrait
# print("En-tête:")
# pprint.pprint(hdr)

# %% [markdown]
# **Exercice: Modifiez la cellule ci-dessus pour extraire les données dans une variable `data_f480m` et l'en-tête SCI dans `sci_hdr`. Affichez ensuite le contenu de `sci_hdr`.**

# %%
# TODO: Print sci_hdr

# %% [markdown]
# Voilà pour les en-têtes. On peut en extraire de l'information utile, notamment les unités dans lesquelles le flux est rapporté.
#
# **Exercice: En examinant l'en-tête, trouvez la clé (_key_) donnant les unités de flux. Complétez ensuite la cellule ci-dessous.**

# %%
# TODO: Flux units
print("Unités du flux:")
# print(flux_units)

# %% [markdown]
# Les données sont en megaJansky par steradian.
# Un Jansky mesure la densité de flux spectrale et est égal à $10^{−26}$ W m$^{−2}$ Hz$^{−1}$.
# Un steradian est une mesure d'angle solide (radian carré).
#
# ### Affichage de l'image
#
# Regardons maintenant de quoi a l'air notre image.

# %%
# print("Type de donnée:", type(data_f480m))
# print("Format des données:", data_f480m.shape)
print("Données:")
# print(data_f480m)

# %% [markdown]
# Les images sont stockées en tableaux [NumPy](https://numpy.org/).
# On voit ici que l'image a une taille de 2070x2076 pixels.
# Par contre, lorsqu'on imprime les données, tous les pixels ont une valeur `nan`, pour « not a number ».
# Cette valeur est utilisée pour signifier que les pixels au bord de l'image sont inutilisables.
# Si on regarde un segment au centre de l'image, on devrait voir des valeurs numériques.
# Une façon rapide de le vérifier est d'afficher l'image avec Matplotlib.
#
# La fonction `plt.imshow()` nous permet d'afficher l'image.
# On peut ajouter une barre de couleurs avec `plt.colorbar()` pour avoir une idée des valeurs numériques.
#
# **Exercice: Affichez l'image**

# %%
import matplotlib.pyplot as plt

plt.style.use("tableau-colorblind10")  # Je suis daltonien

# TODO: Display image

# %% [markdown]
# On voit que la majorité des pixels ne sont en effet pas des `nan`. Bonne nouvelle!
# Par contre, on ne voit pas grand chose dans l'image
# Ceci se produit généralement lorsque quelques pixels sont très brillants. Le reste des pixels apparaît alors comme très sombres.
# On pourrait manuellement zoomer sur la barre de couleurs, mais ce n'est pas optimal.
#
# Voyons voir si une échelle logarithmique nous aide à y voir plus clair avec `norm="log"`.
# N'hésitez pas à zoomer sur l'image pour voir la forme des sources de lumière.
#
# **Exercice: Reproduisez la figure ci-dessus avec une échelle log pour les couleurs**

# %%
# TODO: Normalisation log

# %% [markdown]
# On voit dans l'image ci-dessus que nos images NIRCam sont des images à grand champ: on n'observe pas uniquement l'étoile ou la naine brune qui nous intéresse, mais son voisinage également.
# Nous identifierons WISE-0336 plus bas
#
# Il resterait deux choses à faire pour améliorer la visualisation:
#
# 1. Matplotlib mets le pixel `(0, 0)` en haut à gauche de l'image, comme il est positionné dans un tableau. Il est plus intuitif de l'afficher en bas avec `origin="lower"`. On peut ajouter cet argument à `plt.imshow()` ou configurer Matplotlib pour le reste du code avec `rcParams`.
# 2. Les sources les plus brillantes affectent encore l'échelle de la barre de couleurs. Les arguments `vmin` et `vmax` permettent de changer la gamme dynamique de l'image. On peut utiliser les quantiles de l'image pour les ajuster.
# 3. On peut changer [les couleurs](https://matplotlib.org/stable/users/explain/colors/colormaps.html) pour du rouge, afin de mieux représenter l'infrarouge (totalement facultatif, on pourrait utiliser une échelle de gris également).
#
# **Exercice: Complétez les changement ci-dessus et affichez à nouveau l'image.**

# %%
import numpy as np
from matplotlib import rcParams

# TODO: origin lower
# TODO: Default cmap

# TODO: vmin et vmax

# TODO: Plot

# %% [markdown]
# On voit certains effets de détecteur dans les images: des lignes horizontales et 4 rectangles verticaux.
# On peut les ignorer pour l'instant. On se concentrera sur une toute petite région du détecteur.
#
# ## Images dans les deux couleurs
#
# Maintenant que la structure des images nous est familière, on peut importer les donné du filtre F150W également.
# La structure est la même que pour les données F480M.
# On peut créer un dictionnaire pour y accéder facilement.
#
# **Exercice: Importez l'image F150W et ajoutez la à `data_dict`.**

# %%
# TODO: F150W

data_dict = {
    # "f480m": data_f480m,
    # TODO: F150W
}

# %% [markdown]
# On peut maintenant afficher les images.
# Nous répéterons ces opérations quelque fois, donc on peut créer des fonctions.
#
# **Exercice: Affichez les deux image, puis convertissez votre code en une fonction `plot_image(data)` pour afficher une seule image ainsi qu'une fonction `plot_images(data_dict)` pour afficher les deux couleurs côte à côte.**

# %%
# plot_images(data_dict)
plt.show()

# %% [markdown]
# On remarque que le détecteur « bleu » ou _Courtes longueurs d'ondes_ de NIRCam est segmenté en 4.
# Voir la [documentation](https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-instrumentation/nircam-detector-overview#gsc.tab=0) pour plus de détails.
#
# Ajustons l'échelle pour mieux voir les sources
#
# **Exercice: Ajoutez l'option `use_vmin_vmax` à votre fonction. Elle devrait ajuster les quantiles comme nous avons fait plus haut.**

# %%
# TODO: Uncomment
# plot_images(data_dict, use_vmin_vmax=True)
# plt.show()

# %% [markdown]
# ## Position de la source
#
# On pourrait ancrer l'image à des coordonnées [WCS](https://docs.astropy.org/en/stable/wcs/index.html), mais ce ne sera pas nécessaire pour notre exercice.
# Les images ont été obtenues à grand champ, mais on la photométrie se calcule uniquement dans les quelques pixels autour de notre source d'intérêt.
#
# WISE-0336 est une naine Y, donc elle est très froide, ce qui veut dire qu'elle est beaucoup plus brillante en F480M qu'en F150W.
# Essayons de l'identifier visuellement d'abord.

# %%
# plot_images(data_dict, use_vmin_vmax=True)
plt.show()

# %% [markdown]
# Pour notre projet, nous avons d'abord cherché les sources de cette manière, puis nous avons confirmé la position avec les coordonnées connues.
# La position pour chaque filtre est notée ci-dessous.

# %%
object_name = "WISE-0336"
f150_pos = (2734, 1759)
f480_pos = (1296, 840)
pos_dict = {
    "f480m": f480_pos,
    "f150w": f150_pos,
}

# %% [markdown]
# On peut afficher la position pour chaque filtre ensuite.
#
# **Exercice: Modifiez votre fonction pour afficher une étoile à la position de WISE-0336 dans les deux filtres. Ajoutez l'argument `pos_dict`.**

# %%
# plot_images(data_dict, use_vmin_vmax=True, pos_dict=pos_dict)
plt.show()

# %% [markdown]
# ## Découpage de la source
#
# Maintenant que nous avons trouvé WISE-0336, inutile de garder toute l'image.
# Une région d'une soixantaine de pixels suffira.
# Dans chaque filtre, on peut découper 68 pixels autour de la source et afficher cette nouvelle image.
#
# **Exercice: Découpez une région de 68x68 pixels autours de WISE-0336 dans chaque filtre. Affichez ensuite cette image.**

# %%
# TODO: Crop and show

# %% [markdown]
# ## Photométrie d'ouverture
#
# Maintenant que la cible d'intérêt est isolée, on peut calculer sa luminosité.
# Comme dans l'article mentionné au début du code, nous utiliserons la photométrie d'ouverture.
# Cette technique consiste à:
#
# 1. Trouver le centre de la cible
# 2. Définir une ouverture circulaire d'une taille donnée autour du centre
# 3. Calculer le flux total dans l'ouverture
# 4. Définir un anneau autour de la cible pour calculer le bruit de fond
# 5. Soustraire le bruit de fond
# 6. Convertir le flux en magnitude
#
# La librairie [photutils](https://photutils.readthedocs.io/en/stable/) implémente ce dont nous avons besoin pour faire ces calculs (sauf 6).
# Cependant, afin de bien comprendre toutes les étapes, c'est toujours une bonne idée de coder la solution manuellement lorsque l'on s'intéresse à un problème pour une première fois.
# Nous allons donc tout calculer nous même et comparer nos résultats avec ceux de photutils.
# Nous utiliserons uniquement les données F480M, comme le signal est meilleur dans ce filtre.
#
# **Note: Nous avons coupé les données à une taille égale de chaque côté. Ceci permet à des erreurs de dimensions de se glisser très facilement dans nos calcul. Un truc simple pour éviter ces erreurs pendant le développement est de changer la taille d'un des axes avec `data= data[:-1]`**.
# On peut ensuite enlever cette opération quand le code est terminé.

# %%
# TODO: Remove :-1
# data = crop_dict["f480m"]
# data = data[:-1]

# %% [markdown]
# ### Conversion des unités
#
# Avant de commencer nos calculs il faut convertir les unités de flux.
# Comme mentionné plus tôt, les données sont en MJy/sr, qui donne une luminosité de surface.
# Ici, on souhaite travailler directement avec un flux. Nous avons deux options:
#
# 1. Convertir les données vers des photons/seconde avec `sci_hdr["PHOTMJSR"]`
# 2. Convertir les données vers des Jansky avec `sci_hdr["PIXAR_SR"]`, qui donne la surface d'un pixel en steradian
#
# Le calcul de la photométrie se fait de la même façon dans les deux cas.
# Seule l'étape 6 est différente.
# Ici, nous allons utiliser l'option 2 car elle simplifie légèrement l'étape 6.

# %%
# 1e6 Jy/MJy et PIXAR_SR SR / pixel
# mjsr_to_jy = 1e6 * sci_hdr["PIXAR_SR"]
# data = data * mjsr_to_jy
flux_units = "Jy"

# %% [markdown]
# ### 1. Trouver le centre de la cible
#
# Commençons par vérifier si la cible est au centre de l'image.
#
# **Exercice: Affichez l'image F480M ainsi qu'une ligne verticale et horizontale au milieu de chaque axe.**

# %%
# TODO: Add lines
# plot_image(data)
plt.show()

# %% [markdown]
# Elle ne semble pas l'être tout à fait! Regardons de plus près.
#
# **Exercice: Affichez le centre de l'image seulement**

# %%
# TODO: Lines + Zoom
# plot_image(data)
plt.show()

# %% [markdown]
# On remarque deux choses:
#
# 1. Le pixel central n'est pas nécessairement le plus brillant.
# 2. L'image n'est pas parfaitement centrée sur un pixel.
#
# Le point 1 vient du fait que nous avons déterminé la position de la source approximativement avant de découper l'image.
# Pour ce qui est du point 2, il se peut que la source soit centrée entre deux pixels. Il faut donc calculer une position centrale plus précise, et pas seulement trouver le pixel le plus brillant.
#
# Il y a différentes façons de trouver le centre d'une image. Photutils implémente celles-ci dans son module [`centroids`](https://photutils.readthedocs.io/en/stable/user_guide/centroids.html):
#
# - Trouver le "centre de masse" de l'image
# - Ajuster un polynôme quadratique en 2 dimensions au centre de l'image
# - Ajuster une distribution gaussienne 1D à chaque dimension de l'image
# - Ajuster une distribution gaussienne 2D à l'image
#
# Nous utiliserons la première méthode ci-dessus: celle du centre de masse (CDM).
# Ici, centre de masse est une analogie: le flux dans chaque pixel est la « masse » du pixel.
# On doit donc calculer une moyenne pondérée de la position des pixels où les poids sont le flux dans chaque pixel.
# Ainsi, si tous les pixels sont égaux, le CDM est au milieu de l'image.
# Si tous les pixels sont à 0 mais qu'un pixel est non nul, le CDM sera sur ce pixels.
# Si tous les pixels sont à 0 mais que deux pixels sont non nuls et égaux, le CDM sera à mi-chemin entre ces deux pixels.
# Dans un cas réaliste comme ici, aucun pixel n'est nul. Chaque pixel "tire" le centre de masse vers lui en fonction de son flux.
#
# Nous allons donc calculer une somme pondérée de la position des pixels.
#
# **Exercice: Trouvez le centre de masse de l'image et affichez le sur un graphique. Attention aux axes: lequel est x et lequel est y?**
#
# <details>
# <summary>Cliquez pour un indice</summary>
#
# Faite une boucle sur chaque axe de `data` et pour chaque pixel:
#
# 1. Obtenez le flux
# 2. Multipliez la position x par le flux et ajoutez la à la moyenne en x
# 3. Multipliez la position y par le flux et joutez la à la moyenne en y
# 4. Divisez la moyenne par la somme des poids
# </details>

# %%
# TODO: COM

# %% [markdown]
# Voyons maintenant ce que `photutils` trouve comme centre de masse.

# %%
from photutils.centroids import centroid_com
# xy_com = centroid_com(data)
# print("Centre de masse photutils", xy_com)

# %% [markdown]
# ### 2 et 4. Ouverture circulaire et anneau pour le bruit de fond
#
# Il faut maintenant définir notre ouverture et notre anneau pour calculer le bruit de fond.
# Pour ce faire, nous utiliserons deux dictionaires qui contiennent les positions x et y des pixels dans chaque ouverture, ainsi que le flux de ces pixels.
#
# **Exercice: Remplissez les dicionnaires ci-dessous.**
#
# <details>
# <summary>Cliquez pour un indice</summary>
#
# Pour chaque pixel:
#
# 1. Calculez sa distance du centre
# 2. Si sa distance du centre est inférieure à `r_src` ajoutez le à `src_aperture`
# 2. Si sa distance est entre `r_in` et `r_out` ajoutez le à `bkg_aperture`.
# </details>

# %%
# Ouverture pour la source
src_aperture = {
    "x": [],
    "y": [],
    "flux": [],
}
# Ouverture (anneau) bruit de fond
bkg_aperture = {
    "x": [],
    "y": [],
    "flux": [],
}
r_src = 8  # Rayon source
r_in = 10  # Rayon intérieur fond
r_out = 15  # Rayon extérieur fond
# TODO: Fill apertures

# %% [markdown]
# **Exercice: Affichez les pixels appartenant à chaque ouverture**

# %%
# fig, ax = plot_image(data)
# TODO: Ajouter les ouvertures
# fig.legend()
plt.show()

# %% [markdown]
# Voyons voir ce qu'en dit `photutils`.
# Le module [`aperture`](https://photutils.readthedocs.io/en/stable/user_guide/aperture.html) contient ce dont nous avons besoin.

# %%
# from photutils.aperture import CircularAnnulus, CircularAperture

# src_photutils = CircularAperture(xy_com, r=r_src)
# bkg_photutils = CircularAnnulus(xy_com , r_in=r_in, r_out=r_out)

# fig, ax = plot_image(data)
# src_photutils.plot(ax=ax, color="C0", label="Ouverture photutils")
# bkg_photutils.plot(ax=ax, color="C2", label="Background photutils")
plt.legend()
plt.show()

# %% [markdown]
# Et superposons les deux méthodes
#
# **Exercice: Superposez les ouvertures que vous avez calculez et celles de photutils pour les comparer**

# %%
# TODO: Combine

# %% [markdown]
# ### 3 et 5. Calculer le flux total et le bruit de fond
#
# Nous avons maintenant tout ce qu'il faut pour calculer la photométrie.
# Il suffit de faire la somme du flux et de soustraire le bruit de fond.
#
# **Exercice: Calculez le flux total, puis corrigez le en soustrayant le bruit de fond. Soustrayez la médiane du bruit de fond de chaque pixel dans votre somme.**

# %%
bkg_flux = bkg_aperture["flux"]
median_bkg = np.median(bkg_flux)
src_flux = src_aperture["flux"]
N_pix = len(src_flux)
bkg_tot = N_pix * median_bkg
src_tot = np.sum(src_flux)
src_phot = src_tot - bkg_tot
print("Median background flux", median_bkg)
print("Total background flux", bkg_tot)
print("Raw source flux", src_tot)
print("Corrected source flux", src_phot)

# %% [markdown]
# On peut vérifier les résultats avec photutils.
# On utilise la méthode `center` qui approxime au pixel près, comme nous faisons plus haut.

# %%
from photutils.aperture import ApertureStats, aperture_photometry

# NOTE: Petite différence pour exact vs "center"
# bkg_stats = ApertureStats(data, bkg_photutils)
# src_stats = ApertureStats(data, src_photutils, sum_method="center")
# photutils_aphot = aperture_photometry(data - bkg_stats.median, src_photutils, method="center")
# print("Median background flux", bkg_stats.median)
# print("Raw source flux", src_stats.sum)
# print("Aperture photometry")
# print(photutils_aphot)

# %% [markdown]
# ### 6. Conversion du flux en magnitude
#
# Nous avons maintenant le flux total en Jy.
# Typiquement, la luminosité des objets astronomique est mesurée avec des [magnitudes](https://en.wikipedia.org/wiki/Magnitude_(astronomy)).
#
# La façon la plus rapide d'obtenir des magnitudes est de convertir d'abord en magnitudes AB, puis en magnitude Vega en utilisant un fichier de référence fournipar l'équipe Webb.
# Les équations ci-dessous sont tirées de la [documentation pour la calibration en flux NIRCam](https://jwst-docs.stsci.edu/jwst-near-infrared-camera/nircam-performance/nircam-absolute-flux-calibration-and-zeropoints#gsc.tab=0).
#
# **Exercice: Nous allons compléter cette section en groupe. Mais les équations sont disponibles au lien ci-dessus si vous avez de l'avance.**

# %%
import asdf

# TODO: AB mag
ab_mag = None

def get_abvega_offset(filt: str):
    abvega_path = data_dir / "jwst_nircam_abvegaoffset_0002.asdf"
    with asdf.open(abvega_path) as af:
        offset_tbl = af["abvega_offset"]
    mask = (offset_tbl["filter"] == filt.upper()) & (offset_tbl["pupil"] == "CLEAR")
    offset_row = offset_tbl[mask]
    assert len(offset_row) == 1
    offset_row = offset_row[0]
    return offset_row["abvega_offset"]

# TODO: Convert with offset
vega_mag = None
print("Magnitude Vega", vega_mag)

# %% [markdown]
# ### 7. Correction d'ouverture
#
# Si vous comparez la magnitude ci-dessus avec celle de l'[article](https://ui.adsabs.harvard.edu/abs/2025AJ....169..163A/abstract) pour le même objet, vous remarquerez une petite différence.
# Il faut en réalité corriger la magnitude pour tenir compte du fait que nous utilisons une ouverture finie, et qu'une partie de la luminosité n'est donc pas inclue dans l'ouverture.
#
# La correction dépend du rayon de l'ouverture et de l'anneau de bruit de fond.
# Il faut donc répéter le calcul de la photométrie avec les paramètres `r_phot`, `skyin` et `skyout` dans le dictionnaire ci-dessous. Il est encore une fois itré d'un fichier de référence Webb.
# Ensuite, il faudra multiplier le flux total par `apcorr`.
# Utilisons `photutils` pour répéter l'analyse.

# %%
aperture_info_dict = {
    "f480m": dict(zip(("filt", "pupil", "ee", "r_phot", "apcorr", "skyin", "skyout"), ('F480M', 'CLEAR', 0.7 ,  3.757,  1.4863, 4.92 , 7.083))),
    "f150w": dict(zip(("filt", "pupil", "ee", "r_phot", "apcorr", "skyin", "skyout"), ('F150W', 'CLEAR', 0.7 ,  3.199,  1.4485, 6.082, 9.496))),
}
aperture_info = aperture_info_dict["f480m"]
print(aperture_info)

# %%
# TODO: Répéter toutes les étapes avec photutils.

# %% [markdown]
# La magnitude est maintenant similaire à celle rapportée dans l'article!
#
# ## Conclusions
#
# Voilà! Nous avons traversé toutes les étapes du calcul de la photométrie d'ouverture.
# Avec ce code, vous devriez pouvoir refaire le calcul pour le filtre F150W ou même pour une autre cible.
#
# Suggestions d'exercices additionnels, si vous voulez explorer le sujet un peu plus:
#
# - Adaptez le code pour calculer la photométrie du filtre F150W également
# - Nous n'avons pas calculé d'incertitudes! Les opérations effectuées ci-dessus respectent les mêmes règles de propagation d'erreur que vous avez vues lors de vos laboratoire. Pouvez-vous propager l'incertitude de l'image (donnée par l'extension `ERR`) au flux total? Puis à la magnitude? L'exemple du lien ci-dessous montre un exemple de calcule tenant compte des incertitudes.
# - Explorez cet exemple de l'équipe JWST montrant comment calculer photométrie d'ouverture pour plusieurs étoiles dans la même image: <https://spacetelescope.github.io/jdat_notebooks/notebooks/NIRCam/aperture_photometry/NIRCam_Aperture_Photometry_Example.html#point-source-aperture-photometry>
# - Explorez cet exemple de photométrie sur des images de galaxies: <https://spacetelescope.github.io/jdat_notebooks/notebooks/NIRCam/NIRCam_photometry/NIRCam_multiband_photometry.html>. La photométrie se calcule un peu différemment pour les sources étendues.

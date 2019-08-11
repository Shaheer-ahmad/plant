import numpy as np
import tensorflow as tf
from keras.preprocessing import image
import io
import base64 
from PIL import Image
import pandas as pd
import re


class prediction():

	def __init__(self):

		# Load model into memory
		self.session = tf.Session()
		self.graph = tf.get_default_graph()
		with self.graph.as_default():
			with self.session.as_default():
				print ("Model inialized...")
				self.model = tf.keras.models.load_model('resnet_weights_16_1.h5')
		print ("Model loaded....")

		#Load labels into memory
		# f = open('labels.txt', 'r')
		# self.labels = f.readlines()
		# self.labels = [item.replace('\n','').replace('_',' ') for item in self.labels]
		# f.close()

		# Load csv into memory
		self.df = pd.read_csv('species.csv', sep=';')
		self.df.fillna("", inplace = True)
		print ("datagra", self.df)
		print('Everything loaded..')

	def predict(self, base64_string):
		try:

			image_ = self.stringToImage(base64_string)
			x = image.img_to_array(image_)
			x = np.expand_dims(x, axis=0)

			images = np.vstack([x])
			with self.graph.as_default():
				with self.session.as_default():
					classes = self.model.predict_classes(images)
			predicted_class = self.get_mapping(classes[0])
			predicted_class = predicted_class.replace('_',' ')

			name, family, author = self.get_details(predicted_class)
			return True, predicted_class, name, family, author

		except Exception as e:
			print ("Exception in predict ",e)
			return False, '', '', '', ''

	def stringToImage(self, base64_string):
		imgdata = base64.b64decode(base64_string)
		image = Image.open(io.BytesIO(imgdata))
		image = image.resize((96, 96), Image.ANTIALIAS)
		return image

	def get_details(self, label):
		try:
			return self.df.loc[self.df['Scientific name'].str.contains(label, flags=re.IGNORECASE, regex=True)][['name', 'family', 'AUTHOR']].to_numpy()[0]
		except Exception as e:
			print ("Exception in get_details ",e)
			return '', '', ''

	def get_mapping(self, label):
		try:
			dict_ = {'abies_concolor': 0,
			 'abies_nordmanniana': 1,
			 'acer_campestre': 2,
			 'acer_ginnala': 3,
			 'acer_griseum': 4,
			 'acer_negundo': 5,
			 'acer_palmatum': 6,
			 'acer_pensylvanicum': 7,
			 'acer_platanoides': 8,
			 'acer_pseudoplatanus': 9,
			 'acer_rubrum': 10,
			 'acer_saccharinum': 11,
			 'acer_saccharum': 12,
			 'aesculus_flava': 13,
			 'aesculus_glabra': 14,
			 'aesculus_hippocastamon': 15,
			 'aesculus_pavi': 16,
			 'ailanthus_altissima': 17,
			 'albizia_julibrissin': 18,
			 'amelanchier_arborea': 19,
			 'amelanchier_canadensis': 20,
			 'amelanchier_laevis': 21,
			 'asimina_triloba': 22,
			 'betula_alleghaniensis': 23,
			 'betula_jacqemontii': 24,
			 'betula_lenta': 25,
			 'betula_nigra': 26,
			 'betula_populifolia': 27,
			 'broussonettia_papyrifera': 28,
			 'carpinus_betulus': 29,
			 'carpinus_caroliniana': 30,
			 'carya_cordiformis': 31,
			 'carya_glabra': 32,
			 'carya_ovata': 33,
			 'carya_tomentosa': 34,
			 'castanea_dentata': 35,
			 'catalpa_bignonioides': 36,
			 'catalpa_speciosa': 37,
			 'cedrus_atlantica': 38,
			 'cedrus_deodara': 39,
			 'cedrus_libani': 40,
			 'celtis_occidentalis': 41,
			 'celtis_tenuifolia': 42,
			 'cercidiphyllum_japonicum': 43,
			 'cercis_canadensis': 44,
			 'chamaecyparis_pisifera': 45,
			 'chamaecyparis_thyoides': 46,
			 'chionanthus_retusus': 47,
			 'chionanthus_virginicus': 48,
			 'cladrastis_lutea': 49,
			 'cornus_florida': 50,
			 'cornus_kousa': 51,
			 'cornus_mas': 52,
			 'corylus_colurna': 53,
			 'crataegus_crus-galli': 54,
			 'crataegus_laevigata': 55,
			 'crataegus_phaenopyrum': 56,
			 'crataegus_pruinosa': 57,
			 'crataegus_viridis': 58,
			 'cryptomeria_japonica': 59,
			 'diospyros_virginiana': 60,
			 'eucommia_ulmoides': 61,
			 'evodia_daniellii': 62,
			 'fagus_grandifolia': 63,
			 'ficus_carica': 64,
			 'fraxinus_americana': 65,
			 'fraxinus_nigra': 66,
			 'fraxinus_pennsylvanica': 67,
			 'ginkgo_biloba': 68,
			 'gleditsia_triacanthos': 69,
			 'gymnocladus_dioicus': 70,
			 'halesia_tetraptera': 71,
			 'ilex_opaca': 72,
			 'juglans_cinerea': 73,
			 'juglans_nigra': 74,
			 'juniperus_virginiana': 75,
			 'koelreuteria_paniculata': 76,
			 'larix_decidua': 77,
			 'liquidambar_styraciflua': 78,
			 'liriodendron_tulipifera': 79,
			 'maclura_pomifera': 80,
			 'magnolia_acuminata': 81,
			 'magnolia_denudata': 82,
			 'magnolia_grandiflora': 83,
			 'magnolia_macrophylla': 84,
			 'magnolia_soulangiana': 85,
			 'magnolia_stellata': 86,
			 'magnolia_tripetala': 87,
			 'magnolia_virginiana': 88,
			 'malus_angustifolia': 89,
			 'malus_baccata': 90,
			 'malus_coronaria': 91,
			 'malus_floribunda': 92,
			 'malus_hupehensis': 93,
			 'malus_pumila': 94,
			 'metasequoia_glyptostroboides': 95,
			 'morus_alba': 96,
			 'morus_rubra': 97,
			 'nyssa_sylvatica': 98,
			 'ostrya_virginiana': 99,
			 'oxydendrum_arboreum': 100,
			 'paulownia_tomentosa': 101,
			 'phellodendron_amurense': 102,
			 'picea_abies': 103,
			 'picea_orientalis': 104,
			 'picea_pungens': 105,
			 'pinus_bungeana': 106,
			 'pinus_cembra': 107,
			 'pinus_densiflora': 108,
			 'pinus_echinata': 109,
			 'pinus_flexilis': 110,
			 'pinus_koraiensis': 111,
			 'pinus_nigra': 112,
			 'pinus_parviflora': 113,
			 'pinus_peucea': 114,
			 'pinus_pungens': 115,
			 'pinus_resinosa': 116,
			 'pinus_rigida': 117,
			 'pinus_strobus': 118,
			 'pinus_sylvestris': 119,
			 'pinus_taeda': 120,
			 'pinus_thunbergii': 121,
			 'pinus_virginiana': 122,
			 'pinus_wallichiana': 123,
			 'platanus_acerifolia': 124,
			 'platanus_occidentalis': 125,
			 'populus_deltoides': 126,
			 'populus_grandidentata': 127,
			 'populus_tremuloides': 128,
			 'prunus_pensylvanica': 129,
			 'prunus_sargentii': 130,
			 'prunus_serotina': 131,
			 'prunus_serrulata': 132,
			 'prunus_subhirtella': 133,
			 'prunus_virginiana': 134,
			 'prunus_yedoensis': 135,
			 'pseudolarix_amabilis': 136,
			 'ptelea_trifoliata': 137,
			 'pyrus_calleryana': 138,
			 'quercus_acutissima': 139,
			 'quercus_alba': 140,
			 'quercus_bicolor': 141,
			 'quercus_cerris': 142,
			 'quercus_coccinea': 143,
			 'quercus_falcata': 144,
			 'quercus_imbricaria': 145,
			 'quercus_macrocarpa': 146,
			 'quercus_marilandica': 147,
			 'quercus_michauxii': 148,
			 'quercus_montana': 149,
			 'quercus_muehlenbergii': 150,
			 'quercus_nigra': 151,
			 'quercus_palustris': 152,
			 'quercus_phellos': 153,
			 'quercus_robur': 154,
			 'quercus_rubra': 155,
			 'quercus_shumardii': 156,
			 'quercus_stellata': 157,
			 'quercus_velutina': 158,
			 'quercus_virginiana': 159,
			 'robinia_pseudo-acacia': 160,
			 'salix_babylonica': 161,
			 'salix_caroliniana': 162,
			 'salix_matsudana': 163,
			 'salix_nigra': 164,
			 'sassafras_albidum': 165,
			 'staphylea_trifolia': 166,
			 'stewartia_pseudocamellia': 167,
			 'styrax_japonica': 168,
			 'styrax_obassia': 169,
			 'syringa_reticulata': 170,
			 'taxodium_distichum': 171,
			 'tilia_americana': 172,
			 'tilia_cordata': 173,
			 'tilia_europaea': 174,
			 'tilia_tomentosa': 175,
			 'toona_sinensis': 176,
			 'tsuga_canadensis': 177,
			 'ulmus_americana': 178,
			 'ulmus_glabra': 179,
			 'ulmus_parvifolia': 180,
			 'ulmus_procera': 181,
			 'ulmus_pumila': 182,
			 'ulmus_rubra': 183,
			 'zelkova_serrata': 184}

			for key, value in dict_.items():
				if value == label:
					return key
		except Exception as e:
			print ("Exception in get_mapping ",e)

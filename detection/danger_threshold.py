# Tespit edilecek tehlikeli nesnelerin listesi
#'knife', 'gun', 'scissors', 'firearm', 'axe', 'sword'
TEHLIKELI_NESNELER = ['knife', 'gun', 'scissors']

# Algılama için varsayılan güven eşiği
# Bu eşik, 'TEHLIKELI_NESNELER' listesinde olmayan diğer tüm nesneler için geçerli.
DEFAULT_CONF_THRESHOLD = 0.30

# 'knife' sınıfı için özel güven eşiği
KNIFE_CONF_THRESHOLD = 0.07

# Tehlike oranı hesaplaması için kurallar:
# Her tespit edilen insan için eklenecek tehlike puanı
PERSON_DANGER_SCORE = 5

# Tehlikeli bir nesne tespit edildiğinde eklenecek tehlike puanı
DANGEROUS_OBJECT_SCORE = 50

# Maksimum tehlike oranı yüzdesi
MAX_DANGER_PERCENTAGE = 100

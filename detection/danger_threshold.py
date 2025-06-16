# Tespit edilecek tehlikeli nesnelerin listesi
TEHLIKELI_NESNELER = ['knife', 'gun', 'scissors']

# Modelin tanıyabildiği hayvan sınıflarının listesi
ANIMAL_CLASSES = [
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
    'bear', 'zebra', 'giraffe'
]

# Algılama için varsayılan güven eşiği
DEFAULT_CONF_THRESHOLD = 0.25

# 'knife' sınıfı için özel güven eşiği
KNIFE_CONF_THRESHOLD = 0.07

# Tehlike oranı hesaplaması için kurallar:
PERSON_DANGER_SCORE = 5
DANGEROUS_OBJECT_SCORE = 50
MAX_DANGER_PERCENTAGE = 100

# Sadece gösterilmesine izin verilen sınıflar (insan, tehlikeli nesneler, hayvanlar)
# Bu liste app.py içinde dinamik olarak oluşturulacak

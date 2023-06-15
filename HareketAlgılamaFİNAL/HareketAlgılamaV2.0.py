import cv2
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Video Yakalama için VideoCapture kullanıyoruz ve (0) dediğimiz ise kameranın listedeki yeri
# yani eğer 2 tane kameramız varsa 2. kamerayı açmak için (1) yazmamız lazım.
capture = cv2.VideoCapture(0)

# Maskeleyeceğimiz yere 3 değer atıyoruz = History, Threshold, DetectShadows
# History: Arkaplanda kaç frame olduğunda arkaplan modeli yenileneceğini seçiyor.
# Threshold: önceki piksel frame ve önceki pozisyonu ile sonraki pozisyonu karşılaştırarak ne kadar farklı olduğunu belirler.
# DetectShadows: Gölge tespiti yapılıp yapılmayacağını belirler.
maske = cv2.createBackgroundSubtractorMOG2(500, 750, True)

# hangi frame'de olduğumuzu takip edecek
kare_sayisi = 0

# E-posta gönderme ayarları
smtp_server = 'smtp.gmail.com'
smtp_port = 587
email_address = 'korocan1907@gmail.com'  # Gönderici e-posta adresi
email_password = 'vegxnhzeiwlngafb'  # Gönderici e-posta şifresi
recipient_address = 'denemeogrenci03@gmail.com'  # Alıcı e-posta adresi

def send_email(subject, message):
    # E-posta gövdesi oluşturma
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient_address
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # E-posta gönderme işlemi
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_address, email_password)
    server.send_message(msg)
    server.quit()

while(1):
    # Anlık frame değerini döndürür.
    ret, frame = capture.read()

    # Bir değer var mı diye kontrol eder, yoksa döngüden çıkar.
    if not ret:
        break

    kare_sayisi += 1
    # Frame'i yeniden boyutlandırır.
    frame_yeni = cv2.resize(frame, (0, 0), fx=1, fy=1)

    # Yeni frame'in boyutunda yüzey maskesi oluşturulur.
    yuzey_maske = maske.apply(frame_yeni)

    # Maske'deki siyah olmayan pikseller sayılır.
    pixelsayaci = np.count_nonzero(yuzey_maske)

    # Çıktıyı alır.
    print('Görüntü: %d, Değişen pixel sayısı: %d' % (kare_sayisi, pixelsayaci))

    # Maske'nin değerleri vektör olarak x, y, w, h değişkenlerine atanır.
    x, y, w, h = cv2.boundingRect(yuzey_maske)

    # Eğer değişen pixel sayısı belli sayıdan yüksekse hareket olarak algılanır.
    if (kare_sayisi > 1 and pixelsayaci > 500):
        print('Hareket Algılandı')
        # Hareket edilen yer bulunduğunda dörtgen içine alınır.
        frame_yeni = cv2.rectangle(frame_yeni, (x, y), (x + w, y + h), (0, 250, 0), 2)
        cv2.putText(frame_yeni, 'Hareket Algılandı', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # E-posta gönderimi
        subject = 'Hareket Algılandı'
        message = 'Hareket algılandı! Hareketin olduğu konum: x={}, y={}, w={}, h={}'.format(x, y, w, h)
        send_email(subject, message)

        # Kayıt yapma (isteğe bağlı)
        # cv2.imwrite('motion_detected.jpg', frame_yeni)

    # Pencere oluşturup gösterir.
    cv2.imshow('Kamera', frame_yeni)
    cv2.imshow('Maske', yuzey_maske)

    k = cv2.waitKey(1) & 0xff
    if k == 27:  # Escape tuşuna basılınca çıkar.
        break

# Döngüden çıktıktan sonra yakalamalar iptal edilir ve tüm pencereler kapatılır.
capture.release()
cv2.destroyAllWindows()

# OpenCV Hareket Algılama Final Projesi
# Bu proje Sistem Analizi ve Tasarımı II dersi kapsamında hazırlanmıştır.
# Kerem Bilir 
Bu proje, OpenCV kütüphanesi kullanarak bir video kaynağından alınan görüntüleri işleyerek, eğer bir hareket algılanırsa bunu ekrana yazı olarak yazdırır ve hareketin olduğu bölgeyi kutu içine alarak görsel olarak belirtir. Bu düzenlenmiş proje, hareket algılandığında e-posta gönderimi yapacak ve e-posta içeriğinde hareketin olduğu konumu belirtecektir. E-posta gönderimi için smtplib kütüphanesi kullanılmaktadır. Ayrıca, isteğe bağlı olarak hareket algılandığında görüntünün kaydedilmesi de sağlanmıştır (cv2.imwrite işlevi ile). Bu özellikler, kodu hareket algılama sisteminizi daha işlevsel hale getirmek için geliştirmektedir.

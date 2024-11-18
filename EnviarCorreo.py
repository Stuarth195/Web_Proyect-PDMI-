import smtplib
import ssl
from email.message import EmailMessage


class EmailSender:
    # Definimos los valores constantes del remitente y la contraseña
    EMAIL_SENDER = "arielsabalv@gmail.com"
    PASSWORD = "tdbk ufjl aiae ejeh"
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465  # Puerto para conexión segura (SSL)

    def __init__(self):
        """
        Inicializa la clase con los detalles del remitente predefinidos.
        """
        pass  # No es necesario hacer nada en el init ya que los valores están fijos

    def send_email(self, email_receiver, subject, body):
        """
        Envía un correo electrónico al destinatario con el asunto y cuerpo proporcionados.

        :param email_receiver: Correo electrónico del destinatario.
        :param subject: Asunto del correo.
        :param body: Cuerpo del correo.
        """
        # Crear el mensaje de correo
        em = EmailMessage()
        em['From'] = self.EMAIL_SENDER
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Crear contexto seguro para la conexión SSL
        context = ssl.create_default_context()

        # Enviar el correo utilizando SMTP sobre SSL
        try:
            with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT, context=context) as smtp:
                smtp.login(self.EMAIL_SENDER, self.PASSWORD)
                smtp.sendmail(self.EMAIL_SENDER, email_receiver, em.as_string())
                print(f'Correo enviado a {email_receiver}')
        except Exception as e:
            print(f'Error al enviar correo: {e}')


# Ejemplo de uso de la clase

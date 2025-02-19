from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.headless = True  # Ejecuta en modo sin interfaz gráfica
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(3)  # Espera más corta para optimizar pruebas

        # Crear un usuario superusuario de prueba
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()  # Cierra el navegador
        super().tearDownClass()

    def test_login(self):
        # Navegar a la página de inicio de sesión
        self.selenium.get(f'{self.live_server_url}/admin/login/')

        # Verificar título de la página
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        # Rellenar formulario de inicio de sesión
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("isard")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        # Verificar acceso exitoso al panel de administración
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

import os
import time
import random
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from image_editor import apply_professional_design  # Asumiendo que tienes este módulo

class FacebookMarketplaceBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--headless")  # Modo headless para servidores sin GUI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        try:
            self.driver.get("https://www.facebook.com/")
            email_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "email")))
            email_field.send_keys(self.username)
            password_field = self.driver.find_element(By.NAME, "pass")
            password_field.send_keys(self.password)
            password_field.submit()
            self.wait.until(EC.url_matches("https://www.facebook.com/?sk=h_chr"))
            print("Inicio de sesión exitoso.")
        except Exception as e:
            print(f"Error durante el inicio de sesión: {e}")

    def complete_form(self, form_data):
        try:
            self.driver.get("https://www.facebook.com/marketplace/create/vehicle")
            print("Redireccionado a Marketplace.")
            
            # Selección aleatoria del año
            random_year = random.randint(2008, 2014)
            options = {
                "Tipo de vehículo": "Auto/camioneta",
                "Año": str(random_year),
                "Carrocería": "Familiar",
                "Estado del vehículo": "Excelente",
                "Transmisión": "Transmisión manual"
            }

            for category, option in options.items():
                self.select_option(category, option)

            for field_name, value in form_data.items():
                field = self.find_field_by_keyword(field_name)
                if field:
                    field.clear()
                    field.send_keys(value)
                    print(f"Campo '{field_name}' completado automáticamente con '{value}'.")
                else:
                    print(f"No se encontró el campo '{field_name}'.")

            self.fill_description("¡Auto usado en cuotas fijas y accesibles!")

            self.upload_photos_from_folder("fotos_autos", "autos_modificados")

            self.click_button("Siguiente")
        except Exception as e:
            print(f"Error al completar el formulario: {e}")

    def find_field_by_keyword(self, keyword):
        try:
            field = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{keyword}')]/following::input[1]")
            return field
        except:
            return None

    def fill_description(self, description):
        try:
            description_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.x1i10hfl")))
            description_field.clear()
            description_field.send_keys(description)
            print("Descripción completada automáticamente.")
        except Exception as e:
            print(f"Error al completar la descripción: {e}")

    def select_option(self, category, option):
        try:
            label_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//label[contains(@aria-label, '{category}')]")))
            self.driver.execute_script("arguments[0].scrollIntoView();", label_element)
            label_element.click()

            option_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{option}']")))
            option_element.click()
            print(f"Opción '{option}' seleccionada en '{category}'.")
        except Exception as e:
            print(f"Error al seleccionar la opción '{option}' en '{category}': {e}")

    def upload_photos_from_folder(self, folder_name, modified_folder_name, max_photos=5):
        try:
            folder_path = os.path.join(os.getcwd(), folder_name)
            modified_folder_path = os.path.join(os.getcwd(), modified_folder_name)
            if not os.path.exists(modified_folder_path):
                os.makedirs(modified_folder_path)
            photos = os.listdir(folder_path)
            random.shuffle(photos)
            for photo in photos[:max_photos]:
                original_path = os.path.join(folder_path, photo)
                modified_path = os.path.join(modified_folder_path, f"modified_{photo}")
                self.modify_and_save_photo(original_path, modified_path)
                input_field = self.driver.find_element(By.XPATH, "//input[@type='file']")
                input_field.send_keys(modified_path)
                print(f"Foto {photosubida correctamente.") except Exception as e: print(f"Error al cargar las fotos: {e}")
    def modify_and_save_photo(self, original_path, modified_path):
    try:
        original_image = cv2.imread(original_path)
        if original_image is None:
            raise FileNotFoundError(f"No se pudo leer la imagen: {original_path}")
        modified_image = apply_professional_design(original_image)
        cv2.imwrite(modified_path, modified_image)
    except Exception as e:
        print(f"Error al modificar y guardar la imagen: {e}")

def click_button(self, button_text):
    try:
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{button_text}']")))
        button.click()
        print(f"Botón '{button_text}' clicado.")
    except Exception as e:
        print(f"Error al hacer clic en el botón '{button_text}': {e}")

def close_browser(self):
    self.driver.quit()
    print("Navegador cerrado.")
if name == "main": with open("datos.txt", "r") as f: fb_username, fb_password, num_posts = f.read().strip().split(",")
    bot = FacebookMarketplaceBot(fb_username, fb_password)
bot.login()

for i in range(int(num_posts)):
    form_data = {
        "Marca": "¡Excelente oportunidad! - Autos usados en cuotas fijas",
        "Modelo": "y accesibles",
        "Precio": str(random.choice(range(60000, 150001, 20000))),
        "Millaje": "300"
    }
    bot.complete_form(form_data)
    time.sleep(15)  # Esperar entre publicaciones
    bot.click_button("Publicar")
    print(f"Publicación {i + 1} completada.")
    time.sleep(30)  # Esperar antes de la siguiente publicación

bot.close_browser()

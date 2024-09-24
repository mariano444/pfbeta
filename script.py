import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import cv2
from image_editor import apply_professional_design  # Asumiendo que tienes este módulo

class FacebookMarketplaceBot:
    def __init__(self, fb_username, fb_password):
        self.fb_username = fb_username
        self.fb_password = fb_password
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        try:
            self.driver.get("https://www.facebook.com/")
            email_field = self.wait.until(EC.visibility_of_element_located((By.NAME, "email")))
            email_field.send_keys(self.fb_username)
            password_field = self.driver.find_element(By.NAME, "pass")
            password_field.send_keys(self.fb_password)
            password_field.submit()
            self.wait.until(EC.url_matches("https://www.facebook.com/?sk=h_chr"))
            print("Inicio de sesión exitoso.")
        except TimeoutException:
            print("Tiempo de espera agotado durante el inicio de sesión.")
        except NoSuchElementException:
            print("No se encontró el campo de correo electrónico o contraseña.")
        except Exception as e:
            print(f"Error durante el inicio de sesión: {e}")

    def complete_form(self, form_data):
        try:
            self.driver.get("https://www.facebook.com/marketplace/create/vehicle")
            print("Redireccionado a Marketplace.")

            # Selección aleatoria del año y precio
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

            description = ("¿Buscas un auto usado? \n"
                           "¡Contáctanos ahora y descubre nuestras excelentes promociones! \n"
                           "Por qué elegir nuestra financiación:\n"
                           "Cuotas fijas y accesibles para que planifiques con tranquilidad.\n"
                           "Flexibilidad para adaptar la cuota según tus necesidades.\n"
                           "Financiamiento del 100% para tu auto usado.\n"
                           "Proceso de financiación sencillo, solo con tu DNI.\n"
                           "Aceptamos autos y motos usadas con la mejor tasación.\n"
                           "#AutosUsados #OfertasDeAutos #FinanciamientoFlexible #CuotasFijas #CompraInteligente #TasaciónJusta")
            self.fill_description(description)

            self.upload_photos_from_folder("fotos_autos", "autos_modificados")

            self.click_button("Siguiente")

        except TimeoutException:
            print("Tiempo de espera agotado durante la carga de Marketplace.")
        except NoSuchElementException:
            print("No se encontró el campo necesario en el formulario.")
        except Exception as e:
            print(f"Error al completar el formulario: {e}")

    def find_field_by_keyword(self, keyword):
        try:
            field = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{keyword}')]/following::input[1]")
            return field
        except NoSuchElementException:
            return None

    def fill_description(self, description):
        try:
            description_field = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.x1i10hfl")))
            description_field.clear()
            description_field.send_keys(description)
            print("Descripción completada automáticamente.")
        except TimeoutException:
            print("Tiempo de espera agotado para el campo de descripción.")
        except Exception as e:
            print(f"Error al completar la descripción: {e}")

    def select_option(self, category, option):
        try:
            label_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//label[contains(@aria-label, '{category}')]")))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });",
                label_element)
            self.driver.execute_script("arguments[0].click();", label_element)

            option_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{option}']")))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });",
                option_element)
            time.sleep(1)

            action = ActionChains(self.driver)
            action.move_to_element(option_element).click().perform()
            print(f"Opción '{option}' seleccionada en '{category}'.")
        except TimeoutException:
            print(f"No se pudo encontrar la opción '{option}' en '{category}'.")
        except Exception as e:
            print(f"Error al seleccionar la opción '{option}' en '{category}': {e}")

    def click_button(self, button_text):
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{button_text}']")))
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            time.sleep(2)
            button.click()
            print(f"Botón '{button_text}' clicado.")
        except TimeoutException:
            print(f"No se pudo encontrar el botón '{button_text}'.")
        except Exception as e:
            print(f"Error al hacer clic en el botón '{button_text}': {e}")

    def upload_photos_from_folder(self, folder_name, modified_folder_name, max_photos=10):
        try:
            folder_path = os.path.join(os.getcwd(), folder_name)
            modified_folder_path = os.path.join(os.getcwd(), modified_folder_name)
            if not os.path.exists(modified_folder_path):
                os.makedirs(modified_folder_path)
            photos = os.listdir(folder_path)
            random.shuffle(photos)
            num_photos_to_upload = min(max_photos, len(photos))
            photo_count = 0
            for index, photo in enumerate(photos):
                if photo_count >= num_photos_to_upload:
                    break
                photo_path = os.path.join(folder_path, photo)
                modified_photo_path = os.path.join(modified_folder_path, f"modified_{photo}")
                if index == 0:
                    self.modify_and_save_photo(photo_path, modified_photo_path)  # Usa la función desde el módulo externo
                else:
                    modified_photo_path = photo_path
                input_field = self.driver.find_element(By.XPATH, "//input[@type='file']")
                input_field.send_keys(modified_photo_path)
                print(f"Fotografía {photo} cargada.")
                photo_count += 1
                time.sleep(1)
                photos.remove(photo)
                self.driver.execute_script('arguments[0].value=""', input_field)
        except Exception as e:
            print(f"Error al cargar las fotos: {e}")

    def modify_and_save_photo(self, original_path, modified_path):
        """
        Modifica una foto aplicando un texto con fondo y un diseño profesional,
        y guarda la imagen modificada en la ruta especificada.
        """
        try:
            original_image = cv2.imread(original_path)
            if original_image is None:
                raise FileNotFoundError(f"No se pudo leer la imagen: {original_path}")

            # Aplicar mejoras visuales
            modified_image = apply_professional_design(original_image)
            cv2.imwrite(modified_path, modified_image)
        except Exception as e:
            print(f"Error al modificar y guardar la imagen: {e}")

    def close_browser(self):
        self.driver.quit()
        print("Navegador cerrado.")


if __name__ == "__main__":
    # Leer los datos desde el archivo
    with open("datos.txt", "r") as f:
        fb_username, fb_password, num_posts = f.read().split(",")

    # Crear la instancia del bot y realizar las publicaciones
    bot = FacebookMarketplaceBot(fb_username, fb_password)
    bot.login()

    for i in range(int(num_posts)):
        random_price = random.choice(range(60000, 150001, 20000))
        form_data = {
            "Marca": "¡Excelente oportunidad! - Autos usados en cuotas fijas",
            "Modelo": "y accesibles",
            "Precio": str(random_price),
            "Millaje": "300"
        }
        bot.complete_form(form_data)
        time.sleep(10)

    bot.close_browser()

    # Eliminar el archivo de credenciales después de la ejecución
    os.remove("datos.txt")
    print("Script completado y credenciales eliminadas.")

from playwright.sync_api import sync_playwright, expect
import re, time


def test_demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")

        #1. Hacer login con el usuario standard
        page.fill('#user-name', 'standard_user')
        page.fill('#password', 'secret_sauce')
        page.click('#login-button')
        
        #2. Añadir el producto Sauce Labs Backpack al carrito
        page.click('text=Sauce Labs Backpack')
        page.click('text=Add to cart')
        
        #3. Verificar que el botón cambia el texto de "Add to cart" a "Remove"
        add_to_cart_button = page.locator('text=Remove')
        expect(add_to_cart_button).to_be_visible()
        
        #4. Añadir el producto “Sauce Labs Bike Light” y “Sauce Labs Fleece Jacket” al carrito
        page.click('text=Back to products')
        page.click('text=Sauce Labs Bike Light')
        page.click('text=Add to cart')
        page.click('text=Back to products')
        page.click('text=Sauce Labs Fleece Jacket')
        page.click('text=Add to cart')
        
        #5. Eliminar el producto “Sauce Labs Backpack” del carrito
        page.click('text=Back to products')
        page.click('text=Sauce Labs Backpack')
        page.click('text=Remove')
        
        # 6. Verificar que el texto del botón cambia de "Remove" a "Add to cart"
        add_to_cart_button = page.locator('text=Add to cart')
        expect(add_to_cart_button).to_be_visible()
        
        #7. Hacer click en el carrito
        page.click('#shopping_cart_container')
        
        #8. Verificar que la url es: https://www.saucedemo.com/cart.html
        expect(page).to_have_url('https://www.saucedemo.com/cart.html')
        
        #9. Hacer click en el botón "Checkout"
        page.click('text=Checkout')
        
        #10. Pulsar en el botón de "Continue"
        page.click('text=Continue')
        
        #11. Verificar que aparece un mensaje de error con el texto First name is required
        #error_message = page.locator('#error-message-container')
        error_message = page.locator('xpath=//h3[contains(text(),"First Name is required")]')
        expect(error_message).to_be_visible()
        
        #12. Rellenar todo el formulario con tus datos personales
        page.fill('#first-name', 'Gabriel')
        page.fill('#last-name', 'Allende')
        page.fill('#postal-code', '29680')
        
        #13. Pulsar en el botón "Continue"
        page.click('text=Continue')
        
        #14. Verificar que el "Total" es la suma de "Item total" + "Tax"
        item_total = float(page.locator('xpath=//div[@class="summary_subtotal_label"]').text_content().split('$')[1])
        tax = float(page.locator('xpath=//div[@class="summary_tax_label"]').text_content().split('$')[1])
        total = float(page.locator('xpath=//div[@class="summary_total_label"]').text_content().split('$')[1])
        assert total == item_total + tax
        
        #15. Pulsar en el botón "Finish"
        page.click('text=Finish')
        
        #16. Verificar que aparece el mensaje "Thank you for your order!"
        thank_you_message = page.locator('xpath=//h2[contains(text(),"Thank you for your order!")]')
        expect(thank_you_message).to_be_visible()
        
        #17. Pulsar en el botón "Back Home"
        page.click('text=Back Home')
        
        #18. Hacer click en el menú desplegable
        page.click('xpath=//button[@id="react-burger-menu-btn"]')
        
        #19. Hacer click en "Logout"
        page.click('text=Logout')
        
        #20. Verificar que los campos "Username" y "Password" están visibles
        expect(page.locator('#user-name')).to_be_visible()
        expect(page.locator('#password')).to_be_visible()

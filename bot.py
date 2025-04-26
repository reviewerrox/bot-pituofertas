from telegram.ext import Application, CommandHandler
import requests

# Definir el token y las variables del bot
TOKEN = "7980488122:AAFnMz_OEzoLcYOAUenPqZyXbcQ87629qw0"
AFILIADO_TAG = "audrey073-21"
CANAL_ID = "@pituofertas"

# Categorías con ASIN de ejemplo
CATEGORIAS = {
    "Papá Pitufo": ["B08K2GWKHF", "B07PGL2ZSL"],
    "Pitufina": ["B08PXYZ123", "B09F9ABC456"],
    "Filósofo": ["B01N2XYZ678", "B07QWXYZ890"],
    "Fortachón": ["B08XYZA1234", "B09ABCD5678"],
    "Manitas": ["B06XYZ09876", "B08ABCDEFGHI"],
    "Goloso": ["B09JKL98765", "B07MNOP54321"],
    "Bromista": ["B08QRST12345", "B07UVWX09876"]
}

# Generar enlace con afiliado
def generar_enlace(asin):
    return f"https://www.amazon.es/dp/{asin}?tag={AFILIADO_TAG}"

# Publicar ofertas automáticamente
async def publicar_ofertas(context):
    for pitufo, productos in CATEGORIAS.items():
        await context.bot.send_message(chat_id=CANAL_ID, text=f"💙 Ofertas de {pitufo}:")
        for asin in productos:
            enlace = generar_enlace(asin)
            await context.bot.send_message(chat_id=CANAL_ID, text=f"🔹 {enlace}\nTe lo consiguió {pitufo} 💪")

# Comando /start
async def start(update, context):
    await update.message.reply_text("¡Bienvenido al Canal de pituofertas! 🚀")

# Comando /agregar para añadir productos manualmente
async def agregar(update, context):
    try:
        asin = context.args[0]
        enlace = generar_enlace(asin)
        await update.message.reply_text(f"Producto agregado:\n🔗 {enlace}")
    except IndexError:
        await update.message.reply_text("Por favor, proporciona un ASIN válido. Ejemplo: /agregar B08K2GWKHF")

# Configuración principal del bot
def main():
    # Crear la aplicación del bot
    application = Application.builder().token(TOKEN).build()

    # Configurar publicaciones automáticas en el arranque
    async def configurar_publicaciones(app):
        app.job_queue.run_repeating(
            callback=publicar_ofertas,
            interval=14400,  # Cada 4 horas
            first=10         # Primer inicio después de 10 segundos
        )

    # Agregar comandos al manejador
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("agregar", agregar))

    # Vincular la función de configuración correctamente
    application.post_init = lambda: application.create_task(configurar_publicaciones(application))

    # Iniciar el bot
    application
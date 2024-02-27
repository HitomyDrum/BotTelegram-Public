import colorama
from colorama import Fore
colorama.init(autoreset=True)
from config import *
import MySQLdb
import sys, os
from aiogram import Bot, executor, types, Dispatcher
import logging
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from command_register import registerUser
import asyncio
import requests
import json
# from limpiador import *
from funciones import conexion
import datetime

# intanciar bot
command = "/.,*"
bot = bool(os.environ.get('bot', True))
token = os.environ.get("token", None)

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

async def getUser(id):
    query = f"SELECT * FROM {conexion.DB_TABLE_} WHERE `usuarios`.`Id` = '{id}';"

    data = await conexion.run_query(query)

    info = []

    if data == None:
        info = ["NO REGISTRADO"]
    else:
        info = ["REGISTRADO"]
        for data in data:
            info.append(data)

    return info

async def getUserDarCreditos(id):
    query = f"SELECT * FROM {conexion.DB_TABLE_} WHERE `usuarios`.`UserTelegram` = '{id}';"

    data = await conexion.run_query(query)

    info = []

    if data == None:
        info = ["NO REGISTRADO"]
    else:
        info = ["REGISTRADO"]
        for data in data:
            info.append(data)

    return info

async def extract_arg(arg):
    await asyncio.sleep(0)
    return arg.split()[1:]

async def printError():
    await asyncio.sleep(0)

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(f"\n{Fore.LIGHTBLACK_EX} [*] ERROR: {Fore.LIGHTWHITE_EX}{exc_type}", f"{Fore.LIGHTWHITE_EX}{fname}", f"{Fore.RED}linea: {exc_tb.tb_lineno}")

async def printComandoEjecutado(user_nick, user_name, comando, fecha_hora, chatID):
    if chatID == CHAT_GRUPO:
        infoComandoLugar = "Dentro del grupo"
    else: infoComandoLugar = "Fuera del grupo"


    print(f"{Fore.LIGHTGREEN_EX} ╔═══════════▌ Comando Ejecutado ▐═══════════")
    print(f"{Fore.LIGHTGREEN_EX} ║ Consultado por: {Fore.LIGHTWHITE_EX}{user_nick}")
    print(f"{Fore.LIGHTGREEN_EX} ║ Username: {Fore.LIGHTWHITE_EX}{user_name}")
    print(f"{Fore.LIGHTGREEN_EX} ║ Comando: {Fore.LIGHTWHITE_EX}{comando}")
    print(f"{Fore.LIGHTGREEN_EX} ║ Fecha y Hora: {Fore.LIGHTWHITE_EX}{fecha_hora}")
    print(f"{Fore.LIGHTGREEN_EX} ║ Grupo: {Fore.LIGHTWHITE_EX}{infoComandoLugar}")
    print(f"{Fore.LIGHTGREEN_EX} ╚═══════════════════════════════════════════")

    await asyncio.sleep(0)

async def btnComprarCreditos():
    keyboard_inline = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Obtener créditos con: ", url="https://t.me/")
    btn2 = types.InlineKeyboardButton(text="User 1", url="https://t.me/")
    keyboard_inline.add(btn1)

    return keyboard_inline

# responde al comando /start
@dp.message_handler(commands=["start", "inicio"], commands_prefix=command)
async def cmd_start(message: types.Message):
    Id                  = message.from_user.id
    user_owner          = message.from_user.username
    user_comun          = message.from_user.first_name
    chatID              = message.chat.id
    chatType            = message.chat.type

    fecha_hora_actual   = datetime.datetime.now(); fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M:%S")

    await printComandoEjecutado(user_comun, user_owner, message.text, fecha_hora_formateada, chatID)

    keyboard_inline     = await btnComprarCreditos()

    SaludoInicialComun = f"{TITULO}\
        \n Hola  {user_comun}\
        \n Escribe /cmds para saber mis comandos."
    await message.reply(SaludoInicialComun, reply_markup=keyboard_inline)

    #========================| Actualizar ChatID o añadir nuevo chatID para los anuncios |============================#

    if chatType == 'private':
        if user_owner == None or user_owner == "None":
            print(f"{Fore.LIGHTMAGENTA_EX} > El usuario no tiene username, no se hace nada.")
        else:
            print(f"{Fore.LIGHTMAGENTA_EX} > El usuario está en privado, procedemos a actualizar su chat ID")
            # Consulta usuario de telegram está registrado
            query               = f"SELECT UserTelegram FROM {conexion.DB_TABLE_} WHERE Id = '{Id}';"
            usuarioRegistrado   = await conexion.run_query(query)

            if usuarioRegistrado != None:
                queryUpdateChatID = f"UPDATE {conexion.DB_TABLE_} SET ChatID = '{chatID}' WHERE Id = '{Id}';"
                await conexion.run_query(queryUpdateChatID)

                print(f"{Fore.LIGHTMAGENTA_EX} > Se actualizó el chat ID privado correctamente!")

@dp.message_handler(commands=["register"], commands_prefix=command)
async def cmdConsultaRegistrar(message: types.Message):
    id          = message.from_user.id
    user        = message.from_user.username
    nick        = message.from_user.first_name
    chatID      = message.chat.id
    messageID   = message.message_id
    chatType    = message.chat.type
    
    await registerUser(bot, id, user, nick, message, chatID, messageID, chatType)

# Mandar mensajes globalmente a todos por privado y en el grupo
@dp.message_handler(commands=["anuncio"], commands_prefix=command)
async def cmdPublicarAnuncio(message: types.Message):
    txtAnuncioPublicar = message.text.replace('/anuncio ', '')

    # Conecta a la base de datos MySQL
    datos = [conexion.DB_HOST_, conexion.DB_USER_, conexion.DB_PASS_, conexion.DB_NAME_, conexion.DB_PUERTO_] 

    conn = MySQLdb.connect(*datos)
    cursor = conn.cursor()

    # Consulta la base de datos para obtener los usuarios con chatID no nulo
    cursor.execute("SELECT Id, chatID, UserTelegram FROM usuarios WHERE chatID IS NOT NULL")
    users_with_chat_ids = cursor.fetchall()

    # Cierra la conexión a la base de datos
    conn.close()

    image_path = './imagenes/'
    keyboard_inline     = await btnComprarCreditos()

    # Enviar al GRUPO
    await bot.send_photo(CHAT_GRUPO, photo=open(image_path, 'rb'), caption=txtAnuncioPublicar, reply_markup=keyboard_inline)
    await asyncio.sleep(1)

    for user_id, chat_id, user_tele in users_with_chat_ids:
        try:
            
            await bot.send_photo(chat_id, photo=open(image_path, 'rb'), caption=txtAnuncioPublicar, reply_markup=keyboard_inline)
            # await bot.send_message(chat_id, txtAnuncioPublicar)
            print(f"se envió el msj a {chat_id}")
        except Exception as e:
            logging.error(f"No se pudo enviar un mensaje a {user_tele}: {e}")

#################################################################################################
@dp.message_handler(commands=["reglas", "rules"], commands_prefix=command)
async def cmdReglas(message: types.Message):
    user_owner = message.from_user.username
    user_comun = message.from_user.first_name
    chatID = message.chat.id
    fecha_hora_actual = datetime.datetime.now(); fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M:%S")

    await printComandoEjecutado(user_comun, user_owner, message.text, fecha_hora_formateada, chatID)


    keyboard_inline = await btnComprarCreditos()

    if chatID == CHAT_GRUPO:
        await message.reply(REGLAS, reply_markup=keyboard_inline)

@dp.message_handler(commands=["precios", "prices", "buy"], commands_prefix=command)
async def cmdPrecios(message: types.Message):
    user_owner = message.from_user.username
    user_comun = message.from_user.first_name
    chatID = message.chat.id
    fecha_hora_actual = datetime.datetime.now(); fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M:%S")

    await printComandoEjecutado(user_comun, user_owner, message.text, fecha_hora_formateada, chatID)

    keyboard_inline = await btnComprarCreditos()

    await message.reply(PRECIOS, reply_markup=keyboard_inline)

@dp.message_handler(commands=["staff", "admins"], commands_prefix=command)
async def cmdStaff(message: types.Message):
    user_owner = message.from_user.username
    user_comun = message.from_user.first_name
    chatID = message.chat.id
    fecha_hora_actual = datetime.datetime.now(); fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%Y %H:%M:%S")

    await printComandoEjecutado(user_comun, user_owner, message.text, fecha_hora_formateada, chatID)

    keyboard_inline = await btnComprarCreditos()

    await message.reply(STAFF, reply_markup=keyboard_inline)


@dp.message_handler(commands=["me"], commands_prefix=command)
async def cmdConsultaMe(message: types.Message):
    id          = message.from_user.id
    user        = message.from_user.username
    nick        = message.from_user.first_name
    chatID      = message.chat.id
    messageID   = message.message_id

    if user == None or user == "None":
        await message.reply(INFO_NO_REGISTRADO, parse_mode="html")
        return
    
    data        = await getUser(id)
    print(data)
    
    datos = f"{TITULO}\
        \n ┌ Usuario ID ➟ {data[1]}\
        \n ├ Username ➟ @{data[5]} \
        \n ├ Nick ➟ {nick}\
        \n ├ Creditos ➟ {data[3]}\
        \n ├ Rango ➟ {data[4]}\
        \n ├ AntiSpam ➟ {data[8]}\
        \n └ Registro ➟ {data[7]}"
    
    rutaFoto = "./imagenes/.jpg"
    await bot.send_photo(chatID, types.InputFile(rutaFoto), caption=datos, reply_to_message_id=messageID)

############ Páginas #############
pag1 = (f"{TITULO}\n\
        \n » Pagina [1]")

pag2 = (f"{TITULO}\n\
        \n » Pagina [2]")

textos = [pag1, pag2]

@dp.message_handler(commands=["cmds"])
async def send_texts(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Siguiente →", callback_data="1"))  # Empezamos desde el primer texto
    await bot.send_message(message.chat.id, textos[0], reply_markup=keyboard, parse_mode="html")

#########################################

async def actualizarUsandoNo(): # Setear No a todos
    query = f"UPDATE {conexion.DB_TABLE_} SET Usando ='no';"
    await conexion.run_query(query)

async def set_default_commands(dp):
    await bot.set_my_commands([
        types.BotCommand("start", "Saludo inicial del BOT"),
        types.BotCommand("cmds", "Comandos del BOT")
    ])

async def on_startup(dp):
    logging.basicConfig(level = logging.INFO)

    await set_default_commands(dp)
    print(f"{Fore.LIGHTGREEN_EX} [•] BOT TELEGRAM ON!")
    cores = os.cpu_count()
    print(f"{Fore.LIGHTCYAN_EX} > Tienes {cores} cores")
    await actualizarUsandoNo()

if __name__ == '__main__':
    print(f"{Fore.YELLOW} [•] BOT TELEGRAM")
    print(f"{Fore.LIGHTCYAN_EX} [•] Corriendo BOT TELEGRAM.")
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

    
    
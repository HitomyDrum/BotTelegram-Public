import colorama
from colorama import Fore
colorama.init(autoreset=True)
import random
import asyncio
from funciones.conexion import run_query, DB_TABLE_
from config import TITULO
import datetime
from aiogram import types

async def generarKey(user):
    codigosAlt = ['$', '%', '/', '+', '-', '*']
    rndNum = random.randint(0, 99); rndNum2 = random.randint(0, 99)
    cod1 = codigosAlt[random.randint(0, len(codigosAlt)-1)]
    cod2 = codigosAlt[random.randint(0, len(codigosAlt)-1)]
    key = f"{cod1}{rndNum}{user}{cod2}{rndNum2}"

    await asyncio.sleep(0)

    return key

async def registrarMySQL(bot, id, user, nick, message, chat_id, messageID, chatType):
    print(f"ID: |{id}|{user}|{nick} | {chatType}")
    # Info si es que no tiene username
    if user == None or user == "None":
        datos = f"\{TITULO}\n❌ Necesitas crear un username antes del registro. ❌"
        await message.reply(datos, parse_mode="html")

        return

    # Consulta usuario de telegram está registrado
    query = f"SELECT UserTelegram FROM {DB_TABLE_} WHERE Id = '{id}';"

    usuarioRegistrado = await run_query(query)
    fecha_hora_actual = datetime.datetime.now()

    creditos__Bienvenida = 100

    if usuarioRegistrado == None:
        keyGenerada = await generarKey(user)
        
        if chatType == 'private':
            registrarUsuario = f"INSERT INTO `usuarios` (`Id`, `Keys420`, `Creditos`, `UserTelegram`, `FechaCrea`, `ChatID`) VALUES ('{id}', '{keyGenerada}', '{creditos__Bienvenida}', '{user}', '{fecha_hora_actual}', '{chat_id}');"
        else:
            registrarUsuario = f"INSERT INTO `usuarios` (`Id`, `Keys420`, `Creditos`, `UserTelegram`, `FechaCrea`) VALUES ('{id}', '{keyGenerada}', '{creditos__Bienvenida}', '{user}', '{fecha_hora_actual}');"
        
        await run_query(registrarUsuario)

        datos = f"{TITULO}\
            \n ↳ Usuario registrado con éxito ✅\
            \n ↳ Username ➟ @{user} \
            \n ↳ Nick ➟ {nick}\
            \n ↳ Créditos de bienvenida ➟ {creditos__Bienvenida}"
        
        print(f"{Fore.LIGHTMAGENTA_EX} ┌─────────────────────────────────────")
        print(f"{Fore.LIGHTMAGENTA_EX} │ »{Fore.LIGHTWHITE_EX} Usuario registrado con éxito")
        print(f"{Fore.LIGHTMAGENTA_EX} └─────────────────────────────────────")

        print(datos)
        rutaFoto = "./imagenes/banner-sins.jpg"
        await bot.send_photo(chat_id, types.InputFile(rutaFoto), caption=datos, reply_to_message_id=messageID)

        return

    datos = f"{TITULO}\
        \n  ↳ Ya estás registrado {nick}⚠️"

    print(f"{Fore.LIGHTMAGENTA_EX} ┌─────────────────────────────────────")
    print(f"{Fore.LIGHTMAGENTA_EX} │ »{Fore.LIGHTWHITE_EX} Ya está registrado {nick}")
    print(f"{Fore.LIGHTMAGENTA_EX} └─────────────────────────────────────")
    
    await message.reply(datos, parse_mode="html")

async def registerUser(bot, id, user, nick, message, chatID, messageID, chatType):
    await registrarMySQL(bot, id, user, nick, message, chatID, messageID, chatType)